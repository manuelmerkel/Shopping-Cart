from typing import Any, Sequence

from pydantic import TypeAdapter
from sqlalchemy import select, and_, func, Row, RowMapping

from models.cart import Cart as CartModel
from models.product import Product as ProductModel
from schemas.cart import Cart as CartSchema
from .base import Controller


class CartController(Controller[CartModel]):

    def get_cart_by_user_id(self, user_id: int) -> Sequence[Row[Any] | RowMapping | Any]:
        stmt = select(CartModel).where(CartModel.user_id == user_id)
        return self.session.scalars(stmt).fetchall()

    def get_cart_item_from_user(self, user_id: int, product_id) -> Row | RowMapping | None:
        stmt = select(CartModel).where(and_(CartModel.user_id == user_id, CartModel.product_id == product_id))
        return self.session.scalars(stmt).one_or_none()

    def count_items(self, user_id: int) -> int:
        cart: list[CartSchema] = TypeAdapter(list[CartSchema]).validate_python(self.get_cart_by_user_id(user_id))
        return len(cart)

    def clear_cart_by_user_id(self, user_id: int) -> None:
        cart_items = self.get_cart_by_user_id(user_id)
        for cart_item in cart_items:
            try:
                self.session.delete(cart_item)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                raise e

    def remove_product_from_user_cart(self, user_id: int, product_id: int) -> None:
        cart_item = self.get_cart_item_from_user(user_id, product_id)

        if cart_item is None:
            raise ValueError("The product is not in cart")

        try:
            self.session.delete(cart_item)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def add_item_for_user(self, user_id, product_id) -> None:
        try:
            new_item = CartModel(
                user_id=user_id,
                product_id=product_id,
            )
            self.session.add(new_item)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def get_cart_with_product_info_by_user_id(self, user_id: int) -> list:
        # TODO hier kann man das noch schöner machen
        stmt = select(CartModel, ProductModel)\
            .join(ProductModel, ProductModel.product_id == CartModel.product_id)\
            .where(CartModel.user_id == user_id)
        cart_with_products = self.session.execute(stmt).fetchall()
        cart_with_products = TypeAdapter(list).validate_python(cart_with_products)

        combined_results = []
        for cart, product in cart_with_products:
            combined_result = {
                'user_id': cart.user_id,
                'product_id': product.product_id,
                'product_name': product.product_name,
                'description': product.description,
                'image': product.image,
                'price': product.price,
                'stock': product.stock
            }
            combined_results.append(combined_result)
        return combined_results

    def get_order_with_product_info(self, user_id: int) -> list:
        # TODO hier kann man das noch schöner machen
        stmt = select(CartModel.product_id, func.count(CartModel.product_id).label("quantity"),
                      func.sum(ProductModel.price).label("total")) \
            .join(ProductModel, ProductModel.product_id == CartModel.product_id) \
            .where(CartModel.user_id == user_id) \
            .group_by(CartModel.product_id)  # TODO
        order_with_product_info = self.session.execute(stmt).fetchall()
        order_with_product_info = TypeAdapter(list).validate_python(order_with_product_info)

        combined_results = []
        for product_id, quantity, total in order_with_product_info:
            combined_result = {
                'product_id': product_id,
                'quantity': quantity,
                'total': total,
            }
            combined_results.append(combined_result)
        return combined_results
