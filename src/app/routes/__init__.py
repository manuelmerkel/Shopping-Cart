from flask import Flask

from .admin import admin_area_blueprint, admin_product_info_blueprint, admin_orders_info_blueprint
from .cart import remove_from_cart_blueprint, cart_blueprint, add_item_cart_blueprint, checkout_blueprint
from .category import display_category_blueprint, add_category_form_blueprint, root_blueprint
from .orders import orders_blueprint
from .product import product_description_blueprint, add_product_blueprint, remove_form_blueprint, \
    remove_product_blueprint
from .user import change_pw_blueprint, profile_blueprint, register_user_blueprint, \
    update_profile_blueprint, login_blueprint, login_form_blueprint, logout_blueprint, registration_form_blueprint, \
    profile_home_blueprint


def register(app: Flask) -> None:
    # User blueprints
    app.register_blueprint(change_pw_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(update_profile_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(login_form_blueprint)
    app.register_blueprint(register_user_blueprint)
    app.register_blueprint(logout_blueprint)
    app.register_blueprint(registration_form_blueprint)
    app.register_blueprint(profile_home_blueprint)

    # Product blueprints
    app.register_blueprint(product_description_blueprint)
    app.register_blueprint(add_product_blueprint)
    app.register_blueprint(remove_form_blueprint)
    app.register_blueprint(remove_product_blueprint)

    # Order blueprints
    app.register_blueprint(orders_blueprint)

    # Category blueprints
    app.register_blueprint(display_category_blueprint)
    app.register_blueprint(add_category_form_blueprint)
    app.register_blueprint(root_blueprint)

    # Cart blueprints
    app.register_blueprint(remove_from_cart_blueprint)
    app.register_blueprint(cart_blueprint)
    app.register_blueprint(add_item_cart_blueprint)
    app.register_blueprint(checkout_blueprint)

    # Admin blueprints
    app.register_blueprint(admin_area_blueprint)
    app.register_blueprint(admin_product_info_blueprint)
    app.register_blueprint(admin_orders_info_blueprint)

