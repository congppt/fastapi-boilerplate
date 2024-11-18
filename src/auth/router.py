from fastapi import APIRouter

from auth.schema import AuthRequest
from dependencies import DBDep

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/login")
async def login(request: AuthRequest, db: DBDep):
    pass

@auth_router.get("/refresh")
async def refresh(refresh_token: str, db: DBDep):
    pass