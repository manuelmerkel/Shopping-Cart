from pprint import pprint

from pydantic import TypeAdapter
from sqlalchemy import select

from models.product import Product as ProductModel
from schemas.product import Product as ProductSchema
from .base import Controller


class ProductController(Controller[ProductModel]):

    def get_products(self) -> list[ProductSchema]:
        stmt = select(ProductModel)
        products = self.session.scalars(stmt).fetchall()
        return TypeAdapter(list[ProductSchema]).validate_python(products)

    def get_product_by_id(self, product_id: int) -> ProductSchema:
        stmt = select(ProductModel).where(ProductModel.product_id == product_id)
        product = self.session.scalars(stmt).one_or_none()

        if product is None:
            raise ValueError("No product found for this product id")

        return TypeAdapter(ProductSchema).validate_python(product)

    def insert_product(self, product_name: str, price: float, description: str, file_name: str, stock: int, category_id: int) -> None:
        try:
            new_product = ProductModel(
                name=product_name,
                price=price,
                description=description,
                image=file_name,
                stock=stock,
                category_id=category_id,
            )

            self.session.add(new_product)
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e

    def remove_product_by_id(self, product_id: int) -> None:
        product = self.get_product_by_id(product_id)
        try:
            self.session.delete(product)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def update_stock_for_product(self, product_id: int, quantity_to_subtract: int) -> None:
        product = self.get_product_by_id(product_id)

        try:
            product.stock = product.stock - quantity_to_subtract
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

