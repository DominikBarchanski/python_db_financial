from pydantic import BaseModel


class BalanceBase(BaseModel):
    user_id: int
    group_id: int
    balance: float

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BalanceCreate(BalanceBase):
    datetime: str
    pass


class Balance(BalanceBase):
    id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
