from rest_framework.permissions import IsAuthenticated

from kash.notification.serializers import NotificationSerializer
from kash.notification.models import Notification
from kash.xlib.rest.pagination import KashPagination
from kash.abstract.viewsets import BaseViewSet


class NotificationViewset(BaseViewSet):
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    pagination_class = KashPagination
    ordering = ["-created_at"]

    def get_queryset(self):
        return Notification.objects.only("id", "description", "created_at", "title").filter(
            profile=self.request.profile
        )
