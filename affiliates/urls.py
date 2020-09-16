from rest_framework import routers

from affiliates.viewsets import AffiliateAgentViewSet, OrderViewSet

router = routers.SimpleRouter()
router.register(r"agents", AffiliateAgentViewSet, basename="agent")
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = router.urls
