from fastapi import APIRouter

from dependencies import DBDep
from user.schema import UserCreateRequest

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.post("")
async def acreate_user(request: UserCreateRequest, db: DBDep):
    pass