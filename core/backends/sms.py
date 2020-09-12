import boto3
from django.conf import settings
from phone_verify.backends.base import BaseBackend


class ConsoleSMSBackend(BaseBackend):
    def send_sms(self, number, message):
        print(f"SMS to {number}: {message}")

    def send_bulk_sms(self, numbers, message):
        for number in numbers:
            self.send_sms(number, message)


class AmazonSMSBackend(BaseBackend):

    def send_sms(self, number, message):
        client = boto3.client(
            "sns",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME,
        )
        client.publish(PhoneNumber=number, Message=message)

    def send_bulk_sms(self, numbers, message):
        for number in numbers:
            self.send_sms(number, message)
