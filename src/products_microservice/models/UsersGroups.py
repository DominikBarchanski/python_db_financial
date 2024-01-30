from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class UserGroups(Base):
    __tablename__ = "user_groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="groups")
    members = relationship("UserGroupMembership", back_populates="group")
    expenses = relationship("Expense", back_populates="group")
    balances = relationship("Balance", back_populates="group")
    products_list = relationship("ProductsList", back_populates="group")
