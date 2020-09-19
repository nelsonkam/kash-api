from django.conf import settings
from slackclient import SlackClient

sc = SlackClient(settings.SLACK_TOKEN)


def send():
    return sc.api_call(
        "chat.postMessage", channel="updates", text="Hello from Python! :tada:"
    )


def send_message(attachments, channel):
    return sc.api_call("chat.postMessage", channel=channel, attachments=attachments)
