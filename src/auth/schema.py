from pydantic import BaseModel, ConfigDict


class AuthRequest(BaseModel):
    pass
class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    model_config = ConfigDict(from_attributes=True)

class UserClaim(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)
    pass