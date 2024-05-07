from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    product_name: str
    price: float
    description: str
    image: str
    stock: int
    category_id: int


class Product(ProductCreate):
    product_id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class ProductUpdate(ProductCreate):
    pass
