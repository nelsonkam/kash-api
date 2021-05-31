from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from django.utils.dateparse import parse_datetime
from djmoney.money import Money

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
def sync_wallet_transactions():
    from kash.models import Wallet, WalletTransaction
    fetched = 0
    for wallet in Wallet.objects.all():
        latest_payment = wallet.wallettransaction_set.order_by("timestamp").last()
        payments = StellarHelpers.horizon_server.payments().for_account(
            wallet.external_id
        ).include_failed(True).limit(100)
        if latest_payment:
            payments = payments.cursor(latest_payment.cursor)
        payments = payments.call()
        payments = payments.get("_embedded").get("records")
        data = StellarHelpers.format_payment_transactions(wallet, payments)
        fetched += len(data)
        for item in data:
            source = item.get('source')[1:] if item.get('source') != "Kash" else item.get('source')
            WalletTransaction.objects.create(
                wallet=wallet,
                is_successful=item.get("successful"),
                cursor=item.get("cursor"),
                timestamp=parse_datetime(item.get("created_at")),
                amount=Money(item.get('amount'), "XOF"),
                txn_type=item.get('type'),
                source=source,
                memo=item.get("memo", "") or "",
                external_id=item.get('account_id')
            )
    print(f"{fetched} items fetched!")


def get_merchants():
    from kash.models import VirtualCard
    count_result = {}
    amount_result = {}
    for card in VirtualCard.objects.all():
        txns = card.get_statement()
        for txn in txns:
            merchant = txn.get("merchant")
            count_result[merchant] = count_result.get(merchant, 0)
            count_result[merchant] += 1
            amount_result[merchant] = amount_result.get(merchant, 0)
            amount_result[merchant] += float(txn.get('amount'))
    for k, v in count_result.items():
        print(k, v, amount_result.get(k))
