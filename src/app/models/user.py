from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import CreatedUpdatedAtMixin


class User(CreatedUpdatedAtMixin):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str]
    email: Mapped[str | None]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    address1: Mapped[str | None]
    address2: Mapped[str | None]
    zipcode: Mapped[str | None]
    city: Mapped[str | None]
    state: Mapped[str | None]
    country: Mapped[str | None]
    phone: Mapped[str | None]

    cart = relationship("Cart", back_populates="user")
    order = relationship("Order", back_populates="user")
