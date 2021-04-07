from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.serializers.payout_method import PayoutMethodSerializer


class PayoutMethodViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PayoutMethodSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.request.user.profile.payout_methods.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)
