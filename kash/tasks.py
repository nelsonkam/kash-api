from celery import shared_task
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.dateparse import parse_datetime
from djmoney.money import Money

from core.utils.notify import tg_bot
from core.utils.payment import rave_request
from kash.utils import TransactionStatusEnum, TransactionType, StellarHelpers


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



@shared_task
def monitor_flw_balance():
    ngn_balance = rave_request("GET", "/balances/NGN").json().get("data").get("available_balance")
    usd_balance = rave_request("GET", "/balances/USD").json().get("data").get("available_balance")
    if ngn_balance < 90000 and usd_balance < 50:
        tg_bot.send_message(chat_id=settings.TG_CHAT_ID, text=f"""
        ⚠️ Flutterwave balance too low!
        NGN Balance: {ngn_balance}
        USD Balance: {usd_balance}

        {"_Ceci est un message test._" if settings.DEBUG else ""}
        """)


@shared_task
def retry_failed_withdrawals():
    from kash.models import Transaction, WithdrawalHistory
    qs = WithdrawalHistory.objects\
        .filter(status=WithdrawalHistory.Status.withdrawn)\
        .prefetch_related("card", "card__profile", "card__profile__user")

    for withdrawal in qs:
        phone, gateway = withdrawal.card.profile.get_momo_account()
        if phone and gateway:
            txn = Transaction.objects.request(
                obj=withdrawal.card,
                name=withdrawal.card.profile.name,
                amount=withdrawal.amount,
                phone=phone,
                gateway=gateway,
                initiator=withdrawal.card.profile.user,
                txn_type=TransactionType.payout
            )
            if txn.status == TransactionStatusEnum.success:
                withdrawal.status = WithdrawalHistory.Status.paid_out
                withdrawal.txn_ref = txn.reference
                withdrawal.save()
