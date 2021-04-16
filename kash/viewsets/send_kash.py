from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.serializers.send_kash import SendKashSerializer


class SendKashViewSet(ModelViewSet):
    serializer_class = SendKashSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.request.user.profile.kash_transactions.all()

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user.profile)

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        send_kash = self.get_object()
        txn = send_kash.pay(phone=request.data.get("phone"), gateway=request.data.get('gateway'))
        return Response({'txn_ref': txn.reference})
