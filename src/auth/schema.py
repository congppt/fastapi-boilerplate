from pydantic import BaseModel, ConfigDict


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    model_config = ConfigDict(from_attributes=True)

class PayloadData(BaseModel):
    user_id: int
    model_config = ConfigDict(from_attributes=True)
    pass
class CurrentUser(BaseModel):
    user_id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
    pass