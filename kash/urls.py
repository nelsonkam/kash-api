from django.urls import path
from rest_framework.routers import SimpleRouter

from kash.models import KashRequest
from kash.viewsets.kash_request import KashRequestViewSet
from kash.viewsets.kash_transaction import KashTransactionViewSet
from kash.viewsets.notification import NotificationViewset
from kash.viewsets.payment_method import PayoutMethodViewset
from kash.viewsets.profile import ProfileViewset
from kash.viewsets.session import CheckoutSessionViewset
from kash.viewsets.transaction import TransactionViewSet
from kash.viewsets.virtual_card import VirtualCardViewSet
from storefront.viewsets import ShopViewSet

router = SimpleRouter()
router.register("sessions", CheckoutSessionViewset, "checkout-session")
router.register("shops", ShopViewSet, "shops")
router.register("profiles", ProfileViewset, "profiles")
router.register("virtual-cards", VirtualCardViewSet, "virtual-cards")
router.register("transactions", TransactionViewSet, "transaction")
router.register("send", KashTransactionViewSet, "send-kash")
router.register("payout-methods", PayoutMethodViewset, "payout-methods")
router.register("requests", KashRequestViewSet, "request-kash")
router.register("notifications", NotificationViewset, "notifications")

urlpatterns = router.urls
