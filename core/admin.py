from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from core.models import User

admin.register(User, UserAdmin)
