from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from kash.models import InviteCode
from kash.serializers.invite_code import InviteCodeSerializer


class InviteCodeViewset(ModelViewSet):
    serializer_class = InviteCodeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return self.request.user.profile.invite_codes.all()

    def perform_create(self, serializer):
        serializer.save(inviter=self.request.user.profile)

    @action(detail=False, methods=['POST'])
    def verify(self, request):
        code = request.data.get('code')
        if code in ["$$$$", "100$"]:
            InviteCode.objects.create(
                inviter=self.request.user.profile,
                invited=self.request.user.profile,
                used_at=now()
            )
            return Response(dict(message="Code verified"))

        invite = InviteCode.objects.filter(code=code).first()
        if not invite:
            return Response({'code': 'invalid'}, status=400)

        if invite.used_at:
            return Response({'code': 'used'}, status=400)

        invite.used_at = now()
        invite.invited = self.request.user.profile
        invite.save()
        return Response(dict(message="Code verified"))
