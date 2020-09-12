from rest_framework import routers

from shop_admin.viewsets import ShopViewSet, ProductViewSet

router = routers.SimpleRouter()
router.register(r"shops", ShopViewSet, basename="shop")
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = router.urls
