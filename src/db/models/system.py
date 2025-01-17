from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models import Entity
from db.models.enum import FunctionType


class SystemFunctionGroup(Entity):
    __tablename__ = 'sys_func_group'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    #relationship
    functions: Mapped[list['SystemFunction']] = relationship(back_populates='group')
class SystemFunction(Entity):
    __tablename__ = 'SYSTEM_FUNCTION'
    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('sys_func_group.id'))
    description: Mapped[str]
    path: Mapped[str]
    type: Mapped[FunctionType] = mapped_column(Enum(FunctionType, native_enum=False, validate_strings=True))
    #relationship
    group: Mapped['SystemFunctionGroup'] = relationship(back_populates='functions')