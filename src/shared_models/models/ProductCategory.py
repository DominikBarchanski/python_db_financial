from .base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class ProductCategory(Base):
    __tablename__ = "product_category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    products_list = relationship("ProductsList", back_populates="category")
