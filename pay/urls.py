from django.urls import path
from rest_framework.routers import SimpleRouter

from pay.viewsets.session import CheckoutSessionViewset
from storefront.viewsets import ShopViewSet

router = SimpleRouter()
router.register("sessions", CheckoutSessionViewset, "checkout-session")
router.register("shops", ShopViewSet, "shops")

urlpatterns = router.urls
