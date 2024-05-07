from pydantic import BaseModel, ConfigDict


class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int


class OrderItem(OrderItemCreate):
    order_item_id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class OrderItemUpdate(OrderItemCreate):
    pass
