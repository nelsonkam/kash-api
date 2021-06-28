from django.contrib import admin
from .models import KYCDocument

class KYCDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'name', 'profile')
    readonly_fields = ('document_img', 'selfie_img', 'profile')



# Register your models here.
admin.site.register(KYCDocument, KYCDocumentAdmin)
