from pydantic import BaseModel, ConfigDict


class OrderCreate(BaseModel):
    user_id: int
    total: float


class Order(OrderCreate):
    order_id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class OrderUpdate(OrderCreate):
    pass
