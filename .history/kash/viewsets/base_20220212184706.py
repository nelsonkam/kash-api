from rest_framework.viewsets import ModelViewSet

class BaseViewSet(ModelViewSet):
    def perform_authentication(self, request):
        super().perform_authentication(request)