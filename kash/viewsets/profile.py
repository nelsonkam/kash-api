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
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.utils import upload_content_file
from kash.models import UserProfile
from kash.serializers.profile import ProfileSerializer, LimitedProfileSerializer


class ProfileViewset(ModelViewSet):
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'profile'):
            return UserProfile.objects.filter(pk=self.request.user.profile.pk)
        return UserProfile.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        if self.kwargs[lookup_url_kwarg] == "current":
            if hasattr(self.request.user, 'profile'):
                obj = self.request.user.profile
            else:
                raise Http404
        else:
            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=['post'])
    def device_ids(self, request, pk=None):
        profile = self.get_object()
        device_id = request.data.get('device_id')
        if device_id and device_id not in profile.device_ids:
            profile.device_ids.append(device_id)
            profile.save()
        return Response(self.get_serializer(profile).data)

    # Deprecated. v1 legacy
    @action(detail=True, methods=['get'])
    def send_recipients(self, request, pk=None):
        profile = self.get_object()
        queryset = UserProfile.objects.exclude(pk=profile.pk).exclude(momo_accounts__isnull=True).order_by(
            "-created_at")
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    # Deprecated. v1 legacy
    @action(detail=True, methods=['get'])
    def request_recipients(self, request, pk=None):
        profile = self.get_object()
        serializer = LimitedProfileSerializer(
            UserProfile.objects.exclude(pk=profile.pk).exclude(momo_accounts__isnull=True), many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def avatar(self, request, pk=None):
        profile = self.get_object()
        image = request.data['avatar']
        profile.avatar_url = upload_content_file(image, f"{uuid4()}-{image.name}")
        profile.save()
        return Response(LimitedProfileSerializer(instance=profile).data)

    @action(detail=True, methods=['post'], url_path="search/contacts")
    def search_contacts(self, request, pk=None):
        profile = self.get_object()
        kashtag_vector = SearchVector('kashtag')
        name_vector = SearchVector('user__name')
        search = request.data['search']
        vectors = kashtag_vector + name_vector
        qs = UserProfile.objects.annotate(search=vectors)\
            .filter(search=search)\
            .exclude(pk=profile.pk)\
            .exclude(momo_accounts__isnull=True)
        return Response(LimitedProfileSerializer(qs, many=True).data)

    @action(detail=True, methods=['post'])
    def contacts(self, request, pk=None):
        profile = self.get_object()
        contacts = request.data['contacts']
        query = Q()
        for phone in contacts:
            query |= Q(user__phone_number__icontains=phone)

        profiles = UserProfile.objects.filter(query)
        contacts_pk = [contact.pk for contact in profile.contacts.all()]
        new_contacts = profiles.filter(~Q(pk__in=contacts_pk))
        profile.contacts.add(*new_contacts)

        return Response(LimitedProfileSerializer(profile.contacts.all(), many=True).data)

    @action(detail=True, methods=['post'], url_path='otp/phone')
    def otp_phone(self, request, pk=None):
        serializer = PhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_token = send_security_code_and_generate_session_token(
            str(serializer.validated_data["phone_number"])
        )
        return Response({"session_token": session_token})

    @action(detail=True, methods=['post'], url_path='otp/verify/phone')
    def verify_phone(self, request, pk=None):
        profile = self.get_object()
        serializer = SMSVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone_number')
        user = profile.user
        user.phone_number = phone
        user.save()
        return Response({"message": "Security code is valid."})