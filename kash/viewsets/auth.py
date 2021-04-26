from phone_verify.serializers import PhoneSerializer, SMSVerificationSerializer
from phone_verify.services import send_security_code_and_generate_session_token
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User
from core.serializers import UserSerializer
from kash.models import UserProfile
from kash.serializers.auth import RegisterSerializer


class AuthViewSet(GenericViewSet):

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.create_user(username=data.get('kashtag'), name=data.get('name'), password=data.get('name'))
        UserProfile.objects.create(
            user=user,
            kashtag=data.get('kashtag')
        )
        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(instance=user).data,
        }
        return Response(data)
