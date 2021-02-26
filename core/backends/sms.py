from abc import ABC

import boto3
from django.conf import settings
from phone_verify.backends.base import BaseBackend
from phone_verify.models import SMSVerification


class BaseSMSBackend(BaseBackend, ABC):
    def create_security_code_and_session_token(self, number):
        if number in settings.PHONE_VERIFICATION.get("TEST_PHONE_NUMBERS"):
            security_code = "123456"
        else:
            security_code = self.generate_security_code()

        session_token = self.generate_session_token(number)

        # Delete old security_code(s) for phone_number if already exists
        SMSVerification.objects.filter(phone_number=number).delete()

        # Default security_code generated of 6 digits
        SMSVerification.objects.create(
            phone_number=number,
            security_code=security_code,
            session_token=session_token,
        )
        return security_code, session_token


class ConsoleSMSBackend(BaseSMSBackend):
    def send_sms(self, number, message):
        print(f"SMS to {number}: {message}")

    def send_bulk_sms(self, numbers, message):
        for number in numbers:
            self.send_sms(number, message)


class AmazonSMSBackend(BaseSMSBackend):

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
