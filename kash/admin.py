from django.contrib import admin
from .models import KYCDocument, PromoCode

class KYCDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'name', 'profile')
    readonly_fields = ('document_img', 'selfie_img', 'profile')

class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'value', 'expires_at', 'is_valid')
    readonly_fields = ('applied_to',)


# Register your models here.
admin.site.register(KYCDocument, KYCDocumentAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
