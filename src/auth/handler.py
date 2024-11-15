from datetime import timedelta, datetime
from typing import Any

import jwt
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.schema import CurrentUser, PayloadData
from constants.app import AUTH_ALGO, AUTH_SCHEME
from constants.cache import CURRENT_USER_KEY
from constants.env import ACCESS_SECRET
from db import cache
from db.models.user import User
from src.utils.json_handler import CustomJSONEncoder


def __create_token(payload: dict, secret: str, exp_after: timedelta) -> str:
    """Generate JWT"""
    exp = datetime.now() + exp_after
    payload.update({"exp": exp})
    return jwt.encode(exp, secret, AUTH_ALGO, json_encoder=CustomJSONEncoder)

async def aget_request_user(auth_header: str, db: AsyncSession) -> CurrentUser:
    """Retrieve user info if authorization data is valid"""
    if not auth_header:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Không thể xác thực thông tin người dùng")
    scheme, token = auth_header.split()
    if scheme.lower() != AUTH_SCHEME:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Không thể xác thực thông tin người dùng")
    payload = get_payload(token, ACCESS_SECRET)
    payload_data = PayloadData(**payload)
    user_id = payload_data.user_id
    user = await aget_active_user(user_id, db)
    return user


def get_payload(token: str, secret: str) -> dict[str: Any]:
    """Retrieve payload from JWT"""
    try:
        payload = jwt.decode(token, secret, algorithms=[AUTH_ALGO])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Phiên đăng nhập đã kết thúc")
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,"Không thể xác thực thông tin người dùng")

async def aget_active_user(user_id: int, db: AsyncSession) -> CurrentUser:
    """Retrieve user info if user is active"""
    key = CURRENT_USER_KEY.format(user_id)
    current_user = cache.aget(key, CurrentUser)
    if not current_user:
        query = select(User).where(User.id == user_id)
        user = await db.scalar(query)
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Không thể xác thực thông tin người dùng")
        current_user = CurrentUser(**vars(user))
    if not current_user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Tài khoản đã bị đình chỉ")
    return current_user

async def acheck_permission(user: CurrentUser, path: str) -> None:
    pass

