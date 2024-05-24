from pprint import pprint

from flask import Blueprint, g, render_template, request, session

from src.app.controllers.category import CategoryController
from src.app.controllers.product import ProductController
from src.app.routes.user import login_required, logged_in

display_category_blueprint = Blueprint("display_category", __name__, url_prefix="/display-category")
add_category_form_blueprint = Blueprint("add_category_form", __name__, url_prefix="/add")
root_blueprint = Blueprint("root", __name__)


@root_blueprint.route("/")
@logged_in
def root():
    ses = g.session
    products = ProductController(ses).get_products()
    categories = CategoryController(ses).get_categories()
    for item in products:
        pprint(vars(item))

    return render_template('home.html', itemData=products, loggedIn=session["logged_in"],
                           firstName=session["first_name"], noOfItems=session["no_of_items"], categoryData=categories)


@add_category_form_blueprint.route("/")
@login_required
def add_category_form():
    ses = g.session
    categories = CategoryController(ses).get_categories()
    return render_template('add.html', categories=categories)


@display_category_blueprint.route("/")
@logged_in
def display_category():
    category_id = int(request.args.get("categoryId"))
    ses = g.session
    categories_with_product = CategoryController(ses).get_category_with_product_info(category_id)
    return render_template('displayCategory.html', data=categories_with_product, loggedIn=session["logged_in"],
                           firstName=session["first_name"], noOfItems=session["no_of_items"],
                           categoryName=categories_with_product[0]["category_name"])

