from django.db.models.query import QuerySet
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.models import UserProfile
from kash.serializers.profile import ProfileSerializer


class ProfileViewset(ModelViewSet):
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(pk=self.request.user.profile.pk)

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

    @action(detail=True, methods=['get'])
    def send_recipients(self, request, pk=None):
        profile = self.get_object()
        serializer = self.get_serializer(UserProfile.objects.exclude(pk=profile.pk).exclude(payout_methods__isnull=True), many=True)

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def request_recipients(self, request, pk=None):
        profile = self.get_object()
        serializer = self.get_serializer(
            UserProfile.objects.exclude(pk=profile.pk).exclude(payout_methods__isnull=True), many=True)

        return Response(serializer.data)
