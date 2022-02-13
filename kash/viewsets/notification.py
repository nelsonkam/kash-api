from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.serializers.notification import NotificationSerializer
from kash.models import Notification
from kash.pagination import KashPagination
from .base import BaseViewSet


class NotificationViewset(BaseViewSet):
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = NotificationSerializer
    pagination_class = KashPagination
    ordering = ["-created_at"]

    def get_queryset(self):
        return Notification.objects.only(
            "id", "description", "created_at", "title"
        ).filter(profile=self.request.profile)
