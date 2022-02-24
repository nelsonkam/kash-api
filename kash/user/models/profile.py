from decimal import Decimal

from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.functional import cached_property

from kash.abstract.models import BaseModel, generate_ref_id
from kash.xlib.rest.validators import KashtagValidator


def generate_code():
    return generate_ref_id(length=5)


class UserProfile(BaseModel):
    user = models.OneToOneField(
        "kash_user.User", on_delete=models.CASCADE, related_name="profile"
    )
    kashtag = models.CharField(
        max_length=30, unique=True, validators=[KashtagValidator, MinLengthValidator(3)]
    )
    device_ids = ArrayField(models.CharField(max_length=255), default=list)
    avatar_url = models.URLField(blank=True)
    contacts = models.ManyToManyField("kash_user.UserProfile")
    referral_code = models.CharField(max_length=10, default=generate_code, unique=True)
    promo_balance = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "kash_userprofile"

    def push_notify(self, title, description, obj=None):
        from kash.notification.models import Notification

        notify = Notification.objects.create(
            title=title,
            description=description,
            content_object=obj,
            profile=self,
        )
        notify.send()

    @cached_property
    def name(self):
        return self.user.name

    @cached_property
    def phone_number(self):
        return self.user.phone_number

    @property
    def txn_summary(self):

        return {"30-days": {"sent": 0, "received": 0}}

    @property
    def kyc_level(self):
        return 2 if self.kycdocument_set.filter(status="approved").exists() else 1

    @property
    def limits(self):
        xof_amount = self.wallet.xof_amount.amount
        withdrawal_fees = max(100, round(xof_amount * Decimal(0.02)))
        return {
            "sendkash": {"min": 25, "max": max(self.wallet.xof_amount.amount - 25, 0)},
            "deposit": {"min": 25, "max": 500000},
            "withdraw": {"min": 0, "max": xof_amount},
            "purchase-card": {
                "min": 5,
                "max": 1000,
            },
            "fund-card": {"min": 5, "max": 1000},
        }

    def get_momo_account(self):
        from kash.transaction.models import Transaction

        payout_method = self.momo_accounts.first()
        if payout_method:
            return payout_method.phone, payout_method.gateway
        elif Transaction.objects.filter(
            initiator_id=self.user_id, status="success"
        ).exists():
            txn = Transaction.objects.filter(
                initiator=self.user, status="success"
            ).last()
            return txn.phone, txn.gateway
        else:
            raise Exception("User hasn't defined a momo account.")

    def __str__(self):
        return f"${self.kashtag}"


