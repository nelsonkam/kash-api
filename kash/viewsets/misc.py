from django.contrib.auth import authenticate
from django.http import HttpResponseForbidden
from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money
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


class MiscViewSet(GenericViewSet):

    @action(detail=False, methods=['GET'])
    def rates(self, request):
        return Response({
            "USD": 1,
            "XOF": convert_money(Money(1, "USD"), "XOF")
        })