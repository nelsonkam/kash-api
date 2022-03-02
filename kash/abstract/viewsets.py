from rest_framework.viewsets import ModelViewSet

from kash.user.models import UserProfile, User


class BaseViewSet(ModelViewSet):
    def perform_authentication(self, request):
        super().perform_authentication(request)
        if isinstance(self.request.user, User):
            self.request.profile = UserProfile.objects.get(user=self.request.user)  # qc: 1
