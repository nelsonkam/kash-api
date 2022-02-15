
import json

from django.conf import settings

from requests import request
from requests.auth import HTTPBasicAuth


class QosicAPI:
    __version__ = '0.0.1'
    _base_url = settings.QOSIC_URL

    def __init__(self, client_id, client_type, username=settings.QOSIC_USERNAME,
                 password=settings.QOSIC_PASSWORD, timeout=5, verify_ssl=False):
        self.client_id = client_id
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.username = username
        self.password = password
        self.client_type = client_type
        self.Transaction = TransactionResource(self)

    def _get_url(self, endpoint):
        """ Get URL for requests """
        url = self._base_url

        if url.endswith("/"):
            url = url[:-1]
        if endpoint.startswith('/'):
            endpoint = endpoint[:-1]

        return f'{url}/{endpoint}'

    def _request(self, method, endpoint, data, params=None, **kwargs):
        """ Do requests """
        if params is None:
            params = {}

        if data:
            data.setdefault('clientid', self.client_id)

        url = self._get_url(endpoint)
        headers = {
            "user-agent": "Qosic API Client-Python/%s" % self.__version__,
            "accept": "application/json"
        }
        if 'headers' in kwargs:
            headers = {**kwargs.pop('headers'), **headers}

        if data is not None:
            data = json.dumps(data, ensure_ascii=False).encode('utf-8')
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
            **kwargs
        )

    def post(self, endpoint, data, **kwargs):
        """ POST requests """
        return self._request("POST", endpoint, data, **kwargs)


class TransactionResource:
    def __init__(self, api):
        self.api = api
        self.base_url = 'QosicBridge/user'

    def create(self, data, **kwargs):
        if self.api.client_type == 'moov':
            url = f'{self.base_url}/requestpaymentmv'
        elif self.api.client_type == 'mtn':
            url = f'{self.base_url}/requestpayment'
        else:
            raise NotImplementedError

        return self.api.post(url, data, **kwargs)

    def status(self, data, **kwargs):
        return self.api.post(f'{self.base_url}/gettransactionstatus', data, **kwargs)

    def refund(self, data, **kwargs):
        return self.api.post(f'{self.base_url}/refund', data, **kwargs)

    def payout(self, data, **kwargs):
        if self.api.client_type == 'moov':
            url = f'{self.base_url}/depositmv'
        elif self.api.client_type == 'mtn':
            url = f'{self.base_url}/deposit'
        else:
            raise NotImplementedError
        return self.api.post(url, data, **kwargs)
