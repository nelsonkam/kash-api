from django.contrib.contenttypes.models import ContentType
from huey import crontab
from huey.contrib.djhuey import db_task, db_periodic_task

from kash.utils import TransactionStatusEnum, TransactionType


@db_task()
def request_transaction(txn_id=None):
    from kash.models import Transaction

    txn = Transaction.objects.get(pk=txn_id)
    txn.request()


@db_periodic_task(crontab(minute="*"))
def check_txn_status():
    from kash.models import Transaction

    for txn in Transaction.objects.filter(status=TransactionStatusEnum.pending.value,
                                          transaction_type=TransactionType.payment):
        txn.request()


@db_periodic_task(crontab(minute="*/5"))
def confirm_card_purchase():
    from kash.models import VirtualCard, Transaction
    cards = VirtualCard.objects.filter(external_id__isnull=True)
    cart_type = ContentType.objects.get_for_model(VirtualCard)
    for txn in Transaction.objects.filter(content_type__pk=cart_type.id, object_id__in=cards,
                                          status=TransactionStatusEnum.success.value,
                                          transaction_type=TransactionType.payment):
        card = VirtualCard.objects.get(pk=txn.object_id)
        card.create_external(amount=txn.amount - card.issuance_cost)


@db_task()
def send_push_notification(profile_id, title, description, obj):
    from kash.models import Notification

    notif = Notification.objects.create(
        title=title,
        description=description,
        content_object=obj,
        profile_id=profile_id
    )
    notif.send()


@db_periodic_task(crontab(minute="*/5"))
def send_pending_notifications():
    from kash.models import Notification

    for notification in Notification.objects.filter(sent_at__isnull=True):
        notification.send()
