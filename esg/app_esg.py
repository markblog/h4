from flask import Blueprint,jsonify,request,send_file
from flask_cors import cross_origin

bp = Blueprint('esg',__name__,url_prefix='/esg')


@bp.route('/')
def index():
    return "esg's index page"
