from datetime import timedelta, datetime

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schema import AuthRequest, AuthResponse
from config import APP_SETTINGS
from constants import AUTH_ALGO, AUTH_SCHEME, USER_CLAIM

from utils.serializer import CustomJSONEncoder

AUTH_SETTINGS = APP_SETTINGS.auth
def __create_token(payload: dict, secret: str, exp_after: timedelta):
    """
    Generate JWT
    :param payload: data that needs to be stored in token
    :param secret: secret to encrypt
    :param exp_after: token's lifetime in minutes
    """
    exp = datetime.now() + exp_after
    payload.update(m={"exp": exp})
    return jwt.encode(payload=payload, key=secret, algorithm=AUTH_ALGO, json_encoder=CustomJSONEncoder)

async def aauthenticate(request: AuthRequest, db: AsyncSession):
    """
    Authenticate & authorize user
    :param request: authentication data
    :param db: Database session
    :return: Authentication & authorization result
    """
    user_claim = None
    access_payload = {USER_CLAIM: user_claim}
    access_token = __create_token(
        payload=access_payload,
        secret=AUTH_SETTINGS.access_secret,
        exp_after=timedelta(minutes=AUTH_SETTINGS.access_exp_minutes)
    )
    refresh_payload = {USER_CLAIM: user_claim}
    refresh_token = __create_token(
        payload=refresh_payload,
        secret=AUTH_SETTINGS.refresh_secret,
        exp_after=timedelta(minutes=AUTH_SETTINGS.refresh_exp_minutes)
    )
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=AUTH_SCHEME
    )


