from pydantic import BaseModel, Field
from typing import Any, Annotated, Literal


class FormatterConfig(BaseModel):
    format: str | None
    datefmt: str | None
    style: Literal['%', '$', '{']
    validate: bool = True
    defaults: dict[str, Any] | None

class FilterConfig(BaseModel):
    name: str = ''
class HandlerConfig(BaseModel):
    class_: str = Field(alias="class")
    level: str | None
    formatter: str | None
    filters: tuple[str]
    filename: str | None
    maxBytes: int | None
    backupCount: int = None
    stream: str = None

class LoggerConfig(BaseModel):
    level: str
    handlers: tuple[str]
    propagate: bool = True

class LoggingConfig(BaseModel):
    version: int
    disable_existing_loggers: bool
    formatters: dict[str, FormatterConfig]
    filters: dict[str, FilterConfig]
    handlers: dict[str, HandlerConfig]
    root: LoggerConfig
    loggers: dict[str, LoggerConfig] = {}

