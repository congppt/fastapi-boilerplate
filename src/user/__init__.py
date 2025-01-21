from datetime import datetime
from typing import Annotated
from uuid import uuid4
from fastapi import APIRouter, Query

from db.models.user import User
from dependencies import Database
from user.schema import UserCreateRequest
from user import handler
from utils.schema import QueryRequest

router = APIRouter(prefix="/user", tags=["user"])


@router.post(path="/", summary="Create user")
async def acreate_user(request: UserCreateRequest, db: Database):
    return await handler.acreate_user(request=request, db=db)


@router.post(path="/batch-create", summary="Batch create user")
async def abatch_create_user(db: Database):
    users = []
    for i in range(10):
        user = await handler.acreate_user(
            request=UserCreateRequest(
                username=f"{uuid4()}",
                password=f"password{i}",
                name=f"name{datetime.now():%Y%m%d}",
            ),
            db=db,
        )
        users.append(user)
    return users


@router.get(path="/", summary="Get users")
async def aget_users(db: Database, request: Annotated[QueryRequest[User], Query()]):
    return await handler.aget_users(db=db, request=request)
