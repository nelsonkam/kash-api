from django.dispatch import Signal

transaction_status_changed = Signal(providing_args=['transaction'])
virtual_card_issued = Signal(providing_args=['card', 'amount'])
virtual_card_funded = Signal(providing_args=['card', 'amount'])
