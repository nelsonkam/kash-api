from rest_framework import routers

from affiliates.viewsets import AffiliateAgentViewSet

router = routers.SimpleRouter()
router.register(r"agents", AffiliateAgentViewSet, basename="agent")

urlpatterns = router.urls
