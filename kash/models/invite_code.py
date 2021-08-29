from django.utils.timezone import now
from djmoney.money import Money
from rest_framework.exceptions import ValidationError
from kash.models.transaction import Transaction
from django.db import models


from core.models.base import BaseModel, generate_ref_id
from kash.utils import TransactionType, generate_reference


def generate_code():
    return generate_ref_id(length=4)


class InviteCode(BaseModel):
    inviter = models.ForeignKey('kash.UserProfile', on_delete=models.CASCADE, related_name='invite_codes')
    code = models.CharField(max_length=10, default=generate_code, unique=True)
    used_at = models.DateTimeField(null=True)
    invited = models.OneToOneField('kash.UserProfile', on_delete=models.CASCADE, null=True, related_name='invite')


class ReferralManager(models.Manager):
    def record_referral(self, profile, referral_code):
        from kash.models import UserProfile

        print(profile, referral_code)

        referrer = UserProfile.objects.get(referral_code=referral_code.split("REF-")[1])

        if Referral.objects.filter(referred=profile).exists():
            raise ValidationError(dict(message="Already invited"))

        return Referral.objects.create(
            referrer=referrer,
            referred=profile,
        )


class Referral(BaseModel):
    referred = models.OneToOneField('kash.UserProfile', on_delete=models.CASCADE)
    referrer = models.ForeignKey("kash.UserProfile", on_delete=models.CASCADE, related_name='referrals')
    rewarded_at = models.DateTimeField(null=True)
    reward_reference = models.CharField(max_length=20, blank=True)

    objects = ReferralManager()

    def reward(self):
        phone, gateway = self.referrer.get_momo_account()
        txn = Transaction.objects.request(
            name=self.referrer.name,
            phone=phone,
            gateway=gateway,
            amount=Money(250, "XOF"),
            initiator=self.referrer.user,
            txn_type=TransactionType.payout
        )

        self.rewarded_at = now()
        self.reward_reference = txn.reference
        self.save()

        self.referrer.push_notify(
            "Nouvelle affiliation 💰",
            "Vous venez de gagner 250 XOF pour avoir recommander Kash à une connaissance.",
            self
        )