from abc import ABC

import boto3
import messagebird
from django.conf import settings
from phone_verify.backends.base import BaseBackend
from phone_verify.models import SMSVerification
from rest_framework.exceptions import APIException


class SMSProviderException(APIException):
    default_code = "sms_provider_error"


class BaseSMSBackend(BaseBackend, ABC):
    def __init__(self, **options):
        super(BaseSMSBackend, self).__init__(**options)
        self.exception_class = Exception

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

    def send_bulk_sms(self, numbers, message):
        for number in numbers:
            self.send_sms(number, message)


class ConsoleSMSBackend(BaseSMSBackend):
    def send_sms(self, number, message):
        if len(number) > 15:
            raise SMSProviderException("number too long")
        print(f"SMS to {number}: {message}")


class MessageBirdSMSBackend(BaseSMSBackend):
    def __init__(self, **options):
        super(MessageBirdSMSBackend, self).__init__(**options)
        self.exception_class = messagebird.ErrorException

    def send_sms(self, number, message):
        try:
            client = messagebird.Client(settings.MESSAGEBIRD_ACCESS_KEY)
            return client.message_create("Kash", number, message, {"reference": "none"})
        except Exception as err:
            raise SMSProviderException(str(err))
