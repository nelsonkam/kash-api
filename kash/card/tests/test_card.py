from djmoney.money import Money
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.test import override_settings

from kash.user.models import User, UserProfile
from kash.card.providers import CardProvider
from kash.card.providers.dummy import set_dummy_balance
from kash.card.models import VirtualCard, FundingHistory, WithdrawalHistory
from kash.transaction.models import Transaction
from kash.earning.models import Earning
from kash.payout.models import Rate

from kash.xlib.utils.utils import (
    Gateway,
    TransactionStatus,
    TransactionType,
    Conversions,
)


@override_settings(TESTING=True, CELERY_TASK_ALWAYS_EAGER=True)
class CardTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username="test", phone_number="00000000")
        cls.profile = UserProfile.objects.create(user=cls.user, kashtag="test")
        Rate.objects.get_or_create(
            code=Rate.Codes.rave_usd_ngn, defaults={"value": 590}
        )

    def setUp(self) -> None:
        self.client.force_authenticate(user=self.user)

    def test_card_issuing(self):
        response = self.client.post(
            reverse("virtual-cards-list"),
            {"nickname": "Test Card", "category": VirtualCard.Category.general},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("nickname"), "Test Card")
        self.assertEqual(response.data.get("category"), VirtualCard.Category.general)
        self.assertEqual(response.data.get("external_id"), "")
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        self.assertEqual(card.provider_name, CardProvider.dummy)

        response = self.client.post(
            reverse("virtual-cards-purchase", kwargs={"pk": card.pk}),
            {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        self.assertNotEqual(card.external_id, "")
        self.assertNotEqual(card.last_4, "")
        txn = Transaction.objects.get(reference=response.data.get("txn_ref"))
        history_item = FundingHistory.objects.get(txn_ref=txn.reference)
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.success)
        self.assertEqual(history_item.retries, 1)

    def test_card_funding(self):
        response = self.client.post(
            reverse("virtual-cards-list"),
            {"nickname": "Test Card", "category": VirtualCard.Category.general},
        )
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        self.client.post(
            reverse("virtual-cards-purchase", kwargs={"pk": card.pk}),
            {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn},
        )

        response = self.client.post(
            reverse("virtual-cards-fund", kwargs={"pk": card.pk}),
            {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn},
        )

        txn = Transaction.objects.get(reference=response.data.get("txn_ref"))
        history_item = FundingHistory.objects.get(txn_ref=txn.reference)
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.success)
        self.assertEqual(history_item.retries, 1)

    def test_card_issuing_success_on_retry(self):
        response = self.client.post(
            reverse("virtual-cards-list"),
            {"nickname": "Fail: Test Card", "category": VirtualCard.Category.general},
        )
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        response = self.client.post(
            reverse("virtual-cards-purchase", kwargs={"pk": card.pk}),
            {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        txn = Transaction.objects.get(reference=response.data.get("txn_ref"))
        history_item = FundingHistory.objects.get(txn_ref=txn.reference, card=card)
        self.assertEqual(card.external_id, "")
        self.assertEqual(card.last_4, "")
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
        self.assertEqual(history_item.retries, 1)

        card.nickname = "Test Card"
        card.save(update_fields=["nickname"])
        history_item.fund()
        history_item.refresh_from_db()
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.success)
        self.assertEqual(history_item.retries, 2)

    def test_card_issuing_fail_on_retry(self):
        response = self.client.post(
            reverse("virtual-cards-list"),
            {"nickname": "Fail: Test Card", "category": VirtualCard.Category.general},
        )
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        response = self.client.post(
            reverse("virtual-cards-purchase", kwargs={"pk": card.pk}),
            {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        txn = Transaction.objects.get(reference=response.data.get("txn_ref"))
        history_item = FundingHistory.objects.get(txn_ref=txn.reference, card=card)
        self.assertEqual(card.external_id, "")
        self.assertEqual(card.last_4, "")
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
        self.assertEqual(history_item.retries, 1)

        for i in range(history_item.retries, FundingHistory.MAX_FUNDING_RETRIES - 1):
            history_item.fund()
            history_item.refresh_from_db()
            self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
            self.assertEqual(history_item.retries, i + 1)

        history_item.fund()
        history_item.refresh_from_db()
        txn.refresh_from_db()
        self.assertEqual(txn.status, TransactionStatus.refunded)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.failed)
        self.assertEqual(history_item.retries, FundingHistory.MAX_FUNDING_RETRIES)

    def test_card_funding_success_on_retry(self):
        response = self.client.post(
            reverse("virtual-cards-list"),
            {"nickname": "Test Card", "category": VirtualCard.Category.general},
        )
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        self.client.post(
            reverse("virtual-cards-purchase", kwargs={"pk": card.pk}),
            {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn},
        )

        card.nickname = "Fail: Test Card"
        card.save(update_fields=["nickname"])
        response = self.client.post(
            reverse("virtual-cards-fund", kwargs={"pk": card.pk}),
            {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        txn = Transaction.objects.get(reference=response.data.get("txn_ref"))
        history_item = FundingHistory.objects.get(txn_ref=txn.reference, card=card)
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
        self.assertEqual(history_item.retries, 1)

        card.nickname = "Test Card"
        card.save(update_fields=["nickname"])
        history_item.fund()
        history_item.refresh_from_db()
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.success)
        self.assertEqual(history_item.retries, 2)

    def test_card_funding_fail_on_retry(self):
        response = self.client.post(
            reverse("virtual-cards-list"),
            {"nickname": "Test Card", "category": VirtualCard.Category.general},
        )
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        self.client.post(
            reverse("virtual-cards-purchase", kwargs={"pk": card.pk}),
            {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn},
        )

        card.nickname = "Fail: Test Card"
        card.save(update_fields=["nickname"])
        response = self.client.post(
            reverse("virtual-cards-fund", kwargs={"pk": card.pk}),
            {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        txn = Transaction.objects.get(reference=response.data.get("txn_ref"))
        history_item = FundingHistory.objects.get(txn_ref=txn.reference, card=card)
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
        self.assertEqual(history_item.retries, 1)

        for i in range(history_item.retries, FundingHistory.MAX_FUNDING_RETRIES - 1):
            history_item.fund()
            history_item.refresh_from_db()
            self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
            self.assertEqual(history_item.retries, i + 1)

        history_item.fund()
        history_item.refresh_from_db()
        txn.refresh_from_db()
        self.assertEqual(txn.status, TransactionStatus.refunded)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.failed)
        self.assertEqual(history_item.retries, FundingHistory.MAX_FUNDING_RETRIES)

    def test_card_withdraw_success(self):
        response = self.client.post(
            reverse("virtual-cards-list"),
            {"nickname": "Test Card", "category": VirtualCard.Category.general},
        )
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        self.client.post(
            reverse("virtual-cards-purchase", kwargs={"pk": card.pk}),
            {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn},
        )
        data = {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn}
        response = self.client.post(
            reverse("virtual-cards-withdraw", kwargs={"pk": card.pk}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        txn = Transaction.objects.get(
            phone=data.get("phone"),
            gateway=data.get("gateway"),
            transaction_type=TransactionType.payout,
        )
        history_item = WithdrawalHistory.objects.get(txn_ref=txn.reference, card=card)
        xof_amount = Conversions.get_xof_from_usd(
            Money(data.get("amount"), "USD"), is_withdrawal=True
        )
        self.assertEqual(txn.amount, xof_amount)
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, WithdrawalHistory.Status.paid_out)

    def test_card_withdraw_fail(self):
        response = self.client.post(
            reverse("virtual-cards-list"),
            {"nickname": "Test Card", "category": VirtualCard.Category.general},
        )
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        self.client.post(
            reverse("virtual-cards-purchase", kwargs={"pk": card.pk}),
            {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn},
        )
        card.refresh_from_db()
        card.nickname = "Fail: Test Card"
        card.save(update_fields=["nickname"])
        data = {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn}
        with self.assertRaises(Exception):
            self.client.post(
                reverse("virtual-cards-withdraw", kwargs={"pk": card.pk}), data
            )

    def test_card_funding_balance_insufficient(self):
        set_dummy_balance(100)
        response = self.client.post(
            reverse("virtual-cards-list"),
            {"nickname": "Test Card", "category": VirtualCard.Category.general},
        )
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        self.client.post(
            reverse("virtual-cards-purchase", kwargs={"pk": card.pk}),
            {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn},
        )

        response = self.client.post(
            reverse("virtual-cards-fund", kwargs={"pk": card.pk}),
            {"amount": 1000, "phone": "90137010", "gateway": Gateway.mtn},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        txn = Transaction.objects.get(reference=response.data.get("txn_ref"))
        history_item = FundingHistory.objects.get(txn_ref=txn.reference, card=card)
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
        self.assertEqual(history_item.retries, 1)

        # test funding retry while balance hasn't been funded yet
        history_item.fund()
        history_item.refresh_from_db()
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
        self.assertEqual(history_item.retries, 1)

        set_dummy_balance(1100)
        history_item.fund()
        history_item.refresh_from_db()
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.success)
        self.assertEqual(history_item.retries, 2)

    def test_card_earning_recorded(self):
        response = self.client.post(
            reverse("virtual-cards-list"),
            {"nickname": "Test Card", "category": VirtualCard.Category.general},
        )
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        self.client.post(
            reverse("virtual-cards-purchase", kwargs={"pk": card.pk}),
            {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn},
        )
        self.assertEqual(Earning.objects.count(), 1)

        self.client.post(
            reverse("virtual-cards-fund", kwargs={"pk": card.pk}),
            {"amount": 10, "phone": "90137010", "gateway": Gateway.mtn},
        )
        self.assertEqual(Earning.objects.count(), 2)

    def test_txn_callback_authentication(self):
        self.client.logout()
        response = self.client.post(
            reverse("virtual-cards-txn-callback"),
            {},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_txn_callback(self):
        # todo: mock notifications for tests like django mailbox
        # in order to test txn_callback effectively
        pass