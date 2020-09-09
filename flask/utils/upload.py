import os
import os.path
import errno

import boto3
from werkzeug.utils import secure_filename

import config

session = boto3.session.Session()
client = session.client(
    "s3",
    region_name=config.DO_SPACES_REGION,
    endpoint_url=config.DO_SPACES_ENDPOINT_URL,
    aws_access_key_id=config.DO_SPACES_KEY,
    aws_secret_access_key=config.DO_SPACES_SECRET,
)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS
    )


def save_file(upload_file):
    filename = secure_filename(str(os.urandom(6)) + upload_file.filename)
    path = os.path.join(config.UPLOAD_FOLDER, filename)
    mkdir_p(config.UPLOAD_FOLDER)
    upload_file.save(path)
    bucket = config.DO_SPACES_BUCKET
    upload_path = f"{bucket}/{filename}"
    client.upload_file(path, bucket, filename)
    client.put_object_acl(ACL="public-read", Bucket=bucket, Key=filename)
    return f"{config.DO_SPACES_ENDPOINT_URL}/{upload_path}"
