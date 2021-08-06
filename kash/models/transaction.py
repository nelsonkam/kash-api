from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from core.utils.notify import tg_bot
from kash.tasks import request_transaction
from kash.providers import PaymentProvider, get_payment_provider
from kash.signals import transaction_status_changed
from kash.utils import TransactionStatusEnum, generate_reference_10, TransactionType, Gateway, \
    TransactionStatus


class TransactionManager(models.Manager):
    def request(self, obj, name, phone, amount, gateway, initiator, txn_type=TransactionType.payment, **kwargs):
        assert gateway in Gateway.values, f"The gateway `{gateway}` is not supported."
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
        elif txn_type == TransactionType.payout:
            transaction.payout()
        else:
            raise NotImplementedError()

        return transaction


class Transaction(models.Model):
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    content_object = GenericForeignKey('content_type', 'object_id')
    gateway = models.CharField(max_length=20, choices=Gateway.choices)
    reference = models.CharField(max_length=50, default=generate_reference_10, unique=True)
    refund_reference = models.CharField(max_length=50, blank=True)
    service_reference = models.CharField(max_length=40, null=True)
    status = models.CharField(max_length=40, default=TransactionStatus.pending,
                              choices=TransactionStatus.choices)
    amount = MoneyField(max_digits=17, decimal_places=2, default_currency='XOF')
    name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=45)
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices, default=TransactionType.payment)
    service_message = models.CharField(max_length=512, null=True)
    last_status_checked = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    initiator = models.ForeignKey('core.User', on_delete=models.CASCADE, null=True)
    provider_name = models.CharField(max_length=20, choices=PaymentProvider.choices, default=PaymentProvider.qosic)

    objects = TransactionManager()

    @property
    def provider(self):
        return get_payment_provider(self.provider_name)

    def change_status(self, status, service_message="", service_reference=""):
        self.status = status
        self.service_message = service_message
        self.service_reference = service_reference
        self.save(update_fields=['status', 'service_message', 'service_reference'])
        transaction_status_changed.send(sender=self.__class__, transaction=self)

    def request(self):
        return self.provider.process(self)

    def payout(self):
        return self.provider.payout(self)

    def refund(self):
        return self.provider.refund(self)

    def retry(self):
        return self.provider.retry(self)

    def check_status(self):
        return self.provider.check_status(self)

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
