import os

from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV")
IS_PRODUCTION = ENV == "production"
IS_TEST = ENV == "test"
IS_LOCAL = not IS_PRODUCTION and not IS_TEST
CONFIG = os.getenv("CONFIG")

DB_URL = os.getenv("DB_URL")
REDIS_URL = os.getenv("REDIS_URL")

MINIO_PUBLIC_URL = os.getenv("MINIO_URL")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_USERNAME = os.getenv("MINIO_USERNAME")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

API_PREFIX = os.getenv("API_PREFIX")
ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")
PROXY=os.getenv("PROXY") or None
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
REFRESH_SECRET = os.getenv("REFRESH_SECRET")
ACCESS_EXP_MINUTES: int = int(os.getenv("ACCESS_EXP_MINUTES"))
REFRESH_EXP_MINUTES: int = int(os.getenv("REFRESH_EXP_MINUTES"))

SENTRY_DSN = os.getenv("SENTRY_DSN")