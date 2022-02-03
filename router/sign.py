from flask import Blueprint,request, session, redirect, url_for
from flask.templating import render_template
import json
from collections import OrderedDict
from model import user_dao
from . import hangout

import bcrypt


def tmp(request):
    print(request.form.get('id'))

bp = Blueprint('sign_bp', __name__, url_prefix='/sign')

@bp.route("",methods=['GET','POST'])
def init():
    if request.method == 'GET':
        print("sd")

@bp.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST' and 'id' in request.form:
        #print(request.get_json())
        #-----info
        dao = user_dao.UserDao()
        # request 처리해서 user 객체 생성
        user = user_dao.User(dao.count_user()+1)
        user.create_user(request.form)

        # 생성된 객체를 데이터베이스에 넣기
        dao.insert_user(user)

        return redirect(url_for('sign_bp.login'))

    else:
        return render_template("signup.html")



@bp.route("/login",methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'id' in request.form and 'password' in request.form:
        dao = user_dao.UserDao()
        input_password = request.form['password']
        input_id = request.form.get('id')
        account, check_password = dao.login_check(input_id,input_password)
        print(check_password)
        if check_password == True:
            session["loggedin"] = True
            session["user_id"] = account['user_id']
            session["user_my_hangout"] = account['user_my_hangout']
            session["user_my_past_hangout"] = account["user_past_hangout"]
            session["user_age"] = account["user_birth"]
            session["user_nation"] = account["user_nation"]
            session["user_university"] = account["user_university"]
            session["user_name"] = account["user_name"]
            session["user_gender"] = account["user_gender"]

            return redirect(url_for('hangout_bp.hangout_list'))
        else:
            msg="Login Failed"


    return render_template("login.html",result=msg)
