from pydantic import BaseModel


class ExpenseBase(BaseModel):
    group_id: int
    user_id: int
    amount: int
    price: float
    name: str
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ExpenseCreate(ExpenseBase):
    datetime: str
    pass


class Expense(ExpenseBase):
    id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
