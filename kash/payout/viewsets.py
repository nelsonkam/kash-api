from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.payout.serializers import MomoAccountSerializer


class MomoAccountViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MomoAccountSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.request.user.profile.momo_accounts.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)
