from pprint import pprint

from pydantic import TypeAdapter
from sqlalchemy import select

from models import orders
from models.orders import Order as OrderModel
from schemas.orders import Order as OrderSchema
from models.order_item import OrderItem as OrderItemModel
from models.product import Product as ProductModel
from .base import Controller


class OrderController(Controller[OrderModel]):

    def get_orders(self) -> list[OrderSchema]:
        stmt = select(OrderModel)
        orders = self.session.scalars(stmt).fetchall()
        return TypeAdapter(list[OrderSchema]).validate_python(orders)

    def get_order_by_user_id(self, user_id: int) -> list[OrderSchema]:
        stmt = select(OrderModel).where(OrderModel.user_id == user_id)
        order = self.session.scalars(stmt).fetchall()
        return TypeAdapter(list[OrderSchema]).validate_python(order)

    def insert_order_by_user_id(self, user_id: int, total: float) -> int:
        try:
            new_order = OrderModel(
                user_id=user_id,
                total=total
            )
            self.session.add(new_order)
            self.session.commit()
            return new_order.order_id
        except Exception as e:
            self.session.rollback()
            raise e

    def get_orders_with_product_info(self) -> list[list[str]]:
        stmt = select(OrderModel, OrderItemModel, ProductModel) \
            .join(OrderItemModel, OrderItemModel.order_id == OrderModel.order_id) \
            .join(ProductModel, ProductModel.product_id == OrderItemModel.product_id)
        orders_with_product_info = self.session.execute(stmt).fetchall()
        orders_with_product_info = TypeAdapter(list).validate_python(orders_with_product_info)

        combined_results = []
        for order, order_item, product in orders_with_product_info:
            combined_result = [
                str(order_item.order_item_id),
                str(order.order_id),
                str(product.product_name)
            ]

            combined_results.append(combined_result)

        return combined_results
