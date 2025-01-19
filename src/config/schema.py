from pydantic import BaseModel, Field, PositiveInt, PostgresDsn, RedisDsn
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)


class SMTPSettings(BaseModel):
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = False
    start_tls: bool = True


class SentrySettings(BaseModel):
    dsn: str = Field(default=...)
    traces_sample_rate: float = Field(ge=0.0, le=1.0)
    sample_rate: float = Field(ge=0.0, le=1.0)
    profiles_sample_rate: float = Field(ge=0.0, le=1.0)


class DiscordAPISettings(BaseModel):
    chatbot: str = Field(default=...)


class AuthSettings(BaseModel):
    access_secret: str = Field(min_length=32)
    refresh_secret: str = Field(min_length=32)
    access_exp_minutes: PositiveInt
    refresh_exp_minutes: PositiveInt


class MinIOSettings(BaseModel):
    host: str = Field(default=...)
    access: str = Field(default=...)
    secret: str = Field(default=...)


class AWSSettings(BaseModel):
    access: str = Field(default=...)
    secret: str = Field(default=...)
    region: str = Field(default=...)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(json_file="appsettings.json")
    env: str = Field(default=...)
    postgres_dsn: PostgresDsn = Field(default=...)
    redis_dsn: RedisDsn = Field(default=...)
    api_prefix: str | None
    encrypt_key: str = Field(default=..., min_length=32)
    proxy: str | None
    auth: AuthSettings
    smtp: SMTPSettings
    minio: MinIOSettings | None
    aws: AWSSettings | None
    logging: dict
    sentry: SentrySettings | None
    discord_api: DiscordAPISettings | None

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ):
        return (
            YamlConfigSettingsSource(
                settings_cls=settings_cls, yaml_file="../appsettings.yml"
            ),
        )

    @property
    def of_local_env(self):
        return self.env != "production" and self.env != "test"

    @property
    def of_production_env(self):
        return self.env == "production"
