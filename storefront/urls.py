from django.urls import path, include
from rest_framework import routers

from storefront import views
from storefront.viewsets import CartViewSet, CheckoutViewSet, CategoryViewSet, ShopViewSet, ProductViewSet

router = routers.SimpleRouter()
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"checkout", CheckoutViewSet, basename="checkout")
# router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"shops", ShopViewSet, basename="shop")
# router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.index),
    path("about/", views.ShopTemplateView.as_view(template_name="storefront/about.html")),
    path("legal/return-policy/", views.ShopTemplateView.as_view(template_name="storefront/legal_return.html")),
    path("legal/privacy-policy/", views.ShopTemplateView.as_view(template_name="storefront/legal_privacy.html")),
    path("legal/terms/", views.ShopTemplateView.as_view(template_name="storefront/legal_terms.html")),
    path("products/", views.product_catalogue),
    path("products/<slug>/", views.product_details),
    path("categories/<slug>/", views.category),
    path("order/<checkout_uid>/confirmed/", views.order_confirmation)
]

handler404 = 'storefront.views.handle_404'
