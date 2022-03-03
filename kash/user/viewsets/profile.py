from uuid import uuid4

from django.http import Http404
from phone_verify.serializers import PhoneSerializer, SMSVerificationSerializer
from phone_verify.services import send_security_code_and_generate_session_token
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.auth.services import AuthService
from kash.auth.throttling import VerificationCodeThrottle
from kash.promo.models import PromoCode
from kash.user.models import User
from kash.xlib.utils import upload_content_file
from kash.user.models import UserProfile
from kash.user.serializers import ProfileSerializer, LimitedProfileSerializer

from kash.abstract.viewsets import BaseViewSet


class ProfileViewset(BaseViewSet):
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    service = AuthService()

    def get_queryset(self):
        if hasattr(self.request, "profile"):
            return self.request.profile
        return UserProfile.objects.none()

    def create(self, request, *args, **kwargs):
        # user cannot create a profile (i.e. POST /profile/)
        # it is automatically done on auth/register/
        raise MethodNotAllowed("POST")

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

    @action(detail=True, methods=["post"], url_path="otp/phone", throttle_classes=[VerificationCodeThrottle])
    def otp_phone(self, request, pk=None):
        session_token = self.service.send_phone_verification_code(request.data.get("phone_number"))
        return Response({"session_token": session_token})

    @action(detail=True, methods=["post"], url_path="otp/verify/phone")
    def verify_phone(self, request, pk=None):
        self.service.link_phone_number(
            user=request.user,
            security_code=request.data.get("security_code"),
            phone_number=request.data.get("phone_number"),
            session_token=request.data.get("session_token"),
        )
        return Response({"message": "Security code is valid."})

    @action(detail=True, methods=["post"], url_path="promo/apply")
    def apply_promo_code(self, request, pk=None):
        profile = self.get_object()
        code = request.data.get("code")
        promo_code = get_object_or_404(PromoCode, code=code)
        promo_code.apply(profile)
        return Response(status=201)
