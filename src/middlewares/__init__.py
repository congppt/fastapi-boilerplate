from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from middlewares.auth import AuthMiddleware
from middlewares.log import  LogMiddleware
middlewares: tuple = (
    (CORSMiddleware, {
        "allow_origins": ("*",),
        "allow_methods": ("*",),
        "allow_headers": ("*",),
        "allow_credentials": True,
    }),
    LogMiddleware,
    (AuthenticationMiddleware, {"backend": AuthMiddleware()}),
)