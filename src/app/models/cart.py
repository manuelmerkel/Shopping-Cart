from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import CreatedUpdatedAtMixin


class Cart(CreatedUpdatedAtMixin):
    __tablename__ = 'cart'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.product_id"), primary_key=True)

    user = relationship("User", back_populates="cart")
    product = relationship("Product", back_populates="cart")
