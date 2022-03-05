from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.db.models import Q
from django.db.models.aggregates import Count
from django.utils.timezone import now
from djmoney.money import Money

from kash.xlib.utils.notify import notify_telegram, notify_slack
from kash.xlib.utils.payment import rave_request
from kash.card.providers import RaveCardProvider
from kash.xlib.utils.utils import (
    TransactionStatusEnum,
    TransactionType,
    Conversions,
    TransactionStatus,
)


@shared_task
def request_transaction(txn_id=None):
    from kash.transaction.models import Transaction

    txn = Transaction.objects.get(pk=txn_id)
    txn.request()


@shared_task
def check_txn_status():
    from kash.transaction.models import Transaction

    qs = Transaction.objects.filter(
        Q(status=TransactionStatus.pending) | Q(status=TransactionStatus.failed),
        created__gte=now() - timedelta(minutes=15),
    )
    for txn in qs:
        txn.check_status()


@shared_task
def send_pending_notifications():
    from kash.notification.models import Notification

    for notification in Notification.objects.filter(sent_at__isnull=True):
        notification.send()


@shared_task
def monitor_flw_balance():
    if settings.DEBUG:
        return
    provider = RaveCardProvider()
    ngn_balance = (
        rave_request("GET", "/balances/NGN").json().get("data").get("available_balance")
    )
    usd_balance = (
        rave_request("GET", "/balances/USD").json().get("data").get("available_balance")
    )
    if not provider.is_balance_sufficient(Money(500, "USD")) and not settings.IS_BETA:
        notify_slack({
            "text": f"⚠️ Le compte Flutterwave est déchargé! (Solde: *${usd_balance}*) cc <@U022FUW39FT>"
        })
        notify_telegram(
            chat_id=settings.TG_CHAT_ID,
            text=f"""
        ⚠️ Flutterwave balance too low!
        NGN Balance: {ngn_balance}
        USD Balance: {usd_balance}

        {"_Ceci est un message test._" if settings.DEBUG else ""}
        """,
        )



@shared_task
def retry_failed_withdrawals():
    from kash.transaction.models import Transaction
    from kash.card.models import WithdrawalHistory

    qs = WithdrawalHistory.objects.filter(
        status=WithdrawalHistory.Status.withdrawn
    ).prefetch_related("card", "card__profile", "card__profile__user")

    for withdrawal in qs:
        phone, gateway = withdrawal.card.profile.get_momo_account()
        withdraw_amount = Conversions.get_xof_from_usd(
            withdrawal.amount, is_withdrawal=True
        )

        if phone and gateway:
            txn = Transaction.objects.request(
                obj=withdrawal.card,
                name=withdrawal.card.profile.name,
                amount=withdraw_amount,
                phone=phone,
                gateway=gateway,
                initiator=withdrawal.card.profile.user,
                txn_type=TransactionType.payout,
            )
            if txn.status == TransactionStatusEnum.success.value:
                withdrawal.status = WithdrawalHistory.Status.paid_out
                withdrawal.txn_ref = txn.reference
                withdrawal.save()


@shared_task
def retry_failed_funding():
    from kash.card.models import FundingHistory

    qs = FundingHistory.objects.filter(
        status=FundingHistory.FundingStatus.paid,
        retries__gte=1,
        retries__lt=FundingHistory.MAX_FUNDING_RETRIES,
        created_at__lte=now() - timedelta(minutes=5),
    ).prefetch_related("card", "card__profile")

    for item in qs:
        item.fund()


@shared_task
def reward_referrer():
    from kash.invite.models import Referral

    referrals = Referral.objects.annotate(
        referred_card_count=Count(
            "referred__virtualcard", filter=~Q(referred__virtualcard__external_id="")
        ),
    ).filter(referred_card_count__gte=1, rewarded_at__isnull=True)

    for referral in referrals:
        referral.reward()


@shared_task
def fetch_rave_rate():
    from kash.payout.models import Rate

    rates = rave_request("GET", f"/rates?from=USD&to=NGN&amount=1").json()
    ngn_amount = rates.get("data").get("to").get("amount")
    Rate.objects.get_or_create(
        code=Rate.Codes.rave_usd_ngn, defaults={"value": ngn_amount}
    )
