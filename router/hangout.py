from flask import Blueprint,request, session, redirect, url_for
from flask.templating import render_template

import json
from collections import OrderedDict
from model import user_dao
from . import sign
import bcrypt



bp = Blueprint('hangout_bp', __name__, url_prefix='/hangout')

@bp.route("/list",methods=['GET','POST'])
def list():
    if 'loggedin' in session:
        return render_template('hangout.html')
    else:
        return redirect('sign_bp.login')
