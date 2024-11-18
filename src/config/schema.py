from pydantic import BaseModel, ConfigDict


class EmailServer(BaseModel):
    host: str
    port: int
    username: str
    password: str
    use_tls: bool = False
    start_tls: bool = True
    model_config = ConfigDict(from_attributes=True)