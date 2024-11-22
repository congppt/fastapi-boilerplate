from fastapi import APIRouter

from config.handler import StartupConfig
from constants.env import CONFIG

router = APIRouter(prefix='/config', tags=['config'])
STARTUP_CONFIG = StartupConfig(CONFIG)