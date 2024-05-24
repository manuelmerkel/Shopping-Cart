import hashlib
from functools import wraps

from flask import Blueprint, g, session, render_template, request, flash, redirect, url_for

from src.app.controllers.cart import CartController
from src.app.controllers.user import UserController
from src.app.schemas.user import User

change_pw_blueprint = Blueprint("change_password", __name__, url_prefix="/account/profile/change-password")
profile_blueprint = Blueprint("profile", __name__, url_prefix="/account/profile/edit")
update_profile_blueprint = Blueprint("update_profile", __name__, url_prefix="/update-profile")
login_blueprint = Blueprint("login", __name__, url_prefix="/login")
login_form_blueprint = Blueprint("login_form", __name__, url_prefix="/login-form")
logout_blueprint = Blueprint("logout", __name__, url_prefix="/logout")
register_user_blueprint = Blueprint("register", __name__, url_prefix="/register")
registration_form_blueprint = Blueprint("register_form", __name__, url_prefix="/registration-form")
profile_home_blueprint = Blueprint("profile_home", __name__, url_prefix="/account/profile")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            flash("Please log in", "info")
            return redirect(url_for('root.root'))
        return f(*args, **kwargs)
    return decorated_function


def logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            session["email"] = ""
            session["user_id"] = -1
            session["first_name"] = ""
            session["no_of_items"] = 0
            session["logged_in"] = False
        return f(*args, **kwargs)
    return decorated_function


@profile_blueprint.route("/")
@login_required
def edit_profile():
    ses = g.session
    profile = UserController(ses).get_user_by_email(session["email"])
    return render_template("editProfile.html", profileData=profile, loggedIn=session["logged_in"],
                           firstName=session["first_name"], noOfItems=session["no_of_items"])


@change_pw_blueprint.route("/", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        old_password = request.form['oldpassword']
        new_password = request.form['newpassword']
        old_password_hash = hashlib.md5(new_password.encode()).hexdigest()
        new_password_hash = hashlib.md5(old_password.encode()).hexdigest()

        ses = g.session
        controller = UserController(ses)
        user = controller.get_user_by_email(session["email"])

        if user.password == old_password_hash:
            try:
                controller.update_password(session["email"], new_password_hash)
                flash('Changed Successfully', 'info')
            except Exception as e:
                flash(f'Error changeing password: {e}', 'error')
        else:
            flash('Wrong password', 'warning')

    return render_template("changePassword.html")


@update_profile_blueprint.route("/", methods=["GET", "POST"])
@login_required
def update_profile():
    email = request.form['email']
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    address1 = request.form['address1']
    address2 = request.form['address2']
    zipcode = request.form['zipcode']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    phone = request.form['phone']

    try:
        ses = g.session
        UserController(ses).update_profile(
            email,
            first_name,
            last_name,
            address1,
            address2,
            zipcode,
            city,
            state,
            country,
            phone
        )
    except Exception as e:
        flash(f'Error on updating profile: {e}', 'error')
    return redirect(url_for('root.root'))


@register_user_blueprint.route("/", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']

        try:
            ses = g.session
            UserController(ses).insert_user(
                email,
                hashlib.md5(password.encode()).hexdigest(),
                first_name,
                last_name,
                address1,
                address2,
                zipcode,
                city,
                state,
                country,
                phone
            )
            flash('Registered Successfully', 'info')
        except Exception as e:
            flash(f'Error on inserting new user: {e}', 'error')

        return render_template("login.html")


@registration_form_blueprint.route("/")
def registration_form():
    return render_template("register.html")


@login_blueprint.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        if is_valid_login(email, password):
            ses = g.session
            user = UserController(ses).get_user_by_email(email)
            session["email"] = user.email
            session["user_id"] = user.user_id
            session["first_name"] = user.first_name
            session["no_of_items"] = CartController(ses).count_items(user.user_id)
            session["logged_in"] = True
        else:
            flash("Invalid UserId / Password", "error")
            return render_template('login.html')

        return redirect(url_for('root.root'))


@login_form_blueprint.route("/")
def login_form():
    if session['email'] != "":
        return redirect(url_for('root.root'))
    else:
        return render_template('login.html')


@logout_blueprint.route("/")
def logout():
    session.pop('email', None)
    session.pop('user_id', None)
    session.pop('first_name', None)
    session.pop('no_of_items', None)
    session.pop('logged_in', None)
    return redirect(url_for('root.root'))


@profile_home_blueprint.route("/")
@login_required
def profile_home():
    return render_template("profileHome.html", loggedIn=session["logged_in"], firstName=session["first_name"],
                           noOfItems=session["no_of_items"])


def is_valid_login(email: str, password: str) -> bool:
    ses = g.session
    users: list[User] = UserController(ses).list_users()

    for user in users:
        if user.email == email and user.password == hashlib.md5(password.encode()).hexdigest():
            return True

    return False
