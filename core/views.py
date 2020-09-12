import base64

import boto3
import uuid
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from storages.backends.s3boto3 import S3Boto3Storage

from core.utils import upload_base64


@api_view(http_method_names=["POST"])
def upload(request):
    value = request.data.get("image")
    url = upload_base64(value)
    return Response(
        data={
            "url": url
        }
    )
