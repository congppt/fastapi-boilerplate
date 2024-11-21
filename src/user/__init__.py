from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from user.schema import UserCreateRequest

router = APIRouter(prefix="/user", tags=["user"])

@router.post(path="", summary="Create user")
async def acreate_user(request: UserCreateRequest, db: AsyncSession = Depends(get_db)):
    pass