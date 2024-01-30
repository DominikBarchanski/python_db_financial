from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class ProductsList(Base):
    __tablename__ = "products_list"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Integer, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="products_list")
    group_id = Column(Integer, ForeignKey("user_groups.id"))
    group = relationship("UserGroups", back_populates="products_list")
    category_id = Column(Integer, ForeignKey("product_category.id"))
    category = relationship("ProductCategory", back_populates="products_list")