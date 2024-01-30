from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class ProductCategory(Base):
    __tablename__ = "product_category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    products_list = relationship("ProductsList", back_populates="category")
