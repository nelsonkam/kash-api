from decimal import Decimal
from django.db import models

from kash.abstract.models import BaseModel, generate_ref_id
from kash.xlib.utils.utils import TransactionStatus


class AdminPayoutRequest(BaseModel):
    code = models.CharField(max_length=12, default=generate_ref_id, unique=True)
    phone = models.CharField(max_length=255)
    gateway = models.CharField(max_length=255)
    amount = models.IntegerField()

    class Meta:
        db_table = "kash_adminpayoutrequest"

    def execute(self):
        from kash.transaction.models import Transaction
        from kash.user.models import User

        admin = User.objects.get(is_superuser=True)
        Transaction.objects.request(
            obj=admin,
            name="admin",
            amount=self.amount,
            phone=str(self.phone),
            gateway=self.gateway,
            initiator=admin,
            txn_type="payout",
        )


class Topup(BaseModel):
    code = models.CharField(max_length=12, default=generate_ref_id, unique=True)
    amount = models.IntegerField()
    ngn_payin_status = models.CharField(max_length=200, default=TransactionStatus.pending)
    xof_txn_status = models.CharField(max_length=200, default=TransactionStatus.pending)
    usd_txn_status = models.CharField(max_length=200, default=TransactionStatus.pending)
    xof_txn_ref = models.CharField(max_length=255, blank=True)
    is_canceled = models.BooleanField(default=False)

    def payout_xof(self, phone, gateway):
        from kash.transaction.models import Transaction
        from kash.user.models import User
        rate = Rate.objects.get(code=Rate.Codes.xof_usdt)

        admin = User.objects.get(is_superuser=True)
        txn = Transaction.objects.request(
            obj=admin,
            name="admin",
            amount=Decimal(self.amount) * rate.value,
            phone=str(phone),
            gateway=gateway,
            initiator=admin,
            txn_type="payout",
        )
        self.xof_txn_ref = txn.reference
        self.xof_txn_status = txn.status
        self.save()
        



class Rate(BaseModel):
    class Codes(models.TextChoices):
        rave_usd_ngn = "rave-usd-ngn"
        xof_usdt = "xof-usdt"

    class Meta:
        db_table = "kash_rate"

    code = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=17, decimal_places=2)
