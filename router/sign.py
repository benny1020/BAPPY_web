from flask import Blueprint,request, session
import json
from collections import OrderedDict
from model import user_dao

import bcrypt


def tmp(request):
    print(request.form.get('id'))

bp = Blueprint('signup_bp', __name__, url_prefix='/sign')

@bp.route("",methods=['GET','POST'])
def init():
    if request.method == 'GET':
        print("sd")

@bp.route("/signup",methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        #print(request.get_json())
        #-----info
        dao = user_dao.UserDao()

        # request 처리해서 user 객체 생성
        user = user_dao.User(dao.count_user()+1)
        user.create_user(request.form)

        # 생성된 객체를 데이터베이스에 넣기
        dao.insert_user(user)

        return 404

    else:
        return 404

@bp.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        dao = user_dao.UserDao()
        input_password = request.form['password']


        input_id = request.form.get('id')
        account, check_password = dao.login_check(input_id,input_password)
        print(check_password)
        return 404
