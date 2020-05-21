from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

vendor_bp = Blueprint('vendors', __name__)

@vendor_bp.route('/', defaults={'vendor': 'index'})
@vendor_bp.route('/<vendor>')
def show(vendor):
    try:
        return render_template('vendors/%s.html' % vendor)
    except TemplateNotFound:
        abort(404)