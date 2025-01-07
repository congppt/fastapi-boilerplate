from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.models import Entity


class SystemFunction(Entity):
    __tablename__ = 'SYSTEM_FUNCTION'
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('SYSTEM_FUNCTION.id'), nullable=True)
    description: Mapped[str]
    path: Mapped[str]

    #relationship
