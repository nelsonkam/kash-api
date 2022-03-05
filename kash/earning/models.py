from djmoney.models.fields import MoneyField
from djmoney.money import Money

from django.db import models

from kash.abstract.models import BaseModel
from kash.xlib.utils.utils import compute_funding_earnings


class EarningManager(models.Manager):
    def record_issuing_earning(self, card, txn, funding_amount, funding_currency):
        if self.filter(txn_ref=txn.reference).first():
            return None
        issuing_earning_amount = compute_funding_earnings(card.issuance_cost, Money(2, "USD"), funding_currency)
        funding_earning_amount = compute_funding_earnings(
            txn.amount - card.issuance_cost, funding_amount, funding_currency
        )
        earning = self.model(
            amount=issuing_earning_amount + funding_earning_amount,
            operation=Earning.Operation.issuing,
            txn_ref=txn.reference,
        )
        earning.save()
        return earning

    def record_funding_earning(self, txn, funding_amount, funding_currency):
        if self.filter(txn_ref=txn.reference).first():
            return None
        earning_amount = compute_funding_earnings(txn.amount, funding_amount, funding_currency)
        earning = self.model(
            amount=earning_amount,
            operation=Earning.Operation.funding,
            txn_ref=txn.reference,
        )
        earning.save()
        return earning


class Earning(BaseModel):
    class Operation(models.TextChoices):
        issuing = "issuing", "Issuing"
        funding = "funding", "Funding"

    amount = MoneyField(max_digits=17, decimal_places=2, default_currency="XOF")
    operation = models.CharField(max_length=30, choices=Operation.choices)
    txn_ref = models.CharField(max_length=255, unique=True)

    objects = EarningManager()

    class Meta:
        db_table = "kash_earning"
