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
router.register("momo-accounts", MomoAccountViewset, "momo-accounts")
router.register("requests", KashRequestViewSet, "request-kash")
router.register("notifications", NotificationViewset, "notifications")
router.register("invites", InviteCodeViewset, "invites")
router.register("kyc", KYCDocumentViewSet, "kyc")
router.register("auth", AuthViewSet, "auth")
router.register("wallets", WalletViewSet, "wallets")

wallets_router = routers.NestedSimpleRouter(router, 'wallets', lookup='wallet')
wallets_router.register(r'transactions', StellarTransactionViewSet, basename='wallet-transactions')

urlpatterns = router.urls + wallets_router.urls + [
    path('version/', views.version, name='version'),
    path('rates/', views.rates, name='rates'),
    path('info/cards/', views.card_info, name='card_info'),
]
