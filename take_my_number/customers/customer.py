import json
from flask import Blueprint, render_template, redirect, url_for, session, abort, flash
from jinja2 import TemplateNotFound
from flask_socketio import send, emit, SocketIO

from helpers import customer_login_required
from auth_forms import RegisterForm, LoginForm, login_user, register_user
from models import Customer, Vendor
from application import socketio, app
import geocoder
from geopy import distance


customer_bp = Blueprint('customers', __name__)


@socketio.on("get vendors", namespace="/customer")
def get_vendors(lat, lon, radius):
    all_vendors = Vendor.query.all()
    vendor_list = []
    for vendor in all_vendors:
        coord1 = (float(vendor.latitude), float(vendor.longitude))
        coord2 = (float(lat), float(lon))
        if distance.distance(coord1, coord2).miles < radius:
            vendor_dict = {
                "id": vendor.id,
                "name": vendor.brand,
                "address": geocoder.bing([float(vendor.latitude), float(vendor.longitude)],key=app.config["BING_MAPS_API"], method='reverse').address,
                "distance": distance.distance(coord1, coord2).miles
            }
            vendor_list.append(vendor_dict)
    print(json.dumps(vendor_list))
    emit("get vendors", json.dumps(vendor_list), json=True)

@customer_bp.route('/')
@customer_login_required
def index():
    return render_template('customer/index.html')

@customer_bp.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_user(login_form, user_type="customer"):
            return redirect(url_for(".index"))
        else:
            flash("Incorrect username or password")
    return render_template("login.html", login_form=login_form, user="customer")

@customer_bp.route('/register', methods=["GET", "POST"])
def register():
    customer_form = RegisterForm()
    error = False
    if customer_form.validate_on_submit():
        if register_user(customer_form, user_type="customer"):
            return redirect(url_for(".login"))
        else:
            error = True
    return render_template("register.html", register_form=customer_form, user="customer", error=error)

@customer_bp.route('/order', methods=["GET", "POST"])
def order():
    return render_template("customer/order.html")