from datetime import datetime, timedelta
from schemas.User import User
from pydantic import BaseModel


class TokensBase(BaseModel):
    token: str
    expires_at: datetime

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class TokensCreate(TokensBase):
    user_id: int


class Tokens(TokensBase):
    id: int
    user: User

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
