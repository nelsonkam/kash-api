from celery import shared_task
from django.contrib.contenttypes.models import ContentType

from kash.utils import TransactionStatusEnum, TransactionType


@shared_task
def request_transaction(txn_id=None):
    from kash.models import Transaction

    txn = Transaction.objects.get(pk=txn_id)
    txn.request()


@shared_task
def check_txn_status():
    from kash.models import Transaction

    for txn in Transaction.objects.filter(status=TransactionStatusEnum.pending.value,
                                          transaction_type=TransactionType.payment):
        txn.check_status()


@shared_task
def send_pending_notifications():
    from kash.models import Notification

    for notification in Notification.objects.filter(sent_at__isnull=True):
        notification.send()
