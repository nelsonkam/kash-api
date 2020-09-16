from rest_framework import routers

from affiliates.viewsets import AffiliateAgentViewSet, OrderViewSet, ShopViewSet

router = routers.SimpleRouter()
router.register(r"agents", AffiliateAgentViewSet, basename="agent")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"shops", ShopViewSet, basename="shop")

urlpatterns = router.urls
