from pydantic import BaseModel


class AuthRequest(BaseModel):
    pass
class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class UserClaim(BaseModel):
    id: int