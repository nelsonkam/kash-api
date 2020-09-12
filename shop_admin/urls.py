from rest_framework import routers

from shop_admin.viewsets import ShopViewSet, ProductViewSet, ProductImageViewSet

router = routers.SimpleRouter()
router.register(r"shops", ShopViewSet, basename="shop")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"product_images", ProductImageViewSet, basename="product_image")

urlpatterns = router.urls
