from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class EmailServer(BaseModel):
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = False
    start_tls: bool = True
    model_config = ConfigDict(from_attributes=True)

class SentryConfig(BaseModel):
    traces_sample_rate: float = Field(ge=0.0, le=1.0)
    sample_rate: float = Field(ge=0.0, le=1.0)
    profiles_sample_rate: float = Field(ge=0.0, le=1.0)

class DiscordConfig(BaseModel):
    base_url: str = Field(...)
    notification_path: str = Field(...)
