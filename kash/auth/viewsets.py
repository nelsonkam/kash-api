from django.contrib.auth import authenticate
from phone_verify.services import send_security_code_and_generate_session_token
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from kash.invite.models import Referral
from kash.user.models import User, UserProfile
from kash.user.serializers import UserSerializer
from kash.auth.serializers import (
    RegisterSerializer,
    CustomPhoneSerializer,
    CustomSMSVerificationSerializer,
)


class AuthViewSet(GenericViewSet):
    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.create_user(
            username=data.get("kashtag"),
            name=data.get("name"),
            password=data.get("password"),
        )
        profile = UserProfile.objects.create(user=user, kashtag=data.get("kashtag"))
        refresh = RefreshToken.for_user(user)

        if referral_code := data.get("referral_code"):
            Referral.objects.record_referral(profile, referral_code)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(instance=user).data,
        }

        return Response(data)

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if not user:
            raise AuthenticationFailed("Invalid username/password")
        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(instance=user).data,
        }
        return Response(data)

    @action(detail=False, methods=["post"])
    def recover(self, request):
        serializer = CustomPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = str(serializer.validated_data.get("phone_number"))
        user = User.objects.filter(phone_number=phone).first()
        if not user:
            raise NotFound

        session_token = send_security_code_and_generate_session_token(
            str(serializer.validated_data["phone_number"])
        )
        return Response({"session_token": session_token})

    @action(detail=False, methods=["post"], url_path="recover/password")
    def reset_password(self, request):
        serializer = CustomSMSVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = str(serializer.validated_data.get("phone_number"))
        user = User.objects.filter(phone_number=phone).first()
        user.username = user.profile.kashtag
        user.set_password(request.data.get("password"))
        user.save()

        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(instance=user).data,
        }
        return Response(data)