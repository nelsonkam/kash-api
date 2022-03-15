from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet

from kash.auth.models import VerificationMethod
from kash.kyc.models import KYCDocument
from kash.user.models import User, UserProfile


class RemoteConfigViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]

    def perform_authentication(self, request):
        super().perform_authentication(request)
        if isinstance(self.request.user, User):
            self.request.profile = UserProfile.objects.get(user=self.request.user)

    @action(detail=False, methods=['get'])
    def cards(self, request):
        has_kyc_doc_approved = KYCDocument.objects.filter(status="approved", profile=request.profile).exists()
        has_valid_verification_method = VerificationMethod.objects.filter(
            profile=request.profile, is_verified=True
        ).exists()
        return Response({'can_create_card': has_kyc_doc_approved and has_valid_verification_method})
