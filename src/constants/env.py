import os

from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")
REDIS_URL = os.getenv("REDIS_URL")

MINIO_PUBLIC_URL = os.getenv("MINIO_URL")
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_USERNAME = os.getenv("MINIO_USERNAME")
MINIO_PASSWORD = os.getenv("MINIO_PASSWORD")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

API_PREFIX = os.getenv("API_PREFIX")
ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")