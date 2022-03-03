import json
import logging
from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now
from requests import ReadTimeout, request
from requests.auth import HTTPBasicAuth

from .base import BaseProvider
from kash.xlib.utils.utils import (
    Gateway,
    TransactionStatus,
    generate_reference_10,
    TransactionType,
)

logger = logging.getLogger(__name__)

class QosicProvider(BaseProvider):
    def process(self, transaction):
        if transaction.transaction_type != TransactionType.payment:
            return
        if transaction.gateway == Gateway.mtn:
            self._request_mtn_mobile_money(transaction)
        elif transaction.gateway == Gateway.moov:
            self._request_moov_mobile_money(transaction)
        else:
            raise NotImplementedError()

    def payout(self, transaction):
        if transaction.transaction_type != TransactionType.payout:
            return

        data = self.get_request_data(transaction)
        try:
            response = self.api_client.post(self.get_payout_endpoint(transaction), data)
            logger.info(response.text, response.status_code, response.status_code == 200)
            assert response.status_code == 200
            assert int(response.json()["responsecode"]) == 0
        except (AssertionError, ValueError) as e:
            # todo; add logger to see more
            logger.error(e)
            transaction.change_status(TransactionStatus.failed)
        except ReadTimeout:
            pass
        else:
            response_data = response.json()
            transaction.change_status(
                status=TransactionStatus.success,
                service_message=response_data["responsemsg"],
                service_reference=response_data["serviceref"],
            )

    def check_status(self, transaction):
        try:
            response = self.api_client.post(
                "QosicBridge/user/gettransactionstatus",
                {
                    "transref": transaction.reference,
                    "clientid": self._get_client_id(transaction),
                },
            )
        except ReadTimeout:
            return
        else:

            status = transaction.status

            if response.status_code == 200:
                response_data = response.json()
                if (
                    response_data["responsecode"]
                    and int(response_data["responsecode"]) == 0
                ):
                    status = TransactionStatus.success
                elif (
                    response_data["responsemsg"]
                    and "success" in response_data["responsemsg"].lower()
                ):
                    status = TransactionStatus.success
                elif response_data["responsecode"] == "01":
                    status = TransactionStatus.pending
                elif response_data["responsecode"] == "529":
                    status = TransactionStatus.failed
                elif (
                    response_data["responsemsg"] == "FAILED"
                    and response_data["responsecode"] == "-1"
                ):
                    status = TransactionStatus.failed

                transaction.change_status(
                    status=status,
                    service_message=response_data["responsemsg"],
                    service_reference=response_data["serviceref"],
                )

        if (
            transaction.created + timedelta(minutes=2) < now()
            and status != TransactionStatus.success
        ):
            transaction.change_status(TransactionStatus.failed)

    def refund(self, transaction):
        if transaction.status != TransactionStatus.success:
            return

        data = self.get_request_data(transaction)
        data["transref"] = generate_reference_10()
        transaction.refund_reference = data["transref"]
        transaction.save(update_fields=["refund_reference"])
        try:
            response = self.api_client.post(self.get_payout_endpoint(transaction), data)
            print(response.text, response.status_code, response.status_code == 200)
            assert response.status_code >= 200
            assert int(response.json()["responsecode"]) == 0
        except (AssertionError, ValueError) as e:
            logger.error(e)
            return False
        else:
            transaction.change_status(TransactionStatus.refunded)

    def retry(self, transaction):
        if transaction.status == TransactionStatus.success:
            return

        transaction.status = TransactionStatus.pending
        transaction.save()
        self.check_status(transaction)
        transaction.refresh_from_db()
        if transaction.status == TransactionStatus.success:
            return

        transaction.reference = generate_reference_10()
        transaction.save(update_fields=["reference"])

        if transaction.transaction_type == TransactionType.payment:
            self.process(transaction)
        elif transaction.transaction_type == TransactionType.payout:
            self.payout(transaction)
        else:
            raise NotImplemented()

    @property
    def api_client(self):
        return QosicAPIClient()

    def _get_client_id(self, transaction):
        if transaction.gateway == Gateway.mtn:
            return settings.QOSIC_MTN_MOBILE_MONEY_CLIENT_ID
        elif transaction.gateway == Gateway.moov:
            return settings.QOSIC_MOOV_MONEY_CLIENT_ID
        else:
            raise NotImplementedError()

    def get_request_data(self, transaction):
        data = {
            "amount": str(int(round(transaction.amount.amount))),
            "msisdn": self.format_phone(transaction.phone),
            "transref": transaction.reference,
            "clientid": self._get_client_id(transaction),
        }

        if settings.DEBUG or settings.APP_ENV == 'beta':
            data["amount"] = "1"
        return data

    def get_payout_endpoint(self, transaction):
        if transaction.gateway == Gateway.mtn:
            return f"QosicBridge/user/deposit"
        elif transaction.gateway == Gateway.moov:
            return f"QosicBridge/user/depositmv"
        else:
            raise NotImplementedError()

    def get_payment_endpoint(self, transaction):
        if transaction.gateway == Gateway.mtn:
            return f"QosicBridge/user/requestpayment"
        elif transaction.gateway == Gateway.moov:
            return f"QosicBridge/user/requestpaymentmv"
        else:
            raise NotImplementedError()

    def format_phone(self, phone):
        if phone.startswith("+"):
            phone = f"{phone[1:]}"
        if phone.startswith("00"):
            phone = f"{phone[2:]}"
        if len(phone) == 8 or not phone.startswith("229"):
            phone = f"229{phone}"

        return phone

    def _request_moov_mobile_money(self, transaction):
        data = self.get_request_data(transaction)
        try:
            response = self.api_client.post(
                self.get_payment_endpoint(transaction), data
            )
            print(response.text, response.status_code, response.status_code == 200)
            assert response.status_code >= 200
        except (AssertionError, ReadTimeout) as e:
            # todo; add logger to see more
            transaction.change_status(TransactionStatus.pending)
        else:
            response_data = response.json()
            if (
                response_data["responsecode"]
                and int(response_data["responsecode"]) == 0
            ):
                status = TransactionStatus.success
            elif response_data["responsecode"] in [
                "8",
                "92",
                "94",
                "95",
                "10",
                "91",
                "98",
                "99",
                "-1",
            ]:
                status = TransactionStatus.failed
            else:
                raise NotImplementedError()

            service_message = response_data["responsemsg"]
            service_reference = response_data["serviceref"]
            transaction.change_status(status, service_message, service_reference)

    def _request_mtn_mobile_money(self, transaction):
        data = self.get_request_data(transaction)
        try:
            response = self.api_client.post(
                self.get_payment_endpoint(transaction), data
            )
            print(response.text, response.status_code, response.status_code == 200)
            assert response.status_code >= 200
        except (AssertionError, ReadTimeout) as e:
            print(e)
            transaction.change_status(TransactionStatus.pending)
        else:
            response_data = response.json()
            transaction.change_status(
                status=TransactionStatus.pending,
                service_message=response_data["responsemsg"],
                service_reference=response_data["serviceref"],
            )


