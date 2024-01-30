from pydantic import BaseModel
from .User import User
from typing import Dict
class UserGroupMembershipBase(BaseModel):
    id: int
    user_id: int
    group_id: int
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserGroupMembershipCreate(UserGroupMembershipBase):
    pass


class UserGroupMembership(UserGroupMembershipBase):
    id: int
    user_id: int
    group_id: int
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserGroupMembershipSchema(BaseModel):
    id: int
    user_id: int
    group_id: int
    name: str

    class Config:
        orm_mode = True


class UserGroupMembershipAddSchema(BaseModel):
    group_id: int
    email: str

    class Config:
        orm_mode = True

class UserGroupMembershipList(BaseModel):
    id: int
    group_id: int
    name: str
    user_id: int
    user: Dict[str, str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True