from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schema import AuthRequest, AuthResponse
from dependencies import get_db

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("", response_model=AuthResponse)
async def alogin(request: AuthRequest, db: AsyncSession = Depends(get_db)):
    pass

@auth_router.get("/refresh", response_model=AuthResponse)
async def arefresh(refresh_token: str, db: AsyncSession = Depends(get_db)):
    pass