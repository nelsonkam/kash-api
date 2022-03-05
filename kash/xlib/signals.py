from django.dispatch import Signal

transaction_status_changed = Signal(providing_args=["transaction"])
virtual_card_issued = Signal(providing_args=["card", "amount", "txn", "provider_data"])
virtual_card_funded = Signal(providing_args=["card", "amount", "txn", "provider_data"])
