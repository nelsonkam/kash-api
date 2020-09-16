from uuid import uuid4

from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response

from affiliates.serializers import AffiliateAgentSerializer
from affiliates.viewsets.base import AffiliatesBaseModelViewSet
from core.models import AffiliateAgent
from core.utils import upload_content_file


class AffiliateAgentViewSet(AffiliatesBaseModelViewSet):
    serializer_class = AffiliateAgentSerializer
    parser_classes = [JSONParser, MultiPartParser]

    def get_queryset(self):
        return AffiliateAgent.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def avatar(self, request, pk=None):
        agent = self.get_object()
        image = request.data['avatar']
        agent.avatar_url = upload_content_file(image, f"{uuid4()}-{image.name}")
        agent.save()
        return Response(self.get_serializer(instance=agent).data)
