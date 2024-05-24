from flask import Blueprint, g, session, render_template

from src.app.controllers.orders import OrderController
from src.app.routes.user import login_required

orders_blueprint = Blueprint("orders", __name__, url_prefix="/account/orders")


@orders_blueprint.route("/")
@login_required
def orders_view():
    ses = g.session
    orders_from_user = OrderController(ses).get_order_by_user_id(session["user_id"])
    return render_template('orderView.html', orders=orders_from_user, user_id=session["user_id"],
                           loggedIn=session["logged_in"], firstName=session["first_name"],
                           noOfItems=session["no_of_items"])
