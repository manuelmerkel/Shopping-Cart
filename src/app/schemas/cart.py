from pydantic import BaseModel, ConfigDict


class CartCreate(BaseModel):
    user_id: int
    product_id: int


class Cart(CartCreate):
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class CartUpdate(BaseModel):
    user_id: int
    product_id: int
