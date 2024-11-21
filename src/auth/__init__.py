from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schema import AuthRequest, AuthResponse
from dependencies import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(path="", response_model=AuthResponse, summary="Login")
async def alogin(request: AuthRequest, db: AsyncSession = Depends(get_db)):
    pass

@router.get(path="/refresh", response_model=AuthResponse, summary="Refresh token")
async def arefresh(refresh_token: str, db: AsyncSession = Depends(get_db)):
    pass