from fastapi import APIRouter, Depends

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
        users.append(
            await handler.acreate_user(
                request=UserCreateRequest(
                    username=f"user{i}", password=f"password{i}", name=f"name{i}"
                ),
                db=db,
            )
        )
    return users


@router.get(path="/", summary="Get users")
async def aget_users(db: Database, request: QueryRequest = Depends()):
    return await handler.aget_users(db=db, request=request)
