from .base import Base
from .UsersGroups import UserGroups
from .Tokens import Tokens
from .UserGroupMembership import UserGroupMembership
from .Expenses import Expense
from .Balance import Balance
from .ProductsList import ProductsList
from .ProductCategory import ProductCategory
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String)
    groups = relationship("UserGroups", back_populates="owner")
    tokens = relationship("Tokens", back_populates="user")
    memberships = relationship("UserGroupMembership", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    balances = relationship("Balance", back_populates="user")
    products_list = relationship("ProductsList", back_populates="user")