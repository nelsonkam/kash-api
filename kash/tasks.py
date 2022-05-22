from datetime import timedelta
from decimal import Decimal

from celery import shared_task
from django.conf import settings
from django.db.models import Q, Avg
from django.db.models.aggregates import Count
from django.utils import timezone
from djmoney.money import Money

from kash.card.providers import RaveCardProvider
from kash.xlib.utils.notify import notify_telegram, notify_slack, send_slack_message
from kash.xlib.utils.payment import rave_request
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
        created__gte=timezone.now() - timedelta(minutes=15),
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
    if not provider.is_balance_sufficient(Money(100, "USD")):
        notify_slack(
            {
                "text": f"⚠️ Le compte Flutterwave est déchargé! (Solde: *${usd_balance}*) cc <@U022FUW39FT>"
            }
        )
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
        created_at__lte=timezone.now() - timedelta(minutes=5),
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


@shared_task
def compute_metrics():
    from kash.user.models import UserProfile
    from kash.card.models import VirtualCard, FundingHistory
    from kash.transaction.models import Transaction

    seven_days_ago = timezone.now().date() - timezone.timedelta(days=7)
    signups = UserProfile.objects.filter(created_at__gte=seven_days_ago).count()
    cards = VirtualCard.objects.filter(created_at__gte=seven_days_ago).exclude(
        external_id=""
    )
    cards_created = cards.count()
    unique_card_creators = cards.distinct("profile").count()
    txns = Transaction.objects.filter(
        created__gte=seven_days_ago, status=TransactionStatus.success
    ).exclude(name="admin")
    active_transactors = txns.distinct("initiator").count()
    payment_count = txns.filter(transaction_type=TransactionType.payment).count()
    payout_count = txns.filter(transaction_type=TransactionType.payout).count()
    refund_count = txns.filter(
        created__gte=seven_days_ago, status=TransactionStatus.refunded
    ).count()
    avg_funding_amt = (
        FundingHistory.objects.filter(
            created_at__gte=seven_days_ago, status=TransactionStatus.success
        )
        .aggregate(Avg("amount"))
        .get("amount__avg")
    )

    send_slack_message(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Chiffres sur les *7 derniers jours*.",
                },
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Inscriptions:*\n {signups}"},
                    {
                        "type": "mrkdwn",
                        "text": f"*Utilisateurs actifs:*\n{active_transactors}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Nbres de cartes créées:*\n{cards_created} cartes ({unique_card_creators} utilisateurs)",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Montant de recharge moyen:*\n${round(avg_funding_amt, 2)}",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Nombres de transactions:*\n{payment_count} paiements - {payout_count} retraits - {refund_count} remboursements",
                    },
                ],
            },
        ],
        channel="C02208FUPRT" if settings.IS_PROD else "C036GNEM98Q",
    )


def deactivate_deleted_rave_card():
    from kash.card.models import VirtualCard

    cards = (
        VirtualCard.objects.exclude(external_id="")
        .filter(
            is_active=True, provider_name="rave", is_permablocked=False, pk__gte=915
        )
        .order_by("created_at")
    )

    for card in cards:
        try:
            details = card.card_details
            print(f"Card #{card.pk} valid.")
        except Exception as err:
            print(err)
            if "not found" in str(err).lower() or "unable to get" in str(err).lower():
                print(f"Card #{card.pk} permablocked: {err}")
                card.is_permablocked = True
                card.permablock_reason = "Rave VISA to MasterCard migration"
                card.save()


@shared_task
def topup_usd_balance():
    from kash.payout.models import Topup

    resp = rave_request(
        "GET", "/balances/NGN", secret_key=settings.NK_RAVE_SECRET_KEY
    ).json()
    balance = resp.get("data").get("available_balance")
    if balance < 10000:
        return

    notify_telegram(
        chat_id=settings.TG_CHAT_ID,
        text=f"Found NGN {balance} on FLW account, topping up Futurix account if there is a pending top up.",
    )
    topup = Topup.objects.filter(
        ngn_payin_status=TransactionStatus.pending,
        created_at__gte=timezone.now() - timezone.timedelta(hours=6),
        is_canceled=False,
    ).last()

    if not topup:
        notify_telegram(
            chat_id=settings.TG_CHAT_ID,
            text=f"No pending top up found. Aborting...",
        )
        return

    topup.ngn_payin_status = TransactionStatus.success
    topup.save()
    resp = rave_request(
        "GET",
        f"/rates?from=USD&to=NGN&amount=1",
        secret_key=settings.NK_RAVE_SECRET_KEY,
    ).json()
    rate = resp.get("data").get("to").get("amount")
    amount_to_send = round(Decimal(balance) / Decimal(rate), 2)

    payload = {
        "account_bank": "flutterwave",
        "account_number": "00717603",
        "amount": int(amount_to_send),
        "currency": "USD",
        "debit_currency": "NGN",
    }
    resp = rave_request(
        "POST", "/transfers", data=payload, secret_key=settings.NK_RAVE_SECRET_KEY
    ).json()
    topup.usd_txn_status = TransactionStatus.success
    topup.save()
    notify_telegram(
        chat_id=settings.TG_CHAT_ID,
        text=f"Futurix account topped up by ${int(amount_to_send)}.",
    )
    recipient_info = settings.PAYOUT_RECIPIENTS["camille-mtn"]
    txn = topup.payout_xof(recipient_info.get("phone"), recipient_info.get("gateway"))
    notify_telegram(
        chat_id=settings.TG_CHAT_ID,
        text=f"Payout of {txn.amount} paid to camille-mtn with status: {txn.status}.",
    )

# @shared_task
def create_refund_history():
    from kash.card.models import VirtualCard, RefundHistory
    qs = VirtualCard.objects.exclude(external_id='').filter(refund__isnull=True, is_active=True, is_permablocked=False)
    print(qs.count())
    for card in qs:
        try:
            print(card.external_id, card.id)
            RefundHistory.objects.create(
                card=card,
                card_balance=Money(card.card_details.get("amount"), "USD")
            )
        except Exception as err:
            print(err)
            if "not found" in str(err).lower() or "unable to get" in str(err).lower():
                print(f"Card #{card.pk} permablocked: {err}")
                card.is_permablocked = True
                card.permablock_reason = "unknown"
                card.save()