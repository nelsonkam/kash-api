from datetime import timedelta

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from django.utils.timezone import now
from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from requests import ReadTimeout

from core.utils.notify import tg_bot
from kash.api import QosicAPI
from kash.signals import transaction_status_changed
from kash.tasks import request_transaction
from kash.utils import GatewayEnum, TransactionStatusEnum, generate_reference_10, TransactionType


class TransactionManager(models.Manager):
    def request(self, obj, name, phone, amount, gateway, initiator, txn_type=TransactionType.payment, **kwargs):
        assert gateway in GatewayEnum.values(), f"The gateway `{gateway}` is not supported."
        amount = amount if isinstance(amount, Money) else Money(amount, 'XOF')
        amount = round(convert_money(amount, "XOF"))
        transaction = self.model(
            content_object=obj,
            name=name or '',
            phone=phone,
            amount=amount,
            gateway=gateway,
            initiator=initiator,
            transaction_type=txn_type
        )
        if 'reference' in kwargs:
            transaction.reference = kwargs['reference']

        transaction.save()
        if txn_type == TransactionType.payment:
            request_transaction.delay(transaction.id)
        else:
            transaction.request()
        return transaction


class Transaction(models.Model):
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    content_object = GenericForeignKey('content_type', 'object_id')
    gateway = models.CharField(max_length=20, choices=GatewayEnum.items())
    reference = models.CharField(max_length=50, default=generate_reference_10, unique=True)
    service_reference = models.CharField(max_length=40, null=True)
    status = models.CharField(max_length=40, default=TransactionStatusEnum.pending.value,
                              choices=TransactionStatusEnum.items())
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency='XOF')
    name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=45)
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices, default=TransactionType.payment)
    service_message = models.CharField(max_length=512, null=True)
    last_status_checked = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey('core.User', on_delete=models.CASCADE, null=True)

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

    def retry(self, is_async=False):
        if self.status == TransactionStatusEnum.success.value:
            return

        self.status = TransactionStatusEnum.pending
        self.save()
        self.check_status()

        if self.status == TransactionStatusEnum.success.value:
            return

        self.reference = generate_reference_10()
        self.save()

        if is_async:
            request_transaction.delay(self.pk)
        else:
            self.request()

    def request(self):
        if self.transaction_type == TransactionType.payment:
            if self.gateway == GatewayEnum.mtn.value:
                self._request_mtn_mobile_money()
            elif self.gateway == GatewayEnum.moov.value:
                self._request_moov_mobile_money()
            else:
                raise NotImplementedError()
        elif self.transaction_type == TransactionType.payout or self.transaction_type == TransactionType.refund:
            if self.gateway == GatewayEnum.mtn.value:
                self._payout_mtn_mobile_money()
            elif self.gateway == GatewayEnum.moov.value:
                self._payout_moov_mobile_money()
            else:
                raise NotImplementedError()

    def _payout_mtn_mobile_money(self):
        data = self._get_request_data()

        try:
            response = self.api.Transaction.payout(data)
            print(response.text, response.status_code, response.status_code == 200)
            assert response.status_code == 200, \
                "%s: status_code: %s content: %s" % (self, response.status_code, response.text)
            assert int(response.json()['responsecode']) == 0, "%s: responsecode: %s json: %s" % (
                self, response.json()['responsecode'], response.json())
        except (AssertionError, ReadTimeout, ValueError) as e:
            # todo; add logger to see more
            self.status = TransactionStatusEnum.failed.value
        else:
            response_data = response.json()
            self.status = TransactionStatusEnum.success.value
            self.service_message = response_data['responsemsg']
            self.service_reference = response_data['serviceref']

        self.last_status_checked = now()
        self.save()
        if self.status != TransactionStatusEnum.pending.value:
            transaction_status_changed.send(sender=self.__class__, transaction=self)

    def _payout_moov_mobile_money(self):
        data = self._get_request_data()

        try:
            response = self.api.Transaction.payout(data)
            print(response.text, response.status_code, response.status_code == 200)
            assert response.status_code == 200, \
                "%s: status_code: %s content: %s" % (self, response.status_code, response.text)
            assert int(response.json()['responsecode']) == 0, "%s: responsecode: %s json: %s" % (
                self, response.json()['responsecode'], response.json())
        except (AssertionError, ReadTimeout, ValueError) as e:
            # todo; add logger to see more
            self.status = TransactionStatusEnum.failed.value
        else:
            response_data = response.json()
            self.status = TransactionStatusEnum.success.value
            self.service_message = response_data['responsemsg']
            self.service_reference = response_data['serviceref']

        self.last_status_checked = now()
        self.save()
        if self.status != TransactionStatusEnum.pending.value:
            transaction_status_changed.send(sender=self.__class__, transaction=self)

    def _get_request_data(self):
        data = {
            "amount": str(int(round(self.amount.amount))),
            "msisdn": self.get_phone(),
            'transref': self.reference
        }

        if settings.DEBUG:
            data['amount'] = "1"
        return data

    def _request_moov_mobile_money(self):
        data = self._get_request_data()
        try:
            response = self.api.Transaction.create(data)
            print(response.text, response.status_code, response.status_code == 200)
            assert response.status_code == 200, \
                "%s: status_code: %s content: %s" % (self, response.status_code, response.text)
        except (AssertionError, ReadTimeout) as e:
            # todo; add logger to see more
            status = TransactionStatusEnum.failed.value
        else:
            response_data = response.json()
            if response_data['responsecode'] and int(response_data['responsecode']) == 0:
                status = TransactionStatusEnum.success.value
            elif response_data['responsecode'] in ['8', '92', '94', '95', '10', '91', '98', '99', '-1']:
                status = TransactionStatusEnum.failed.value
            else:
                raise NotImplementedError

            self.service_message = response_data['responsemsg']
            self.service_reference = response_data['serviceref']

        self.last_status_checked = now()
        self.status = status
        self.save()
        if self.status != TransactionStatusEnum.pending.value:
            transaction_status_changed.send(sender=self.__class__, transaction=self)

    def _request_mtn_mobile_money(self):
        data = self._get_request_data()
        try:
            response = self.api.Transaction.create(data)
            print(response.text, response.status_code, response.status_code == 200)
            assert response.status_code == 202, \
                "%s: status_code: %s content: %s" % (self, response.status_code, response.text)
        except (AssertionError, ReadTimeout) as e:
            self.status = TransactionStatusEnum.failed.value
            self.save()
        else:
            response_data = response.json()

            self.status = TransactionStatusEnum.pending.value
            self.service_message = response_data['responsemsg']
            self.service_reference = response_data['serviceref']
            self.save()

        if self.status != TransactionStatusEnum.pending.value:
            transaction_status_changed.send(sender=self.__class__, transaction=self)

    def refund(self):
        if self.status != TransactionStatusEnum.success.value:
            return

        txn = Transaction.objects.request(
            obj=self,
            name=self.name,
            phone=self.phone,
            gateway=self.gateway,
            initiator=self.initiator,
            amount=self.amount,
            txn_type=TransactionType.refund
        )

        if txn.status == TransactionStatusEnum.success.value:
            self.status = TransactionStatusEnum.refunded.value
            self.save()
            transaction_status_changed.send(sender=self.__class__, transaction=self)

    def check_status(self):
        if self.status != TransactionStatusEnum.pending.value:
            return

        response = self.api.Transaction.status(data={'transref': self.reference})

        status = self.status
        print("status", status)
        print(response.text, response.status_code, response.status_code == 200)

        if response.status_code == 200:
            response_data = response.json()
            print(response_data)
            if response_data['responsecode'] and int(response_data['responsecode']) == 0:
                status = TransactionStatusEnum.success.value
            elif response_data['responsemsg'] and 'success' in response_data['responsemsg'].lower():
                status = TransactionStatusEnum.success.value
            elif response_data['responsecode'] == '01':
                status = TransactionStatusEnum.pending.value
            elif response_data['responsecode'] == '529':
                status = TransactionStatusEnum.failed.value
            # elif self.gateway == GatewayEnum.moov.value and response_data['responsecode'] in ['8', '92', '94', '95', '10', '91', '98', '99']:
            #     status = TransactionStatusEnum.failed.value
            elif response_data['responsemsg'] == 'FAILED' and response_data['responsecode'] == '-1':
                status = TransactionStatusEnum.failed.value

            self.service_message = response_data['responsemsg']
            self.service_reference = response_data['serviceref']

            self.last_status_checked = now()
            self.save()

        if self.created + timedelta(minutes=2) < now() and status != TransactionStatusEnum.success.value:
            status = TransactionStatusEnum.failed.value

        if Transaction.objects.get(pk=self.pk).status != status:
            self.status = status
            self.save()
            transaction_status_changed.send(sender=self.__class__, transaction=self)

    def __str__(self):
        return f'{self.reference}/ {self.status}'

    class Meta:
        db_table = 'qosic_transaction'


@receiver(transaction_status_changed)
def notify(sender, **kwargs):
    txn = kwargs.pop("transaction")
    if txn.status == TransactionStatusEnum.success.value:
        tg_bot.send_message(chat_id=settings.TG_CHAT_ID, text=f"""
New successful {txn.transaction_type} on Kash!💪🏾

Type: {txn.content_type.model}
Amount: {txn.amount}
Reference: {txn.reference}
User: {txn.initiator.profile}

{"_Ceci est un message test._" if settings.DEBUG else ""}
""", disable_notification=True)
    elif txn.status == TransactionStatusEnum.failed.value and txn.transaction_type == TransactionType.payout:
        tg_bot.send_message(chat_id=settings.TG_CHAT_ID, text=f"""
⚠️ Payout failed!
Reference: {txn.reference}

{"_Ceci est un message test._" if settings.DEBUG else ""}
""")
