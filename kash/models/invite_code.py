from django.utils.timezone import now
from djmoney.money import Money
from rest_framework.exceptions import ValidationError
from kash.models.transaction import Transaction
from django.db import models, transaction


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
        code = referral_code.split("REF-")[1] if "REF-" in referral_code else referral_code

        referrer = UserProfile.objects.get(referral_code=code)

        if Referral.objects.filter(referred=profile).exists():
            raise ValidationError(dict(message="Already invited"))

        return Referral.objects.create(
            referrer=referrer,
            referred=profile,
        )


class Referral(BaseModel):
    REWARD_AMOUNT = 500
    referred = models.OneToOneField('kash.UserProfile', on_delete=models.CASCADE)
    referrer = models.ForeignKey("kash.UserProfile", on_delete=models.CASCADE, related_name='referrals')
    rewarded_at = models.DateTimeField(null=True)

    objects = ReferralManager()

    def reward(self):
        from kash.models import UserProfile
        with transaction.atomic():
            profile = UserProfile.objects.select_for_update().filter(pk=self.referrer.pk).first()
            profile.promo_balance += self.REWARD_AMOUNT
            profile.save()
            self.rewarded_at = now()
            self.save()

        self.referrer.push_notify(
            "Nouvelle affiliation 💰",
            f"Vous venez de gagner {self.REWARD_AMOUNT} XOF pour avoir recommander Kash à une connaissance.",
            self
        )