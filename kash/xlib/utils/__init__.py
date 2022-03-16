import logging

import boto3
import uuid
import base64

from botocore.exceptions import ClientError
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def upload_content_file(content_file, filename, acl="public-read"):
    session = boto3.session.Session()
    client = session.client(
        "s3",
        region_name=settings.DO_SPACES_REGION,
        endpoint_url=settings.DO_SPACES_ENDPOINT_URL,
        aws_access_key_id=settings.DO_SPACES_KEY,
        aws_secret_access_key=settings.DO_SPACES_SECRET,
    )

    path = default_storage.save(f"static/uploads/{filename}", content_file)
    resp = client.upload_file(path, settings.DO_SPACES_BUCKET, filename)
    resp = client.put_object_acl(
        ACL=acl, Bucket=settings.DO_SPACES_BUCKET, Key=filename
    )

    return f"{settings.DO_SPACES_ENDPOINT_URL}/{settings.DO_SPACES_BUCKET}/{filename}"


def upload_base64(encoded_file):
    fmt, imgstr = encoded_file.split(";base64,")
    ext = fmt.split("/")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file = ContentFile(base64.b64decode(imgstr), name=filename)
    return upload_content_file(file, filename)


def money_to_dict(price):
    return {"amount": price.amount, "currency": str(price.currency)}


def create_presigned_url(
    object_url, bucket_name=settings.DO_SPACES_BUCKET, expiration=3600
):
    session = boto3.session.Session()
    client = session.client(
        "s3",
        region_name=settings.DO_SPACES_REGION,
        endpoint_url=settings.DO_SPACES_ENDPOINT_URL,
        aws_access_key_id=settings.DO_SPACES_KEY,
        aws_secret_access_key=settings.DO_SPACES_SECRET,
    )
    try:
        response = client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_url.split("/")[-1]},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    return response
