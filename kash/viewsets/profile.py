from kash.models.promo_code import PromoCode
from uuid import uuid4

import phonenumbers
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404
from phone_verify.serializers import PhoneSerializer, SMSVerificationSerializer
from phone_verify.services import send_security_code_and_generate_session_token
from phonenumbers import NumberParseException
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import User
from core.utils import upload_content_file
from kash.models import UserProfile, Wallet
from kash.serializers.profile import ProfileSerializer, LimitedProfileSerializer
from kash.serializers.wallet import WalletSerializer

from .base import BaseViewSet


class ProfileViewset(BaseViewSet):
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request, "profile"):
            return self.request.profile
        return UserProfile.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        if self.kwargs[lookup_url_kwarg] == "current":
            if hasattr(self.request, "profile"):
                obj = self.request.profile
            else:
                raise Http404
        else:
            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=["post"])
    def device_ids(self, request, pk=None):
        profile = self.get_object()
        device_id = request.data.get("device_id")
        if device_id and device_id not in profile.device_ids:
            profile.device_ids.append(device_id)
            profile.save()
        return Response(self.get_serializer(profile).data)

    @action(detail=True, methods=["post"])
    def avatar(self, request, pk=None):
        profile = self.get_object()
        image = request.data["avatar"]
        profile.avatar_url = upload_content_file(image, f"{uuid4()}-{image.name}")
        profile.save()
        return Response(LimitedProfileSerializer(instance=profile).data)

    @action(detail=True, methods=["post"], url_path="otp/phone")
    def otp_phone(self, request, pk=None):
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(username=serializer.validated_data["phone_number"])
        if user:
            raise PermissionDenied
        session_token = send_security_code_and_generate_session_token(
            str(serializer.validated_data["phone_number"])
        )
        return Response({"session_token": session_token})

    @action(detail=True, methods=["post"], url_path="otp/verify/phone")
    def verify_phone(self, request, pk=None):
        profile = self.get_object()
        serializer = SMSVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone_number")
        user = profile.user
        user.phone_number = phone
        user.save()
        return Response({"message": "Security code is valid."})

    @action(detail=True, methods=["post"], url_path="promo/apply")
    def apply_promo_code(self, request, pk=None):
        profile = self.get_object()
        code = request.data.get("code")
        promo_code = get_object_or_404(PromoCode, code=code)
        promo_code.apply(profile)
        return Response(status=201)
