from flask import Blueprint, render_template, redirect, url_for, session, abort
from jinja2 import TemplateNotFound

from helpers import customer_login_required
from auth_forms import RegisterForm, LoginForm, login_user, register_user
from models import Customer

customer_bp = Blueprint('customers', __name__)

@customer_bp.route('/')
@customer_login_required
def index():
    return render_template('customers/index.html')

@customer_bp.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_user(login_form, user_type="customer"):
            return url_for("index")
    else:
        return render_template("login.html", login_form=login_form, user="customer")

@customer_bp.route('/register', methods=["GET", "POST"])
def register():
    customer_form = RegisterForm()
    if customer_form.validate_on_submit():
        if register_user(customer_form, user_type="customer"):
            return url_for("login")
    else:
        return render_template("register.html", register_form=customer_form, user="customer", error=False)
