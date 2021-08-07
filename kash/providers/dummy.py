from kash.providers.base import BaseProvider
from kash.utils import TransactionStatus, generate_reference_10


class DummyProvider(BaseProvider):
    def process(self, transaction):
        if "fail-" in transaction.reference:
            transaction.change_status(TransactionStatus.failed)
        else:
            transaction.change_status(TransactionStatus.success)

    def payout(self, transaction):
        if "fail-" in transaction.reference:
            transaction.change_status(TransactionStatus.failed)
        else:
            transaction.change_status(TransactionStatus.success)

    def refund(self, transaction):
        transaction.refund_reference = generate_reference_10()
        transaction.save(update_fields=['refund_reference'])
        transaction.change_status(TransactionStatus.refunded)

    def retry(self, transaction):
        transaction.reference = generate_reference_10()
        transaction.save(update_fields=['reference'])
        transaction.change_status(TransactionStatus.success)

    def check_status(self, transaction):
        if "fail-" in transaction.reference:
            transaction.change_status(TransactionStatus.failed)
        else:
            transaction.change_status(TransactionStatus.success)
