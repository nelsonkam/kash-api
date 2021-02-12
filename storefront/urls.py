from django.urls import path, include
from rest_framework import routers

from storefront import views
from storefront.viewsets import CartViewSet, CheckoutViewSet, CategoryViewSet, ShopViewSet, ProductViewSet

router = routers.SimpleRouter()
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"checkout", CheckoutViewSet, basename="checkout")
# router.register(r"categories", CategoryViewSet, basename="category")
# router.register(r"shops", ShopViewSet, basename="shop")
# router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.index),
    path("products/", views.product_catalogue),
    path("products/<slug>/", views.product_details)
]

handler404 = 'storefront.views.handle_404'
