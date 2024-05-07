from controllers.product import ProductController
from flask import Blueprint, g, session, render_template, request, flash, redirect, url_for

from routes.user import login_required, logged_in
from schemas.product import Product
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'jpeg', 'jpg', 'png', 'gif'}

product_description_blueprint = Blueprint("product_description", __name__, url_prefix="/product-description")
add_product_blueprint = Blueprint("add_product", __name__, url_prefix="/add-item")
remove_form_blueprint = Blueprint("remove_form", __name__, url_prefix="/remove")
remove_product_blueprint = Blueprint("remove_product", __name__, url_prefix="/remove_item")


@product_description_blueprint.route("/")
@logged_in
def product_description():
    product_id = int(request.args.get('productId'))

    ses = g.session
    product_data = ProductController(ses).get_product_by_id(product_id)

    return render_template("productDescription.html", data=product_data, loggedIn=session["logged_in"],
                           firstName=session["first_name"], noOfItems=session["no_of_items"])


@add_product_blueprint.route("/", methods=["GET", "POST"])
@login_required
def add_item():
    if request.method == "POST":
        product_name = request.form['product-name']
        price = float(request.form['price'])
        description = request.form['description']
        stock = int(request.form['stock'])
        category_id = int(request.form['category'])
        file_name = ''

        image = request.files['image']
        if image and allowed_file(image.filename):
            file_name = secure_filename(image.filename)
            # image.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))  # TODO
        image_name = file_name

        try:
            ses = g.session
            ProductController(ses).insert_product(
                product_name,
                price,
                description,
                image_name,
                stock,
                category_id
            )
            flash("Item added successfully", "info")
        except Exception as e:
            flash(f"Error adding item: {e}", "error")

        return redirect(url_for('root.root'))


@remove_form_blueprint.route("/")
@login_required
def remove():
    ses = g.session
    products: list[Product] = ProductController(ses).get_products()
    return render_template('remove.html', data=products)


@remove_product_blueprint.route("/")
@login_required
def remove_item():
    product_id = int(request.args.get('productId'))
    try:
        ses = g.session
        ProductController(ses).remove_product_by_id(product_id)
        flash("Product removed successfully", "info")
    except Exception as e:
        flash(f"Error removing product: {e}", "error")

    return redirect(url_for('root.root'))


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
