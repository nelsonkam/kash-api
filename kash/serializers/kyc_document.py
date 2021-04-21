from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from kash.models import KYCDocument


class KYCDocumentSerializer(ModelSerializer):
    formatted = SerializerMethodField(read_only=True)

    def get_formatted(self, obj):
        name_map = {
            'id_card': "Carte d'identité",
            'passport': "Passeport"
        }
        color_map = {
            'pending': '#F7AF22',
            'accepted': '#1ACE4C',
            'rejected': "red"
        }
        text_map = {
            'pending': "En cours",
            'accepted': 'Validée',
            'rejected': "Rejétée"
        }
        return {
            'status_color': color_map[obj.status],
            'name': name_map[obj.document_type],
            'status_text': text_map[obj.status]
        }

    class Meta:
        model = KYCDocument
        fields = ['id', 'document_type', 'status', 'name', 'formatted']