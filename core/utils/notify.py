from django.conf import settings
from slackclient import SlackClient
import telegram

sc = SlackClient(settings.SLACK_TOKEN)
tg_bot = telegram.Bot(token=settings.TG_BOT_TOKEN)


def send():
    return sc.api_call(
        "chat.postMessage", channel="updates", text="Hello from Python! :tada:"
    )


def send_message(attachments, channel):
    return sc.api_call("chat.postMessage", channel=channel, attachments=attachments)
