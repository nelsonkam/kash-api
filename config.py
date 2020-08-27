import os
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()

JWT_REFRESH_TOKEN_EXPIRES = False
JWT_ACCESS_TOKEN_EXPIRES = False
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
DO_SPACES_KEY = os.getenv("DO_SPACES_KEY")
DO_SPACES_SECRET = os.getenv("DO_SPACES_SECRET")
DO_SPACES_BUCKET = os.getenv("DO_SPACES_BUCKET")
DO_SPACES_REGION = os.getenv("DO_SPACES_REGION")
DO_SPACES_ENDPOINT_URL = os.getenv("DO_SPACES_ENDPOINT_URL")
ONESIGNAL_APP_ID = os.getenv("ONESIGNAL_APP_ID")
ONESIGNAL_API_KEY = os.getenv("ONESIGNAL_API_KEY")

GQL_ENGINE_URL = os.getenv("GQL_ENGINE_URL")
GQL_ENGINE_SECRET = os.getenv("GQL_ENGINE_SECRET")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
REDIS_URL = os.getenv("REDIS_URL")
DB_URL = os.getenv("DB_URL")
SQLALCHEMY_DATABASE_URI = DB_URL

APP_ENV = os.getenv("APP_ENV")

result = urlparse(DB_URL)

ORATOR_DATABASES = {
    "postgres": {
        "driver": "postgres",
        "host": result.hostname,
        "database": result.path[1:],
        "user": result.username,
        "password": result.password,
        "port": result.port,
    }
}
