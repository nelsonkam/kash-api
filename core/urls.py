from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from core import views
from core.viewsets import auth

router = routers.SimpleRouter()
router.register(r"phone", auth.Verification, basename="phone")

urlpatterns = router.urls + [
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("upload/", views.upload, name="upload"),
    path("user/current/", views.user_current, name="user_current"),
    path("setup_fee/", views.setup_fee, name="setup_fee"),
]
