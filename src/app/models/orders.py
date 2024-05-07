from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import CreatedUpdatedAtMixin


class Order(CreatedUpdatedAtMixin):
    __tablename__ = 'orders'

    order_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    total: Mapped[float]

    user = relationship("User", back_populates="order")
    order_item = relationship("OrderItem", back_populates="order")
