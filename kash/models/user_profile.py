import re

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.postgres.fields import ArrayField
from django.core import validators
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _

from core.models.base import BaseModel


@deconstructible
class KashtagValidator(validators.RegexValidator):
    regex = r'^[\w]+\Z'
    message = _(
        'Enter a valid kashtag. This value may contain only English letters, '
        'numbers, and _ characters.'
    )
    flags = re.ASCII


class UserProfile(BaseModel):
    user = models.OneToOneField('core.User', on_delete=models.CASCADE, related_name='profile')
    kashtag = models.CharField(max_length=30, unique=True, validators=[KashtagValidator, MinLengthValidator(3)])
    device_ids = ArrayField(models.CharField(max_length=255), default=list)

    @property
    def name(self):
        return self.user.name
