from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from kash.models import KashTransaction, UserProfile, VirtualCard, SendKash
from kash.serializers.profile import ProfileSerializer


class KashTransactionSerializer(ModelSerializer):
    sender = ProfileSerializer(read_only=True)
    formatted = SerializerMethodField(read_only=True)

    def get_formatted(self, obj):
        title = None
        if isinstance(obj.receiver, UserProfile):
            title = f"Envoi à ${obj.receiver.kashtag}"
        elif isinstance(obj.receiver, VirtualCard):
            title = obj.receiver.nickname
        elif isinstance(obj.receiver, SendKash):
            if obj.receiver.recipients.count() == 1:
                title = f"Envoi à ${obj.receiver.recipients.first().kashtag}"
            else:
                title = f"Envoi à {obj.receiver.recipients.count()} personnes"
        else:
            raise NotImplementedError
        return {
            'title': title,
            'description': obj.narration
        }

    class Meta:
        model = KashTransaction
        fields = ['id', 'amount', 'amount_currency', 'sender', 'txn_ref', 'narration', 'formatted', 'txn_type','status', 'timestamp']
