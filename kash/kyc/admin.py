from django.contrib import admin
from .models import KYCDocument


class KYCDocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "name", "profile")
    readonly_fields = ("document_img", "selfie_img", "profile")


admin.site.register(KYCDocument, KYCDocumentAdmin)
