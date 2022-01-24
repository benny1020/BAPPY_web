from flask import Blueprint,request, session
import json
from collections import OrderedDict




bp = Blueprint('signup_bp', __name__, url_prefix='/sign')

@bp.route("",methods=['GET','POST'])
def init():
    if request.method == 'GET':


@bp.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        request.form.get('ch1')
    else:
        return 404
