from flask_mongoengine import MongoEngine
from flask_user import UserMixin

db = MongoEngine()


class User(db.Document, UserMixin):
    # User authentication information
    username = db.StringField(default='')
    password = db.StringField()
    roles = db.ListField(db.StringField(), default=[])

class Vendor(db.Document):
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
    # User information
    first_name = db.StringField(default='')
    last_name = db.StringField(default='')
    orders = db.ListField(db.EmbeddedDocumentField(Order))

