from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.serializers.notification import NotificationSerializer


class NotificationViewset(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.request.user.profile.notifications.all().order_by("-created_at")[:1]
