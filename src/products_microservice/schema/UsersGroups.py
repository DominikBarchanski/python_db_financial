from pydantic import BaseModel
from typing import List

from models.User import User


class UsersGroupsBase(BaseModel):
    name: str
    owner_id: int

    class Config:
        arbitrary_types_allowed = True


class UsersGroupsCreate(UsersGroupsBase):
    pass


class UsersGroups(UsersGroupsBase):
    id: int
    users: List[User] = []

    class Config:
        orm_mode = True
