from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from db.database import aget_db

DBDep = Annotated[AsyncSession, Depends(aget_db)]