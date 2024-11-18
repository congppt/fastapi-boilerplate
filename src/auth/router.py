from fastapi import APIRouter

from auth.schema import AuthRequest
from dependencies import DBDep

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("")
async def alogin(request: AuthRequest, db: DBDep):
    pass

@auth_router.get("/refresh")
async def arefresh(refresh_token: str, db: DBDep):
    pass