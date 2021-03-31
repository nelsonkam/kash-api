from django.dispatch import Signal

transaction_status_changed = Signal(providing_args=['transaction'])
