from uuid import uuid4

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.utils import upload_content_file
from kash.serializers.kyc_document import KYCDocumentSerializer


class KYCDocumentViewSet(ModelViewSet):
    serializer_class = KYCDocumentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.profile.kycdocument_set.all().order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    @action(detail=True, methods=['post'])
    def document(self, request, pk=None):
        kyc_doc = self.get_object()
        image = request.data['document']
        kyc_doc.doc_url = upload_content_file(image, f"{uuid4()}-{image.name}", "private")
        kyc_doc.save()
        return Response(self.get_serializer(instance=kyc_doc).data)

    @action(detail=True, methods=['post'])
    def selfie(self, request, pk=None):
        kyc_doc = self.get_object()
        image = request.data['selfie']
        kyc_doc.selfie_url = upload_content_file(image, f"{uuid4()}-{image.name}", "private")
        kyc_doc.save()
        return Response(self.get_serializer(instance=kyc_doc).data)