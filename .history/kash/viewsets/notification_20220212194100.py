from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.serializers.notification import NotificationSerializer
from kash.models import Notification
from .base import BaseViewSet


class CustomPagination(LimitOffsetPagination):
    default_limit = 50

    def get_paginated_response(self, data):
        return Response(data)


class NotificationViewset(BaseViewSet):
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = NotificationSerializer
    pagination_class = CustomPagination
    ordering = ["-created_at"]

    def get_queryset(self):
        return Notification.objects.filter(profile=self.request.profile)