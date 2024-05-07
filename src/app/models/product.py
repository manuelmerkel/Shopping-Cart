from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import CreatedUpdatedAtMixin


class Product(CreatedUpdatedAtMixin):
    __tablename__ = 'products'

    product_id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str]
    price: Mapped[float]
    description: Mapped[str]
    image: Mapped[str]
    stock: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.category_id"))

    category = relationship("Category", back_populates="product")
    cart = relationship("Cart", back_populates="product")
    order_item = relationship("OrderItem", back_populates="product")
