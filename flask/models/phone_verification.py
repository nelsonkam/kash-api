import secrets
import string

from app import db
from utils.sms import send_sms


class PhoneVerification(db.Model):
    @classmethod
    def generate_security_code(cls, length=6):
        return "".join(secrets.choice(string.digits) for i in range(length))

    @classmethod
    def send_verification_code(cls, phone_number):
        verification = cls()
        verification.phone_number = phone_number
        verification.security_code = cls.generate_security_code()
        verification.session_token = secrets.token_hex()

        verification.save()
        verification.send()
        return verification

    @classmethod
    def verify(cls, phone_number, security_code, session_token):
        verification = (
            cls.where("phone_number", phone_number)
            .where("security_code", security_code)
            .where("session_token", session_token)
            .first()
        )
        if verification and not verification.is_verified and not verification.is_expired():
            verification.is_verified = True
            verification.save()
            return True

        return False

    def is_expired(self):
        return False

    def send(self):
        send_sms(
            self.phone_number,
            f"Votre code de verification pour Kweek est: {self.security_code}",
        )
