from django.contrib.auth import authenticate
from django.http import HttpResponseForbidden
from phone_verify.serializers import PhoneSerializer, SMSVerificationSerializer
from phone_verify.services import send_security_code_and_generate_session_token
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import User
from core.serializers import UserSerializer
from kash.models import UserProfile, Wallet
from kash.serializers.auth import RegisterSerializer


class AuthViewSet(GenericViewSet):

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.create_user(username=data.get('kashtag'), name=data.get('name'),
                                        password=data.get('password'))
        profile = UserProfile.objects.create(
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

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if not user:
            raise AuthenticationFailed
        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(instance=user).data,
        }
        return Response(data)

    @action(detail=False, methods=['post'])
    def recover(self, request):
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = str(serializer.validated_data.get('phone_number'))
        user = User.objects.filter(phone_number=phone).first()
        if not user:
            raise NotFound

        session_token = send_security_code_and_generate_session_token(
            str(serializer.validated_data["phone_number"])
        )
        return Response({"session_token": session_token})

    @action(detail=False, methods=['post'], url_path='recover/password')
    def reset_password(self, request):
        serializer = SMSVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = str(serializer.validated_data.get('phone_number'))
        user = User.objects.filter(phone_number=phone).first()
        user.username = user.profile.kashtag
        user.set_password(request.data.get('password'))
        user.save()

        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(instance=user).data,
        }
        return Response(data)
