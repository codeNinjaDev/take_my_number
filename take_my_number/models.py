from flask_mongoengine import MongoEngine

from app import db

class Vendor(db.Document):
    # User authentication information
    username = db.StringField(default='')
    password = db.StringField()
    first_name = db.StringField(default='')
    last_name = db.StringField(default='')
    brand = db.StringField(default='')
    location = db.PointField(auto_index=False)
    max_occupants = db.IntField()
    current_occupants = db.IntField()
    user_queue = db.IntField()
    number_up = db.IntField(),
    meta = {
        'indexes': [[("location", "2dsphere"), ("datetime", 1)]]
    }

class Order(db.EmbeddedDocument):
    vendor = db.ReferenceField(Vendor)
    order_number = db.IntField(required=True)
    called_number = db.BooleanField()

class Customer(db.Document):
    # Customer information
    username = db.StringField(default='')
    password = db.StringField()
    orders = db.ListField(db.EmbeddedDocumentField(Order))

