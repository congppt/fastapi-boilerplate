from datetime import datetime
from email.policy import default

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Entity(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(default=func.now)
    created_by: Mapped[str] = mapped_column(default='DEV')
    updated_at: Mapped[datetime] = mapped_column(default=func.now, onupdate=func.now)
    updated_by: Mapped[str] = mapped_column(default='DEV')