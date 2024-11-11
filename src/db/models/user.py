from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.entity import Entity


class User(Entity):
    id: Mapped[int] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    #relationship