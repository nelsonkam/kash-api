from django.conf import settings
from django.urls import path

from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenRefreshView

from kash import views
from kash.auth.viewsets import AuthViewSet
from kash.kyc.viewsets import KYCDocumentViewSet
from kash.notification.viewsets import NotificationViewset
from kash.user.viewsets import ProfileViewset
from kash.transaction.viewsets import QosicTransactionViewSet
from kash.card.viewsets import VirtualCardViewSet
from kash.invite.viewsets import InviteCodeViewset

router = routers.SimpleRouter()
router.register("profiles", ProfileViewset, "profiles")
router.register("virtual-cards", VirtualCardViewSet, "virtual-cards")
router.register("qosic-txn", QosicTransactionViewSet, "transaction")
router.register("notifications", NotificationViewset, "notifications")
router.register("invites", InviteCodeViewset, "invites")
router.register("kyc", KYCDocumentViewSet, "kyc")
router.register("auth", AuthViewSet, "auth")


urlpatterns = router.urls + [
    path("version/", views.version, name="version"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("rates/", views.rates, name="rates"),
    path("info/cards/", views.card_info, name="card_info"),
    path("misc/fund/", views.recharge, name="misc_fund"),
    path(f"tgbot/{settings.TG_BOT_TOKEN}/", views.tg_bot, name="tg_bot"),
]
