import boto3
from flask import current_app as app
import config


def send_sms(phone_number, message):
    if app.debug:
        print(f"SMS for {phone_number}: {message}")
    else:
        client = boto3.client(
            "sns",
            aws_access_key_id=config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
            region_name=config.AWS_REGION_NAME,
        )
        client.publish(PhoneNumber=phone_number, Message=message)
