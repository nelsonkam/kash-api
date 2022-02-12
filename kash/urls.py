from django.conf import settings
from django.urls import path
from rest_framework_nested import routers

from kash import views
from kash.viewsets.auth import AuthViewSet
from kash.viewsets.invite_code import InviteCodeViewset
from kash.viewsets.kash_request import KashRequestViewSet
from kash.viewsets.kyc_document import KYCDocumentViewSet
from kash.viewsets.notification import NotificationViewset
from kash.viewsets.payout_method import MomoAccountViewset
from kash.viewsets.profile import ProfileViewset
from kash.viewsets.transaction import QosicTransactionViewSet, StellarTransactionViewSet
from kash.viewsets.virtual_card import VirtualCardViewSet
from kash.viewsets.wallet import WalletViewSet

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
    path("rates/", views.rates, name="rates"),
    path("info/cards/", views.card_info, name="card_info"),
    path("misc/fund/", views.recharge, name="misc_fund"),
    path(f"tgbot/{settings.TG_BOT_TOKEN}/", views.tg_bot, name="tg_bot"),
]
