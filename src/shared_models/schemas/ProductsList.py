from pydantic import BaseModel


class ProductsListBase(BaseModel):
    id: int
    name: str
    quantity: int
    user_id: int
    group_id: int
    category_id: int
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ProductsListCreate(ProductsListBase):
    pass


class ProductsList(ProductsListBase):
    id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
