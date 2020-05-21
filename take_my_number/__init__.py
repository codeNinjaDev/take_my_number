"""Initialize Flask app."""

from flask import Flask
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_user import login_required, UserManager, UserMixin

from .models import db

def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('../instance/config.py')
    db.init_app(app)
    app.session_interface = MongoEngineSessionInterface(db)


    with app.app_context():
        from .vendors import vendor
        app.register_blueprint(vendor.vendor_bp, url_prefix='/vendors')
    return app