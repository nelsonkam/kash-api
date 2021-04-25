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
            if obj.sender == obj.profile:
                title = f"Envoi à ${obj.receiver.kashtag}"
            else:
                if obj.is_anonymous:
                    title = f"Anonyme 🤑"
                else:
                    title = f"${obj.sender.kashtag}"
        elif isinstance(obj.receiver, VirtualCard):
            title = obj.receiver.nickname
        elif isinstance(obj.receiver, SendKash):
            if obj.sender == obj.profile:
                if obj.receiver.recipients.count() == 1:
                    title = f"Envoi à ${obj.receiver.recipients.first().kashtag}"
                else:
                    title = f"Envoi à {obj.receiver.recipients.count()} personnes"
            else:
                if obj.receiver.is_incognito:
                    title = "Anonyme"
                else:
                    title = f"${obj.sender.kashtag}"
        else:
            raise NotImplementedError
        return {
            'title': title,
            'description': f"Pour: {obj.narration}"
        }

    class Meta:
        model = KashTransaction
        fields = ['id', 'amount', 'amount_currency', 'sender', 'txn_ref', 'narration', 'formatted', 'txn_type',
                  'status', 'timestamp']
