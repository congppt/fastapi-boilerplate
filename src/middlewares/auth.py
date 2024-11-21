from typing import Any

import jwt
from fastapi import status, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.authentication import BaseUser, AuthenticationBackend, AuthCredentials, AuthenticationError
from fastapi.requests import HTTPConnection

from auth.schema import UserClaim
from constants.app import AUTH_SCHEME, AUTH_ALGO, USER_CLAIM
from constants.cache import CURRENT_USER_KEY
from constants.env import ACCESS_SECRET
from db import cache, aget_db
from db.models.user import User


class CurrentUser(BaseModel, BaseUser):
    id: int | None
    is_active: bool = False
    model_config = ConfigDict(from_attributes=True)

    @property
    def is_authenticated(self) -> bool:
        return self.id is not None


def get_payload(token: str, secret: str) -> dict[str: Any]:
    """
    Retrieve payload from JWT
    :param token: JWT token
    :param secret: Secret used to encrypt JWT
    :return: payload
    """
    try:
        payload = jwt.decode(jwt=token, key=secret, algorithms=[AUTH_ALGO])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Phiên đăng nhập đã kết thúc")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Không thể xác thực thông tin người dùng")


class AuthMiddleware(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> tuple[AuthCredentials, BaseUser] | None:
        async for db in aget_db():
            conn.state.db = db
            auth_header = conn.get('Authorization')
            if not auth_header:
                return
            scheme, token = auth_header.split()
            if scheme.lower() != AUTH_SCHEME or not token:
                raise AuthenticationError("Không thể xác thực thông tin người dùng")
            user = await self.aget_current_user(token=token, db=db)
            await self.acheck_permission(user=user)

            return AuthCredentials(['authenticated']), user

    async def aget_current_user(self, token: str, db: AsyncSession) -> CurrentUser | None:
        """
        Retrieve user info if authorization data is valid
        :param token: Token used for authentication
        :param db: Database session
        :return: Current user
        """
        payload = get_payload(token=token, secret=ACCESS_SECRET)
        user_claim = UserClaim(**payload.get(USER_CLAIM))
        user = await self.aget_active_user(user_id=user_claim.id, db=db)
        return user

    @staticmethod
    async def aget_active_user(user_id: int, db: AsyncSession) -> CurrentUser:
        """
        Retrieve user info if user is active
        :param user_id: User identifier
        :param db: Database session
        :return: Current user
        """
        key = CURRENT_USER_KEY.format(user_id)
        current_user = cache.aget(key=key, model=CurrentUser)
        if not current_user:
            query = select(User).where(User.id == user_id)
            user = await db.scalar(statement=query)
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail="Không thể xác thực thông tin người dùng")
            current_user = CurrentUser(**vars(user))
        if not current_user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Tài khoản đã bị đình chỉ")
        return current_user

    @staticmethod
    async def acheck_permission(user: CurrentUser | None) -> None:
        pass
