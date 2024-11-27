from fastapi import APIRouter

from dependencies import Database
from user.schema import UserCreateRequest

router = APIRouter(prefix="/user", tags=["user"])


@router.post(path="", summary="Create user")
async def acreate_user(request: UserCreateRequest, db: Database):
    pass
