from django.test import TestCase, override_settings
from djmoney.money import Money

from core.models import User
from kash.card_providers import CardProvider
from kash.models import VirtualCard, UserProfile, FundingHistory
from kash.tasks import retry_failed_funding
from kash.utils import TransactionStatus


@override_settings(TESTING=True, CELERY_TASK_ALWAYS_EAGER=True)
class FundingHistoryTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='test_card',
            phone_number='00000000'
        )
        cls.profile = UserProfile.objects.create(
            user=cls.user,
            kashtag='test_card'
        )

    def test_card_issuing(self):
        card = VirtualCard.objects.create(
            nickname="Test Card",
            provider_name=CardProvider.dummy,
            profile=self.profile
        )
        txn = card.purchase_momo(Money(10, "USD"), "90137010", "mtn-bj")
        history_item = FundingHistory.objects.get(txn_ref=txn.reference)
        txn.refresh_from_db()
        self.assertEqual(txn.status, TransactionStatus.success)
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.success)
        self.assertEqual(history_item.retries, 1)

    def test_card_issuing_fail_retry(self):
        card = VirtualCard.objects.create(
            nickname="Fail: Test Card",
            provider_name=CardProvider.dummy,
            profile=self.profile
        )

        txn = card.purchase_momo(Money(10, "USD"), "90137010", "mtn-bj")
        history_item = FundingHistory.objects.get(txn_ref=txn.reference)
        txn.refresh_from_db()
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

        retry_failed_funding.delay()
        history_item.refresh_from_db()
        self.assertEqual(history_item.status, FundingHistory.FundingStatus.success)
        self.assertEqual(history_item.retries, 3)

