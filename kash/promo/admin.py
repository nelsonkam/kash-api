from django.contrib import admin
from .models import PromoCode


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'value', 'expires_at', 'is_valid')
    readonly_fields = ('applied_to',)


admin.site.register(PromoCode, PromoCodeAdmin)
