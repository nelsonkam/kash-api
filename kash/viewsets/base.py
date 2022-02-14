from rest_framework.viewsets import ModelViewSet

from core.models import User
from kash.models import UserProfile

class BaseViewSet(ModelViewSet):
    def perform_authentication(self, request):
        super().perform_authentication(request)
        if isinstance(self.request.user, User):
            self.request.profile = UserProfile.objects.get(user=self.request.user)  # qc: 1