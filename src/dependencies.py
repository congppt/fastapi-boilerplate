from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from db import aget_db
from middlewares.auth import CurrentUser

Database = Annotated[AsyncSession, Depends(aget_db)]

def get_current_user(request: Request) -> CurrentUser | None:
    """
    Get current user of request
    :param request: Request object
    :return: Current user
    """
    return request.user


Client = Annotated[CurrentUser, Depends(get_current_user)]
