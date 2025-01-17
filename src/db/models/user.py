from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models import Entity


class User(Entity):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    name: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    # relationship
