from datetime import timedelta

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now

from requests import ReadTimeout

from pay.api import QosicAPI
from pay.signals import transaction_status_changed
from pay.utils import GatewayEnum, TransactionStatusEnum, generate_reference_10


class TransactionManager(models.Manager):
    def request(self, obj, name, phone, amount, gateway, **kwargs):
        assert gateway in GatewayEnum.values(), f"The gateway `{gateway}` is not supported."

        transaction = self.model(
            content_object=obj,
            first_name=name,
            phone=phone,
            amount=amount,
            gateway=gateway,
        )
        if 'reference' in kwargs:
            transaction.reference = kwargs['reference']

        transaction.save()

        # if settings.DEBUG:
        #     return
        transaction.request()
        return transaction


class Transaction(models.Model):
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    content_object = GenericForeignKey('content_type', 'object_id')
    gateway = models.CharField(max_length=20, choices=GatewayEnum.items())
    reference = models.CharField(max_length=20, default=generate_reference_10, unique=True)
    service_reference = models.CharField(max_length=40, null=True)
    status = models.CharField(max_length=40, default=TransactionStatusEnum.pending.value, choices=TransactionStatusEnum.items())
    amount = models.DecimalField(max_digits=17, decimal_places=4)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=45)
    service_message = models.CharField(max_length=512, null=True)
    last_status_checked = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = TransactionManager()

    _api = None

    @property
    def api(self):
        if not self._api:
            if self.gateway == GatewayEnum.mtn.value:
                self._api = QosicAPI(settings.QOSIC_MTN_MOBILE_MONEY_CLIENT_ID, 'mtn', timeout=20)
            elif self.gateway == GatewayEnum.moov.value:
                self._api = QosicAPI(settings.QOSIC_MOOV_MONEY_CLIENT_ID, 'moov', timeout=60)
            else:
                raise NotImplementedError(f"The {self.gateway} payment method is not supported")

        return self._api

    def get_phone(self):
        phone = self.phone
        if phone.startswith('+'):
            phone = f'{phone[1:]}'
        if phone.startswith('00'):
            phone = f'{phone[2:]}'
        if len(phone) == 8 or not phone.startswith('229'):
            phone = f'229{phone}'

        return phone

    def request(self):
        if self.gateway == GatewayEnum.mtn.value:
            self._request_mtn_mobile_money()
        elif self.gateway == GatewayEnum.moov.value:
            self._request_moov_mobile_money()
        else:
            raise NotImplementedError()

    def _get_request_data(self):
        data = {
            "amount": str(self.amount),
            "msisdn": self.get_phone(),
            "firstname": self.first_name,
            "lastname": self.last_name,
            'transref': self.reference
        }

        if settings.DEBUG:
            data['amount'] = "1"
        return data

    def _request_moov_mobile_money(self):
        old_status = self.status
        data = self._get_request_data()
        try:
            response = self.api.Transaction.create(data)
            assert response.status_code == 200, \
                "%s: status_code: %s content: %s" % (self, response.status_code, response.text)
        except (AssertionError, ReadTimeout) as e:
            # todo; add logger to see more
            self.status = GatewayEnum.failed.value
        else:
            response_data = response.json()
            if response_data['responsecode'] == '0':
                self.status = GatewayEnum.success.value
            elif response_data['responsecode'] in ['8', '92', '94', '95', '10', '91', '98', '99', '-1']:
                self.status = GatewayEnum.failed.value
            else:
                raise NotImplementedError

            self.service_message = response_data['responsemsg']
            self.service_reference = response_data['serviceref']

        self.last_status_checked = now()
        self.save()

        if old_status != self.status:
            transaction_status_changed.send(sender=self. __class__, transaction=self)

    def _request_mtn_mobile_money(self):
        data = self._get_request_data()
        try:
            response = self.api.Transaction.create(data)
            assert response.status_code == 202, \
                "%s: status_code: %s content: %s" % (self, response.status_code, response.text)
        except (AssertionError, ReadTimeout) as e:
            self.status = TransactionStatusEnum.failed.value
            self.save(update_fields=('status',))
        else:
            response_data = response.json()

            self.status = GatewayEnum.pending.value
            self.service_message = response_data['responsemsg']
            self.service_reference = response_data['serviceref']
            self.save()
        # to automatically handle case when consumer amount is not enough
        self.check_status()

    def refund(self):
        # moov doesn't have refund api.
        if self.status != TransactionStatusEnum.success.value or self.gateway == TransactionStatusEnum.moov.value:
            return

        data = self._get_request_data()
        response = self.api.Transaction.refund(data)
        assert response.status_code == 200, "%s: status_code: %s content: %s" % (self, response.status_code, response.text)
        self.status = TransactionStatusEnum.refunded.value
        self.save()

        transaction_status_changed.send(sender=self.__class__, transaction=self)

    def check_status(self):
        if self.status != TransactionStatusEnum.pending.value:
            return

        response = self.api.Transaction.status(data={'transref': self.reference})

        old_status = self.status

        if response.status_code == 200:
            response_data = response.json()

            if response_data['responsecode'] == "00":
                self.status = TransactionStatusEnum.success.value

            elif response_data['responsecode'] == '01':
                self.status = TransactionStatusEnum.pending.value
            elif response_data['responsecode'] == '529':
                self.status = TransactionStatusEnum.failed.value
            elif response_data['responsemsg'] == 'FAILED' and response_data['responsecode'] == '-1':
                self.status = TransactionStatusEnum.failed.value

            self.service_message = response_data['responsemsg']
            self.service_reference = response_data['serviceref']

            self.last_status_checked = now()

        if self.created + timedelta(minutes=3) < now() and self.status != TransactionStatusEnum.success.value:
            self.status = TransactionStatusEnum.failed.value
        self.save()

        if self.status != old_status:
            transaction_status_changed.send(sender=self.__class__, transaction=self)

    def __str__(self):
        return f'{self.reference}/ {self.status}'

    class Meta:
        db_table = 'qosic_transaction'
