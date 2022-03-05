from uuid import uuid4

from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kash.abstract.viewsets import BaseViewSet
from kash.kyc.models import KYCDocument
from kash.kyc.serializers import KYCDocumentSerializer
from kash.xlib.utils import upload_content_file


class KYCDocumentViewSet(BaseViewSet):
    serializer_class = KYCDocumentSerializer
    permission_classes = [IsAuthenticated]
    ordering = ["-created_at"]

    def get_queryset(self):
        return KYCDocument.objects.filter(profile=self.request.profile)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.profile)

    @action(detail=True, methods=["post"])
    def document(self, request, pk=None):
        kyc_doc = self.get_object()
        doc_image = request.data.get("document")
        selfie = request.data.get("selfie")
        if not doc_image or not selfie:
            raise ValidationError("A document image and selfie is required.")
        kyc_doc.doc_url = upload_content_file(doc_image, f"{uuid4()}-{doc_image.name or 'doc.jpg'}", "private")
        kyc_doc.selfie_url = upload_content_file(selfie, f"{uuid4()}-{selfie.name or 'selfie.jpg'}", "private")
        kyc_doc.save()
        return Response(self.get_serializer(instance=kyc_doc).data)
