from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.annotation import Annotated

from middlewares.auth import CurrentUser


def get_db(request: Request) -> AsyncSession:
    """
    Get database session from request
    :param request: Request object
    :return: Database session
    """
    return request.state.db

DBDep = Annotated[AsyncSession, Depends(get_db)]

def get_current_user(request: Request) -> CurrentUser | None:
    """
    Get current user of request
    :param request: Request object
    :return: Current user
    """
    return request.state.user

CurrentUser = Annotated[CurrentUser, Depends(get_current_user)]