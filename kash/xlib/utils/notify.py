from django.conf import settings
from slackclient import SlackClient
import telegram
from telegram import message
from hashids import Hashids

from .payment import rave_request
from .utils import GATEWAY_LIST, Gateway

sc = SlackClient(settings.SLACK_TOKEN)
tg_bot = telegram.Bot(token=settings.TG_BOT_TOKEN)


def notify_telegram(*args, **kwargs):
    if settings.DEBUG or settings.TESTING:
        print(kwargs.get("text"))
        return
    return tg_bot.send_message(*args, **kwargs)


def send():
    return sc.api_call(
        "chat.postMessage", channel="updates", text="Hello from Python! :tada:"
    )


def send_message(attachments, channel):
    return sc.api_call("chat.postMessage", channel=channel, attachments=attachments)


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


def parse_command(data):
    from kash.models import AdminPayoutRequest

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
    except Exception as err:
        tg_bot.send_message(chat_id=chat_id, text=str(err))
