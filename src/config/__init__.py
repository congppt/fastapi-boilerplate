from fastapi import APIRouter

from config.schema import AppSettings

router = APIRouter(prefix="/config", tags=["config"])
APP_SETTINGS = AppSettings()  # type: ignore
