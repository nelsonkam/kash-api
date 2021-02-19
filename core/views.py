import base64

import boto3
import uuid
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render


from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from storages.backends.s3boto3 import S3Boto3Storage
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.utils import upload_base64
from core.serializers import UserSerializer


@api_view(http_method_names=["POST"])
def upload(request):
    value = request.data.get("image")
    url = upload_base64(value)
    return Response(
        data={
            "url": url
        }
    )

@api_view(http_method_names=['GET'])
@authentication_classes([JWTAuthentication])
def user_current(request):
    return Response(UserSerializer(request.user).data,)