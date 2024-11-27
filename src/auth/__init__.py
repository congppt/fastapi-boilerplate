from fastapi import APIRouter

from auth.schema import AuthRequest, AuthResponse
from dependencies import Database

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(path="", response_model=AuthResponse, summary="Login")
async def alogin(request: AuthRequest, db: Database):
    pass


@router.get(path="/refresh", response_model=AuthResponse, summary="Refresh token")
async def arefresh(refresh_token: str, db: Database):
    pass
