from src.app.models.order_item import OrderItem as OrderItemModel

from .base import Controller


class OrderItemController(Controller[OrderItemModel]):

    def add_order_item(self, order_id: int, product_id: int, quantity: int):
        try:
            new_order_item = OrderItemModel(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity,
            )
            self.session.add(new_order_item)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
