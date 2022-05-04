from flask import Blueprint,request, session, redirect, url_for
from flask.templating import render_template

import json
from collections import OrderedDict
from model import user_dao
from . import sign
import bcrypt
from model import hangout_dao

bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@bp.route("/register",methods=['GET','POST'])
def register():
    if 'loggedin' in session:
        return render_template('hangout.html')
    else:
        return redirect('sign_bp.login')


@bp.route("/cancel",methods=['POST'])
def admin_cancel():
    if 'user_id' in request.form and 'hangout_id' in request.form:
        user_id = request.form['user_id']
        hangout_id = request.form['hangout_id']
        hdao = hangout_dao.HangoutDao()
        udao = user_dao.UserDao()
        user_info = udao.getUserInfo(user_id)
        session['user_info'] = user_info
        session.modified=True
        res = hdao.cancel_hangout_byidx(hangout_id,user_id,user_info['user_nation'],user_info['user_gender'],user_info['user_birth'])

        if res == "true":
            userMyHangout = udao.str_to_li(user_info['user_my_hangout'])
            try:
                userMyHangout.remove(hangout_id)
            except:
                return "cannot remove"

            udao.updateUsermyHangout(user_id,user_info['user_my_hangout'])
            return "complete"
    else:
        return "error"
