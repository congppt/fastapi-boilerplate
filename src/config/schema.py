from pydantic import BaseModel, ConfigDict, Field, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class EmailServer(BaseModel):
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = False
    start_tls: bool = True
    model_config = ConfigDict(from_attributes=True)


class SentryConfig(BaseModel):
    sentry_dsn: str = Field(...)
    traces_sample_rate: float = Field(ge=0.0, le=1.0)
    sample_rate: float = Field(ge=0.0, le=1.0)
    profiles_sample_rate: float = Field(ge=0.0, le=1.0)


class DiscordConfig(BaseModel):
    base_url: str = Field(...)
    notification_path: str = Field(...)


class AuthConfig(BaseModel):
    access_secret: str = Field(min_length=32)
    refresh_secret: str = Field(min_length=32)
    access_exp_minutes: PositiveInt
    refresh_exp_minutes: PositiveInt


class StorageConfig(BaseModel):
    host: str = Field(...)
    bucket: str = Field(...)
    access: str = Field(...)
    secret: str = Field(...)
    public_endpoint: str = Field(...)


class EnvConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=('.env', '.env.local'), env_file_encoding='utf-8')
    env: str = Field(...)
    db_url: str = Field(...)
    cache_url: str = Field(...)
    api_prefix: str | None
    encrypt_key: str = Field(...)
    proxy: str | None
    sentry: SentryConfig
    discord: DiscordConfig
    auth: AuthConfig
    logging: dict
