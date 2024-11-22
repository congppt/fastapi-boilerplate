from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, foreign

from db.models import Entity


class SystemFunction(Entity):
    __tablename__ = 'SYSTEM_FUNCTION'
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('SYSTEM_FUNCTION.id'), nullable=True)
    description: Mapped[str]
    path: Mapped[str]

    #relationship

class SystemConfig(Entity):
    __tablename__ = 'SYSTEM_CONFIG'
    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[Any] = mapped_column(JSONB)
