from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.pagination import KashPagination
from kash.serializers.kash_transaction import KashTransactionSerializer


class KashTransactionViewSet(ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = KashTransactionSerializer
    pagination_class = KashPagination

    def get_queryset(self):
        return self.request.user.profile.kashtransaction_set.all().order_by("-timestamp")

