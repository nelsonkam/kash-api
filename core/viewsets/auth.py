from django.contrib.auth import authenticate
from phone_verify.api import VerificationViewSet
from phone_verify.serializers import SMSVerificationSerializer
from rest_framework import exceptions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.serializers import UserSerializer


class Verification(VerificationViewSet):
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[AllowAny],
        serializer_class=SMSVerificationSerializer,
    )
    def verify(self, request):
        serializer = SMSVerificationSerializer(data=request.data)
        phone_number = request.data.get("phone_number")
        security_code = request.data.get("security_code")
        session_token = request.data.get("session_token")
        if serializer.is_valid():
            user = authenticate(
                request,
                phone_number=phone_number,
                security_code=security_code,
                session_token=session_token,
            )

            refresh = RefreshToken.for_user(user)
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(instance=user).data,
            }
            return Response(data)
        raise exceptions.AuthenticationFailed(detail=serializer.errors)
