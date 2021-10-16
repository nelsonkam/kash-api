from django.db import models
from core.models.base import BaseModel, generate_ref_id

class AdminPayoutRequest(BaseModel):
  code = models.CharField(max_length=12, default=generate_ref_id, unique=True)
  phone = models.CharField(max_length=255)
  gateway = models.CharField(max_length=255)
  amount = models.IntegerField()

  def execute(self):
    from kash.models import Transaction
    from core.models import User

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
