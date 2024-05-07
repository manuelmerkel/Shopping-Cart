from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import CreatedUpdatedAtMixin


class OrderItem(CreatedUpdatedAtMixin):
    __tablename__ = 'order_items'

    order_item_id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    quantity: Mapped[int]

    order = relationship("Order", back_populates="order_item")
    product = relationship("Product", back_populates="order_item")
