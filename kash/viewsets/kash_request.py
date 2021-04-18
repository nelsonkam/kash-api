from datetime import timedelta

from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.exceptions import Throttled
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.models import KashRequestResponse, SendKash, KashRequest, Notification
from kash.pagination import KashPagination
from kash.serializers.kash_request import KashRequestSerializer, KashRequestResponseSerializer


class KashRequestViewSet(ModelViewSet):
    serializer_class = KashRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = KashPagination

    def get_queryset(self):
        return self.request.user.profile.kash_requested.all().order_by("-created_at")

    def perform_create(self, serializer):
        count = KashRequest.objects.filter(created_at__gte=now() - timedelta(hours=1),
                                           initiator=self.request.user.profile).count()
        if count > 3:
            notif = Notification.objects.create(
                title="Fais doucement oh 😩",
                description="Tu as déjà trop demander de kash dans les dernières heures, réessaie dans quelques heures. ",
                content_object=self.request.user.profile,
                profile=self.request.user.profile
            )
            notif.send()
            raise Throttled
        serializer.save(initiator=self.request.user.profile)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        kash_request = get_object_or_404(KashRequest.objects.all(), pk=pk)
        txn = kash_request.accept(phone=request.data.get('phone'),
                         gateway=request.data.get('gateway'))
        return Response({'txn_ref': txn.reference})

    @action(detail=True, methods=['post'])
    def accepted(self, request, pk=None):
        kash_request = get_object_or_404(KashRequest.objects.all(), pk=pk)
        response = KashRequestResponse.objects.create(
            sender=request.user.profile,
            request=kash_request,
            accepted=True,
            transaction=SendKash.objects.get(pk=request.data.get("transaction_id"))
        )
        return Response(KashRequestResponseSerializer(response).data)

    @action(detail=True, methods=['post'])
    def rejected(self, request, pk=None):
        kash_request = get_object_or_404(KashRequest.objects.all(), pk=pk)
        response = KashRequestResponse.objects.create(
            sender=request.user.profile,
            request=kash_request,
            accepted=False,
        )
        return Response(KashRequestResponseSerializer(response).data)

    @action(detail=False, methods=['get'])
    def received(self, request):
        queryset = self.request.user.profile.kash_requests.all().order_by("-created_at")
        queryset = self.paginate_queryset(queryset)
        return self.get_paginated_response(self.get_serializer(queryset, many=True).data)
