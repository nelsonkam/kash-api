from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.serializers.transaction import TransactionSerializer


class TransactionViewSet(ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    lookup_field = 'reference'

    def get_queryset(self):
        return self.request.user.transaction_set.all()

