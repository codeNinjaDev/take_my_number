import json


from flask import Blueprint, render_template, redirect, url_for, session, abort, flash, request
from jinja2 import TemplateNotFound
from flask_socketio import send, emit, SocketIO


from helpers import vendor_login_required
from auth_forms import VendorForm, LoginForm, login_user, register_user
from models import Vendor, db
from application import socketio, app
import geocoder
from geopy import distance

vendor_bp = Blueprint('vendor', __name__)


@socketio.on('enter', namespace="/vendor")
@vendor_login_required
def enter_store():
    curr_vendor = Vendor.query.filter_by(id=session["vendor_id"]).first()
    curr_vendor.current_occupants += 1
    db.session.add(curr_vendor)
    db.session.commit()
    emit("current occupants", curr_vendor.current_occupants, namespace="/vendor")

@socketio.on('exit', namespace="/vendor")
@vendor_login_required
def exit_store():
    curr_vendor = Vendor.query.filter_by(id=session["vendor_id"]).first()
    curr_vendor.current_occupants -= 1
    if curr_vendor.current_occupants < curr_vendor.max_occupants:
        curr_vendor.number_up += 1
        message_name = "vendor" + str(session["vendor_id"])
        emit(message_name, curr_vendor.number_up)
    db.session.add(curr_vendor)
    db.session.commit()
    emit("current occupants", curr_vendor.current_occupants, namespace="/vendor")
    emit("number up", curr_vendor.number_up, namespace="/vendor")

@socketio.on('reset', namespace="/vendor")
@vendor_login_required
def reset_store():
    curr_vendor = Vendor.query.filter_by(id=session["vendor_id"]).first()
    curr_vendor.current_occupants = 0
    curr_vendor.number_up = 0
    curr_vendor.user_queue = curr_vendor.max_occupants
    db.session.add(curr_vendor)
    db.session.commit()
    emit("current occupants", curr_vendor.current_occupants, namespace="/vendor")
    emit("number up", curr_vendor.number_up, namespace="/vendor")
    emit("user queue", curr_vendor.user_queue, namespace="/vendor")

@vendor_bp.route('/home', defaults={'action': None})
@vendor_bp.route('/home/<action>', methods=["GET", "POST"])
@vendor_login_required
def index(action):
    curr_vendor = Vendor.query.filter_by(id=session["vendor_id"]).first()
    if request.method == "POST":
        if action == "enter":
            curr_vendor.current_occupants += 1
        elif action == "exit":
            curr_vendor.current_occupants -= 1
            if curr_vendor.current_occupants < curr_vendor.max_occupants:
                curr_vendor.number_up += 1
        elif action == "reset":
            curr_vendor.current_occupants = 0
        else:
            return render_template('vendor/index.html', current_occupants=curr_vendor.current_occupants, user_queue=curr_vendor.user_queue, max_occupants=curr_vendor.max_occupants)

        db.session.add(curr_vendor)
        db.session.commit()

        message_name = "vendor" + str(session["vendor_id"])
        emit(message_name, (curr_vendor.number_up), namespace='/')
    return render_template('vendor/index.html', current=curr_vendor.current_occupants, user_queue=curr_vendor.user_queue, max_occupants=curr_vendor.max_occupants)

@vendor_bp.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_user(login_form, user_type="vendor"):
            print(url_for(".index"))
            return redirect(url_for(".index"))
        else:
            flash("Incorrect username or password")
    return render_template("login.html", login_form=login_form, user="vendor")

@vendor_bp.route('/register', methods=["GET", "POST"])
def register():
    vendor_form = VendorForm()
    error = False
    if vendor_form.validate_on_submit():
        if register_user(vendor_form, user_type="vendor"):
            return redirect(url_for(".login"))
        else:
            error = True
    return render_template("register.html", register_form=vendor_form, user="vendor", error=error)


