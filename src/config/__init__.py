from fastapi import APIRouter

from config.schema import AppSettings

router = APIRouter(prefix="/config", tags=["config"])
APP_SETTINGS = AppSettings(_yaml_file="appsettings.yml")  # type: ignore
