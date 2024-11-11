from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base_entity import BaseEntity


class User(BaseEntity):
    id: Mapped[int] = mapped_column(primary_key=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    #relationship