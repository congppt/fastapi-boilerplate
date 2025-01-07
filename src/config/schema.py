from pydantic import BaseModel, Field, PositiveInt, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, JsonConfigSettingsSource


class SMTPSettings(BaseModel):
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = False
    start_tls: bool = True


class SentrySettings(BaseModel):
    dsn: str = Field(...)
    traces_sample_rate: float = Field(ge=0.0, le=1.0)
    sample_rate: float = Field(ge=0.0, le=1.0)
    profiles_sample_rate: float = Field(ge=0.0, le=1.0)


class DiscordSettings(BaseModel):
    base_url: str = Field(...)
    notification_path: str = Field(...)


class AuthSettings(BaseModel):
    access_secret: str = Field(min_length=32)
    refresh_secret: str = Field(min_length=32)
    access_exp_minutes: PositiveInt
    refresh_exp_minutes: PositiveInt


class MinIOSettings(BaseModel):
    host: str = Field(...)
    access: str = Field(...)
    secret: str = Field(...)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(json_file='appsettings.json')
    env: str = Field(...)
    postgres_dsn:  PostgresDsn = Field(...)
    redis_dsn: RedisDsn = Field(...)
    api_prefix: str | None
    encrypt_key: str = Field(..., min_length=32)
    proxy: str | None
    auth: AuthSettings
    smtp: SMTPSettings
    minio: MinIOSettings
    logging: dict
    sentry: SentrySettings
    discord: DiscordSettings

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ):
        return (JsonConfigSettingsSource(settings_cls),)

    @property
    def of_local_env(self):
        return self.env != 'production' and self.env != 'test'
    def of_production_env(self):
        return self.env == 'production'