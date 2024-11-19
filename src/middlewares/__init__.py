from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from .auth import AuthMiddleware
from .log import  LogMiddleware
middlewares: set = {
    (CORSMiddleware, {
        "allow_origins": ("*",),
        "allow_methods": ("*",),
        "allow_headers": ("*",),
        "allow_credentials": True,
    }),
    LogMiddleware,
    (AuthenticationMiddleware, {"backend": AuthMiddleware})
}