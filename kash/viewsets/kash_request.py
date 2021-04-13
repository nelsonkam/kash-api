from datetime import timedelta

from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.exceptions import Throttled
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.models import KashRequestResponse, KashTransaction, KashRequest, Notification
from kash.serializers.kash_request import KashRequestSerializer, KashRequestResponseSerializer


class KashRequestViewSet(ModelViewSet):
    serializer_class = KashRequestSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.request.user.profile.kash_requested.all()

    def perform_create(self, serializer):
        count = KashRequest.objects.filter(created_at__gte=now() - timedelta(hours=1), initiator=self.request.user.profile).count()
        if count > 5:
            notif = Notification.objects.create(
                title="Fait doucement oh 😩",
                description="Tu as déjà trop demander de kash dans les dernières heures, réessaies dans quelques heures. ",
                content_object=self.request.user.profile,
                profile=self.request.user.profile
            )
            notif.send()
            raise Throttled
        serializer.save(initiator=self.request.user.profile)

    @action(detail=True, methods=['post'])
    def accepted(self, request, pk=None):
        kash_request = get_object_or_404(KashRequest, pk=pk)
        response = KashRequestResponse.objects.create(
            sender=request.user.profile,
            request=kash_request,
            accepted=True,
            transaction=KashTransaction.objects.get(pk=request.data.get("transaction_id"))
        )
        return Response(KashRequestResponseSerializer(response).data)

    @action(detail=True, methods=['post'])
    def rejected(self, request, pk=None):
        kash_request = get_object_or_404(KashRequest, pk=pk)
        response = KashRequestResponse.objects.create(
            sender=request.user.profile,
            request=kash_request,
            accepted=False,
        )
        return Response(KashRequestResponseSerializer(response).data)