class QosicAPIClient:
    __version__ = "0.0.1"
    _base_url = settings.QOSIC_URL

    def __init__(
        self,
        username=settings.QOSIC_USERNAME,
        password=settings.QOSIC_PASSWORD,
        timeout=30,
        verify_ssl=False,
    ):
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.username = username
        self.password = password

    def _get_url(self, endpoint):
        """Get URL for requests"""
        url = self._base_url

        if url.endswith("/"):
            url = url[:-1]
        if endpoint.startswith("/"):
            endpoint = endpoint[:-1]

        return f"{url}/{endpoint}"

    def _request(self, method, endpoint, data, params=None, **kwargs):
        """Do requests"""
        if params is None:
            params = {}

        url = self._get_url(endpoint)
        headers = {
            "user-agent": "Qosic API Client-Python/%s" % self.__version__,
            "accept": "application/json",
        }
        if "headers" in kwargs:
            headers = {**kwargs.pop("headers"), **headers}

        if data is not None:
            data = json.dumps(data, ensure_ascii=False).encode("utf-8")
            headers["content-type"] = "application/json;charset=utf-8"

        return request(
            method=method,
            url=url,
            verify=self.verify_ssl,
            auth=HTTPBasicAuth(self.username, self.password),
            params=params,
            data=data,
            timeout=self.timeout,
            headers=headers,
            **kwargs,
        )

    def post(self, endpoint, data, **kwargs):
        """POST requests"""
        return self._request("POST", endpoint, data, **kwargs)
