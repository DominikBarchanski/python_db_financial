from pydantic import BaseModel


class ProductCategoryBase(BaseModel):
    id: int
    name: str


    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ProductListCreate(ProductCategoryBase):
    pass


class ProductCategory(ProductCategoryBase):
    id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
