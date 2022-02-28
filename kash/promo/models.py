from django.db import models, transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from kash.abstract.models import BaseModel


class PromoCode(BaseModel):
    code = models.CharField(max_length=10, unique=True)
    value = models.PositiveIntegerField()
    expires_at = models.DateTimeField(null=True)
    is_valid = models.BooleanField(default=True)
    applied_to = models.ManyToManyField("kash_user.UserProfile")

    class Meta:
        db_table = 'kash_promocode'

    @property
    def appliable(self):
        return timezone.now() < self.expires_at and self.is_valid

    def apply(self, profile):
        from kash.user.models import UserProfile

        if not self.appliable:
            raise ValidationError({"code": "Code not applicable"})

        if self.applied_to.filter(pk=profile.pk).exists():
            raise ValidationError({"code": "Code already applied"})

        with transaction.atomic():
            profile = (
                UserProfile.objects.select_for_update().filter(pk=profile.pk).first()
            )
            profile.promo_balance += self.value
            profile.save()
            self.applied_to.add(profile)
