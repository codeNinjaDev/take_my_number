from flask import session, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DecimalField, validators, SubmitField
from werkzeug.security import check_password_hash, generate_password_hash

from models import Customer, Vendor
from app import db

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', [validators.Length(min=6, max=35), validators.InputRequired()])
    last_name = StringField('Last Name', [validators.Length(min=6, max=35), validators.InputRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.InputRequired()])
    password = PasswordField('New Password', [validators.InputRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField("Submit")

class VendorForm(RegisterForm):
    max_occupancy = IntegerField('Max Occupancy', [validators.InputRequired()])
    brand = StringField("Brand Name", [validators.InputRequired()])
    latitude = DecimalField("Latitude")
    longitude = DecimalField("Longitude")
    current_occupants = IntegerField("Current Occupants")

class LoginForm(FlaskForm):
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    submit = SubmitField("Submit")

def login_user(login_form, user_type="customer"):
    user = None
    if user_type == "customer":
        user = Customer.objects(username=login_form.email.data).first()
    else:
        user = Vendor.objects(username=login_form.email.data).first()

    if not user or not check_password_hash(user.psswd_hash, login_form.password.data):
        print(login_form.password.data)
        return False

    if user_type == "customer":
        session["customer_id"] = user.id
    else:
        session["vendor_id"] = user.id
    return True

def register_user(register_form, user_type="customer"):
    username = register_form.email.data
    password_hash = generate_password_hash(register_form.password.data)
    # Query database for username
    user = None
    if user_type == "customer":
        user = Customer.objects(username=register_form.email.data).first()
    else:
        user = Vendor.objects(username=register_form.email.data).first()

    if user:
        return render_template("register.html", register_form=register_form, user=user_type, error=True)

    if user_type == "customer":
        customer = Customer(username=username, psswd_hash=password_hash, first_name=register_form.first_name.data,
            last_name=register_form.last_name.data).save()
    else:
        vendor = Vendor(username=username, psswd_hash=password_hash, first_name=register_form.first_name.data,
            last_name=register_form.last_name.data, max_occupants=int(register_form.max_occupancy.data), brand=register_form.brand.data,
            current_occupants=int(register_form.current_occupants.data), location=[int(register_form.latitude.data), int(register_form.longitude.data)],
            user_queue=0, number_up=int(register_form.max_occupancy.data)).save()
