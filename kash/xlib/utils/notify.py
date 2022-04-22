from django.conf import settings
from slackclient import SlackClient
import telegram
from telegram import message
from hashids import Hashids
import requests
from djmoney.money import Money

from .payment import rave_request
from .utils import GATEWAY_LIST, CardActionType, Gateway

sc = SlackClient(settings.SLACK_TOKEN)


def notify_telegram(*args, **kwargs):
    if settings.DEBUG or settings.TESTING:
        print(kwargs.get("text"))
        return
    tg_bot = telegram.Bot(token=settings.TG_BOT_TOKEN)
    return tg_bot.send_message(*args, **kwargs)


def send():
    return sc.api_call(
        "chat.postMessage", channel="updates", text="Hello from Python! :tada:"
    )


def send_slack_message(**kwargs):
    return sc.api_call("chat.postMessage", **kwargs)


def notify_slack(message):
    return requests.post(settings.SLACK_WEBHOOK_URL, json=message)


def check_funding_status():
    ngn_balance = (
        rave_request("GET", "/balances/NGN").json().get("data").get("available_balance")
    )
    usd_balance = (
        rave_request("GET", "/balances/USD").json().get("data").get("available_balance")
    )
    data = rave_request("GET", f"/rates?from=NGN&to=USD&amount={ngn_balance}").json()
    amount = data.get("data").get("to").get("amount")
    return 1000 - (usd_balance + amount)


def parse_topup_command(chat_id, arg_list):
    from kash.payout.models import Topup

    tg_bot = telegram.Bot(token=settings.TG_BOT_TOKEN)

    if len(arg_list) == 2 and arg_list[0] == "start":
        topup = Topup.objects.create(amount=int(arg_list[1]))
        tg_bot.send_message(
            chat_id=chat_id,
            text=f"Topup (code: {topup.code}) of USD {topup.amount} started.",
        )
        return

    # /topup pay REFID camille-mtn
    if len(arg_list) == 3 and arg_list[0] == "pay":
        code = arg_list[1]
        recipient = arg_list[2]
        recipient_info = settings.PAYOUT_RECIPIENTS[recipient]
        topup = Topup.objects.get(code=code)
        txn = topup.payout_xof(
            recipient_info.get("phone"), recipient_info.get("gateway")
        )
        tg_bot.send_message(
            chat_id=chat_id,
            text=f"Payout of {txn.amount} paid to {recipient} with status: {txn.status}.",
        )
        return

    if len(arg_list) == 2 and arg_list[0] == "cancel":
        code = arg_list[1]
        topup = Topup.objects.get(code=code)
        topup.is_canceled = True
        topup.save()
        tg_bot.send_message(
            chat_id=chat_id,
            text=f"Topup {code} canceled.",
        )
        return


def parse_card_command(chat_id, arg_list):
    from kash.card.models import VirtualCard
    from kash.payout.models import CardAction

    tg_bot = telegram.Bot(token=settings.TG_BOT_TOKEN)

    if len(arg_list) == 2 and arg_list[0] == "find":
        last_4 = arg_list[1]
        cards = VirtualCard.objects.filter(last_4=last_4)
        text = [
            f"- {card.id} - {card.nickname} ({'active' if card.is_active else 'inactive'})"
            for card in cards
        ]
        tg_bot.send_message(
            chat_id=chat_id,
            text=f"Cards found:\n." + "\n".join(text),
        )

    # /card credit ID amount
    if len(arg_list) == 3 and arg_list[0] == "credit":
        card_id = arg_list[1]
        card = VirtualCard.objects.get(pk=card_id)
        amount = arg_list[2]
        action = CardAction.objects.create(
            amount=int(amount),
            action_type=CardActionType.funding,
            card=card
        )
        tg_bot.send_message(
            chat_id=chat_id,
            text=f"Are you sure you want to fund {card.nickname} ·{card.last_4} ({'active' if card.is_active else 'inactive'}) with USD {amount}?\nConfirmation code: {action.code}",
        )

    # /card debit ID amount
    if len(arg_list) == 3 and arg_list[0] == "debit":
        card_id = arg_list[1]
        card = VirtualCard.objects.get(pk=card_id)
        amount = arg_list[2]
        action = CardAction.objects.create(
            amount=int(amount),
            action_type=CardActionType.withdrawal,
            card=card
        )
        tg_bot.send_message(
            chat_id=chat_id,
            text=f"Are you sure you want to debit {card.nickname} ·{card.last_4} ({'active' if card.is_active else 'inactive'}) with USD {amount}?\nConfirmation code: {action.code}",
        )

    if len(arg_list) == 2 and arg_list[0] == "confirm":
        code = arg_list[1]
        action = CardAction.objects.get(code=code, is_confirmed=False)
        action.is_confirmed = True
        action.save()
        card = action.card
        if action.action_type == CardActionType.funding:
            card.provider.fund(card, Money(action.amount, "USD"))
            tg_bot.send_message(
                chat_id=chat_id,
                text=f"Cards credited.",
            )
        elif action.action_type == CardActionType.withdrawal:
            card.provider.withdraw(card, Money(action.amount, "USD"))
            tg_bot.send_message(
                chat_id=chat_id,
                text=f"Cards debited.",
            )

    


def parse_command(data):
    from kash.payout.models import AdminPayoutRequest

    tg_bot = telegram.Bot(token=settings.TG_BOT_TOKEN)

    try:
        update = telegram.Update.de_json(data, tg_bot)
        if not update.message:
            return
        chat_id = str(update.message.chat.id)
        if chat_id != settings.TG_CHAT_ID:
            tg_bot.send_message(
                chat_id=chat_id,
                text="You do not have the necessary permissions to communicate with Jarvis.",
            )
            return
        text = update.message.text.encode("utf-8").decode()

        if text.startswith("/status"):
            command = text.split(" ")
            if len(command) == 2:
                if command[1] == "funding":
                    tg_bot.send_message(
                        chat_id=chat_id,
                        text=f"You have to fund the account by ${check_funding_status()}",
                    )
                    return

        if text.startswith("/recipients"):
            recipient_list = "\n".join(
                [
                    f'{key} - {value.get("phone")}'
                    for key, value in settings.PAYOUT_RECIPIENTS.items()
                ]
            )
            tg_bot.send_message(
                chat_id=chat_id,
                text=f"Here's the list of recipients:\n{recipient_list}",
            )
            return
        if text.startswith("/send"):
            command = text.split(" ")
            if len(command) == 4:
                recipient = command[3]
                amount = command[1]
                recipient_info = settings.PAYOUT_RECIPIENTS[recipient]
                request = AdminPayoutRequest.objects.create(
                    amount=int(amount),
                    phone=recipient_info.get("phone"),
                    gateway=recipient_info.get("gateway"),
                )
                tg_bot.send_message(
                    chat_id=chat_id,
                    text=f"Are you sure you want to send {amount} to {recipient} ({recipient_info.get('phone')})?\nConfirmation code is: {request.code}",
                )

                return

        if text.startswith("/confirm"):
            command = text.split(" ")
            if len(command) == 2:
                code = command[1]
                request = AdminPayoutRequest.objects.get(code=code)
                request.execute()
                return
        tg_bot.send_message(chat_id=chat_id, text="I couldn't quite get that message.")

        if text.startswith("/topup") or text.startswith("/top"):
            commands = text.split(" ")[1:]
            parse_topup_command(chat_id, commands)

        if text.startswith("/card"):
            commands = text.split(" ")[1:]
            parse_card_command(chat_id, commands)

    except Exception as err:
        tg_bot.send_message(chat_id=chat_id, text=str(err))
 