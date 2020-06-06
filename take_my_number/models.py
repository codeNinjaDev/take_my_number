from flask_sqlalchemy import SQLAlchemy

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    # User authentication information
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    latitude = db.Column(db.String(10))
    longitude = db.Column(db.String(10))
    max_occupants = db.Column(db.Integer)
    current_occupants = db.Column(db.Integer)
    user_queue =  db.Column(db.Integer)
    number_up =  db.Column(db.Integer)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    order_number =  db.Column(db.Integer, nullable=False)
    called_number = db.Column(db.Boolean, default=False)


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

