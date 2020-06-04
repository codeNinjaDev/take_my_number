"""Initialize Flask app."""

from flask import Flask, render_template
from flask_session import Session
from mongoengine import connect, disconnect
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_socketio import SocketIO
from flask_wtf import CsrfProtect
from flask_bootstrap import Bootstrap


from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import apology

app = Flask(__name__, instance_relative_config=False)
app.config.from_pyfile('../instance/config.py')
app.config["TEMPLATES_AUTO_RELOAD"] = True
print(app.config["MONGODB_HOST"])
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
Bootstrap(app)
db = MongoEngine(app)
disconnect()
connect(host=app.config["MONGODB_HOST"])

csrf = CsrfProtect(app)

socketio = SocketIO(app)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

from vendors import vendor
app.register_blueprint(vendor.vendor_bp, url_prefix='/vendor')

from customers import customer
app.register_blueprint(customer.customer_bp, url_prefix='/customer')
"""
def errorhandler(e):
    ""Handle error""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    print(e)
    apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
"""
if __name__ == "main":
    socketio.run(app)
