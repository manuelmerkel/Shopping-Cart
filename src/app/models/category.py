from .base import CreatedUpdatedAtMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Category(CreatedUpdatedAtMixin):
    __tablename__ = 'categories'

    category_id: Mapped[int] = mapped_column(primary_key=True)
    category_name: Mapped[str]

    product = relationship("Product", back_populates="category")
