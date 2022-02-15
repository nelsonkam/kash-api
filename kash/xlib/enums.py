from django.db.models import TextChoices


class PaymentMethod(TextChoices):
    momo = "momo", "Mobile Money"
    card = "card", "Credit or debit card"
    cash = "cash", "Cash on delivery"


class CardProvider(TextChoices):
    rave = "rave"
    dummy = "dummy"
