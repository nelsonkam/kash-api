from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.serializers.kash_request import KashRequestSerializer


class KashRequestViewSet(ModelViewSet):
    serializer_class = KashRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.request.user.profile.kash_requested.all()

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user.profile)
