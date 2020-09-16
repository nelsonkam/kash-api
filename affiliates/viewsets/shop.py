from affiliates.serializers import ShopSerializer
from affiliates.viewsets.base import AffiliatesBaseModelViewSet


class ShopViewSet(AffiliatesBaseModelViewSet):
    serializer_class = ShopSerializer

    def get_queryset(self):
        return self.request.user.affiliate.shops.all()


