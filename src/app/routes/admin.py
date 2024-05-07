from flask import Blueprint, session, redirect, url_for, render_template, flash, g

from controllers import OrderController
from routes.user import login_required

admin_area_blueprint = Blueprint("admin_area", __name__, url_prefix="/admin")
admin_product_info_blueprint = Blueprint("admin_product_info", __name__, url_prefix="/admin/products")
admin_orders_info_blueprint = Blueprint("admin_orders_info", __name__, url_prefix="/admin/orders")


@admin_area_blueprint.route("/")
@login_required
def admin_area():
    first_name = session["first_name"]
    if "admin" not in first_name:
        flash("You are not an admin", "warning")
        return redirect(url_for('root.root'))
    return render_template('adminArea.html', firstName=first_name, noOfItems=session["no_of_items"],
                           loggedIn=session["logged_in"])


@admin_product_info_blueprint.route("/")
@login_required
def admin_available_products_statistics():
    # TODO
    return redirect(url_for('root.root'))


@admin_orders_info_blueprint.route("/")
def admin_orders_statistics():
    ses = g.session
    orders = OrderController(ses).get_orders_with_product_info()

    dynamic_data_table = get_dynamic_table(orders)

    return render_template("adminOrderStats.html", cloumnHeaders=dynamic_data_table[0],
                           tableValues=dynamic_data_table[1:],
                           firstName=session["first_name"], noOfItems=session["no_of_items"],
                           loggedIn=session["logged_in"])


def get_dynamic_table(orders: list[list[str]]) -> list[list[str]]:
    if orders is []:
        flash(f"No order found, {f'{session["first_name"]}'}. Date: {f'{datetime.time}'}", "info")
        return orders

    allProducts: set = set()
    allOrders: dict = {}
    current_item: str = ""

    for order_item_id, order_id, product_name in orders:
        if product_name not in allProducts:
            allProducts.add(product_name)

        if order_id in allOrders:
            if product_name in allOrders[order_id]:
                allOrders[order_id][product_name] = allOrders[order_id][product_name] + 1
            elif product_name not in allOrders[order_id]:
                allOrders[order_id][product_name] = 1
        else:
            allOrders[order_id] = {product_name: 1}

    allProducts = sorted(allProducts)
    all_headers: list[int] = ["Order ID"] + [d for d in allProducts]

    dynamic_table: list[list[str]] = []
    dynamic_table.append(all_headers)

    for row in sorted(allOrders, key=int):  # int to sort tables ascending
        list: list[any] = []
        list.append((row))
        for i in range(1, len(all_headers)):
            current_product = all_headers[i]
            if (current_product in allOrders[(row)]):
                list.append(str(allOrders[(row)][current_product]))
            else:
                list.append('0')
        dynamic_table.append(list)

    # for row in dynamicTable:
    #     print(row)

    for row in dynamic_table[1:]:
        row_total = sum(map(int, row[1:]))
        row.append(str(row_total))

    all_headers.append("Total")
    total_row = ["Total"]

    for indx, column in enumerate(zip(*dynamic_table[1:])):
        if indx == 1:
            continue
        total_row.append(str(sum(map(int, column))))
    dynamic_table.append(total_row)

    return dynamic_table if not len(dynamic_table) <= 1 else []
