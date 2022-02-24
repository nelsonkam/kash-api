from django.utils.timezone import now
from django.db import models, transaction

from kash.abstract.models import BaseModel, generate_ref_id


def generate_code():
    return generate_ref_id(length=4)


class InviteCode(BaseModel):
    inviter = models.ForeignKey(
        "kash_user.UserProfile", on_delete=models.CASCADE, related_name="invite_codes"
    )
    code = models.CharField(max_length=10, default=generate_code, unique=True)
    used_at = models.DateTimeField(null=True)
    invited = models.OneToOneField(
        "kash_user.UserProfile", on_delete=models.CASCADE, null=True, related_name="invite"
    )


class ReferralManager(models.Manager):
    def record_referral(self, profile, referral_code):
        from kash.user.models import UserProfile

        code = (
            referral_code.split("REF-")[1] if "REF-" in referral_code else referral_code
        )

        referrer = UserProfile.objects.filter(referral_code=code).first()

        if not referrer or Referral.objects.filter(referred=profile).exists():
            return None

        return Referral.objects.create(
            referrer=referrer,
            referred=profile,
        )


class Referral(BaseModel):
    REWARD_AMOUNT = 500
    referred = models.OneToOneField("kash_user.UserProfile", on_delete=models.CASCADE)
    referrer = models.ForeignKey(
        "kash_user.UserProfile", on_delete=models.CASCADE, related_name="referrals"
    )
    rewarded_at = models.DateTimeField(null=True)

    objects = ReferralManager()

    def reward(self):
        from kash.user.models import UserProfile

        with transaction.atomic():
            profile = (
                UserProfile.objects.select_for_update()
                .filter(pk=self.referrer.pk)
                .first()
            )
            profile.promo_balance += self.REWARD_AMOUNT
            profile.save()
            self.rewarded_at = now()
            self.save()
            self.referrer.push_notify(
                "Nouvelle affiliation 💰",
                f"Vous venez de gagner {self.REWARD_AMOUNT} XOF pour avoir recommander Kash à une connaissance.",
                self,
            )
