from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.test import override_settings

from core.models import User
from kash.card_providers import CardProvider
from kash.models import UserProfile, VirtualCard, Transaction, FundingHistory
from kash.utils import Gateway, TransactionStatus
from kash.tasks import retry_failed_funding


@override_settings(TESTING=True, CELERY_TASK_ALWAYS_EAGER=True)
class CardTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test',
            phone_number='00000000'
        )
        cls.profile = UserProfile.objects.create(
            user=cls.user,
            kashtag='test'
        )

    def setUp(self) -> None:
        self.client.force_authenticate(user=self.user)

    def test_card_issuing(self):
        response = self.client.post(reverse("virtual-cards-list"), {
            "nickname": 'Test Card',
            'category': VirtualCard.Category.general
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("nickname"), 'Test Card')
        self.assertEqual(response.data.get("category"), VirtualCard.Category.general)
        self.assertEqual(response.data.get("external_id"), '')
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        self.assertEqual(card.provider_name, CardProvider.dummy)

        response = self.client.post(reverse("virtual-cards-purchase", kwargs={'pk': card.pk}), {
            "amount": 10,
            'phone': '90137010',
            'gateway': Gateway.mtn
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        self.assertNotEqual(card.external_id, '')
        self.assertNotEqual(card.last_4, '')
        txn = Transaction.objects.get(reference=response.data.get("txn_ref"))
        history_item = FundingHistory.objects.get(txn_ref=txn.reference)
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.success)
        self.assertEqual(history_item.retries, 1)

    def test_card_funding(self):
        response = self.client.post(reverse("virtual-cards-list"), {
            "nickname": 'Test Card',
            'category': VirtualCard.Category.general
        })
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        self.client.post(reverse("virtual-cards-purchase", kwargs={'pk': card.pk}), {
            "amount": 10,
            'phone': '90137010',
            'gateway': Gateway.mtn
        })

        response = self.client.post(reverse("virtual-cards-fund", kwargs={'pk': card.pk}), {
            "amount": 10,
            'phone': '90137010',
            'gateway': Gateway.mtn
        })

        txn = Transaction.objects.get(reference=response.data.get("txn_ref"))
        history_item = FundingHistory.objects.get(txn_ref=txn.reference)
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.success)
        self.assertEqual(history_item.retries, 1)

    def test_card_issuing_success_on_retry(self):
        response = self.client.post(reverse("virtual-cards-list"), {
            "nickname": 'Fail: Test Card',
            'category': VirtualCard.Category.general
        })
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        response = self.client.post(reverse("virtual-cards-purchase", kwargs={'pk': card.pk}), {
            "amount": 10,
            'phone': '90137010',
            'gateway': Gateway.mtn
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        txn = Transaction.objects.get(reference=response.data.get("txn_ref"))
        history_item = FundingHistory.objects.get(txn_ref=txn.reference, card=card)
        self.assertEqual(card.external_id, '')
        self.assertEqual(card.last_4, '')
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
        self.assertEqual(history_item.retries, 1)

        retry_failed_funding.delay()
        history_item.refresh_from_db()
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
        self.assertEqual(history_item.retries, 2)

        card.nickname = "Test Card"
        card.save()
        retry_failed_funding.delay()
        history_item.refresh_from_db()
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.success)
        self.assertEqual(history_item.retries, 3)

    def test_card_issuing_fail_on_retry(self):
        response = self.client.post(reverse("virtual-cards-list"), {
            "nickname": 'Fail: Test Card',
            'category': VirtualCard.Category.general
        })
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        response = self.client.post(reverse("virtual-cards-purchase", kwargs={'pk': card.pk}), {
            "amount": 10,
            'phone': '90137010',
            'gateway': Gateway.mtn
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        txn = Transaction.objects.get(reference=response.data.get("txn_ref"))
        history_item = FundingHistory.objects.get(txn_ref=txn.reference, card=card)
        self.assertEqual(card.external_id, '')
        self.assertEqual(card.last_4, '')
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
        self.assertEqual(history_item.retries, 1)

        for i in range(history_item.retries, FundingHistory.MAX_FUNDING_RETRIES - 1):
            retry_failed_funding.delay()
            history_item.refresh_from_db()
            self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
            self.assertEqual(history_item.retries, i + 1)

        retry_failed_funding.delay()
        history_item.refresh_from_db()
        txn.refresh_from_db()
        self.assertEqual(txn.status, TransactionStatus.refunded)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.failed)
        self.assertEqual(history_item.retries, 4)

    def test_card_funding_success_on_retry(self):
        response = self.client.post(reverse("virtual-cards-list"), {
            "nickname": 'Test Card',
            'category': VirtualCard.Category.general
        })
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        self.client.post(reverse("virtual-cards-purchase", kwargs={'pk': card.pk}), {
            "amount": 10,
            'phone': '90137010',
            'gateway': Gateway.mtn
        })

        card.nickname = "Fail: Test Card"
        card.save()
        response = self.client.post(reverse("virtual-cards-fund", kwargs={'pk': card.pk}), {
            "amount": 10,
            'phone': '90137010',
            'gateway': Gateway.mtn
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        txn = Transaction.objects.get(reference=response.data.get("txn_ref"))
        history_item = FundingHistory.objects.get(txn_ref=txn.reference, card=card)
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
        self.assertEqual(history_item.retries, 1)

        retry_failed_funding.delay()
        history_item.refresh_from_db()
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
        self.assertEqual(history_item.retries, 2)

        card.nickname = "Test Card"
        card.save()
        retry_failed_funding.delay()
        history_item.refresh_from_db()
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.success)
        self.assertEqual(history_item.retries, 3)

    def test_card_funding_fail_on_retry(self):
        response = self.client.post(reverse("virtual-cards-list"), {
            "nickname": 'Test Card',
            'category': VirtualCard.Category.general
        })
        card = VirtualCard.objects.get(pk=response.data.get("id"))
        self.client.post(reverse("virtual-cards-purchase", kwargs={'pk': card.pk}), {
            "amount": 10,
            'phone': '90137010',
            'gateway': Gateway.mtn
        })

        card.nickname = "Fail: Test Card"
        card.save()
        response = self.client.post(reverse("virtual-cards-fund", kwargs={'pk': card.pk}), {
            "amount": 10,
            'phone': '90137010',
            'gateway': Gateway.mtn
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        txn = Transaction.objects.get(reference=response.data.get("txn_ref"))
        history_item = FundingHistory.objects.get(txn_ref=txn.reference, card=card)
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
        self.assertEqual(history_item.retries, 1)

        for i in range(history_item.retries, FundingHistory.MAX_FUNDING_RETRIES - 1):
            retry_failed_funding.delay()
            history_item.refresh_from_db()
            self.assertEqual(history_item.status, FundingHistory.FundingStatus.paid)
            self.assertEqual(history_item.retries, i + 1)

        retry_failed_funding.delay()
        history_item.refresh_from_db()
        txn.refresh_from_db()
        self.assertEqual(txn.status, TransactionStatus.refunded)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.failed)
        self.assertEqual(history_item.retries, 4)