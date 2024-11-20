from configparser import ConfigParser

from pydantic import BaseModel, ConfigDict

from constants.env import CONFIG
from utils.singleton import Singleton


class EmailServer(BaseModel):
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = False
    start_tls: bool = True
    model_config = ConfigDict(from_attributes=True)

class InitConfig(metaclass=Singleton):
    def __init__(self):
        self._parser = ConfigParser()
        self._parser.read(CONFIG)

    def get(self, section: str) -> dict[str, str]:
        return {key: value for key, value in self._parser.items(section)}

