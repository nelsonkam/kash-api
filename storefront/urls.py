from rest_framework import routers

from storefront.viewsets import CartViewSet, CheckoutViewSet

router = routers.SimpleRouter()
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"checkout", CheckoutViewSet, basename="checkout")

urlpatterns = router.urls
