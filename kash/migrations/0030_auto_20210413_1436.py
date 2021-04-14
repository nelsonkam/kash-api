# Generated by Django 3.1.1 on 2021-04-13 14:36

from django.db import migrations
from django.db.models import Q


def fill_transactions(apps, schema_editor):
    KashTransaction = apps.get_model('kash', "KashTransaction")
    Transaction = apps.get_model('kash', "Transaction")
    PayoutMethod = apps.get_model('kash', "PayoutMethod")
    VirtualCard = apps.get_model('kash', "VirtualCard")
    SendKash = apps.get_model('kash', "SendKash")
    Profile = apps.get_model('kash', "UserProfile")

    from django.contrib.contenttypes.models import ContentType

    for txn in Transaction.objects.filter(Q(status="success") | Q(status="refunded")):
        kash_txn = KashTransaction(
            amount=txn.amount,
            sender=txn.initiator.profile,
            txn_ref=txn.reference,
            timestamp=txn.created
        )

        if txn.transaction_type == "payout":
            payout_method = PayoutMethod.objects.filter(phone=txn.phone, gateway=txn.gateway).first()
            if payout_method:
                content_type = ContentType.objects.get_for_model(Profile)
                kash_txn.receiver_id = payout_method.profile_id
                kash_txn.receiver_type_id = content_type.id
                kash_txn.profile = payout_method.profile
                kash_txn.narration = "Demande de kash 💰"
                kash_txn.txn_type = "credit"
                kash_txn.save()
        elif txn.transaction_type == "payment":
            kash_txn.txn_type = "debit"
            kash_txn.profile = txn.initiator.profile
            content_type = ContentType.objects.get(model=txn.content_type.model,
                                                   app_label=txn.content_type.app_label)
            content_object = content_type.get_object_for_this_type(pk=txn.object_id)
            card_type = ContentType.objects.get_for_model(VirtualCard)
            sendkash_type = ContentType.objects.get_for_model(SendKash)

            if content_type == card_type:
                kash_txn.narration = "Achat/recharge d'une carte virtuelle 💳"
                kash_txn.receiver_id = content_object.id
                kash_txn.receiver_type_id = content_type.id
                kash_txn.save()
            elif content_type == sendkash_type:
                kash_txn.narration = content_object.note
                kash_txn.receiver_id = content_object.id
                kash_txn.receiver_type_id = content_type.id
                kash_txn.save()


def remove_transactions(apps, schema_editor):
    KashTransaction = apps.get_model('kash', "KashTransaction")
    for i in KashTransaction.objects.all():
        i.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('kash', '0029_kashtransaction'),
    ]

    operations = [
        migrations.RunPython(fill_transactions, remove_transactions)
    ]
