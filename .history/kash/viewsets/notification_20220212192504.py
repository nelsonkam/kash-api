from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.serializers.notification import NotificationSerializer
from kash.models import Notification
from .base import BaseViewSet


class NotificationViewset(BaseViewSet):
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = NotificationSerializer

    ordering = ["-created_at"]

    def get_queryset(self):
        return Notification.objects.filter(profile=self.request.profile)

    def get_paginated_response(self, data):
        return super().get_paginated_response(data)
