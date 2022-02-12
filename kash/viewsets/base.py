from rest_framework.viewsets import ModelViewSet
from kash.models import UserProfile

class BaseViewSet(ModelViewSet):
    def perform_authentication(self, request):
        super().perform_authentication(request)
        self.request.profile = UserProfile.objects.get(user=self.request.user)  # qc: 1
