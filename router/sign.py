from flask import Blueprint,request, session, redirect, url_for
from flask.templating import render_template
import json
from collections import OrderedDict
from model import user_dao
from . import hangout

import bcrypt



bp = Blueprint('sign_bp', __name__, url_prefix='/sign')
@bp.route("/getUserCancel",methods=['GET','POST'])
def getUserCancel():
    if request.method == 'GET' and 'user_id' in request.form:
        #print(user_dao.UserDao().getUserCancel(request.form['user_id']))
        #print("asd")
        return str(user_dao.UserDao().getUserCancel(request.form['user_id']))
@bp.route("/user-manage",methods=['GET','POST'])
def userManage():
    return render_template("user_manage.html")

@bp.route("",methods=['GET','POST'])
def init():
    if request.method == 'GET':
        print("sd")

@bp.route("/user_approve", methods = ['POST','GET'])
def userApprove():
    if request.method == 'POST' and 'user_phone' in request.form and 'approve' in request.form:
        print(request.form['user_phone'])
        print(request.form['approve'])
        dao = user_dao.UserDao()
        if dao.getUserIdByPhone(request.form['user_phone'])==None:
            return "false"
        if request.form['approve']=="true": # approve
            try:
                dao.setUserCancel(dao.getUserIdByPhone(request.form['user_phone']),999999)
            except:
                return "setUserCancel error"
        else: # not approve
            try:
                dao.setUserCancel(dao.getUserIdByPhone(request.form['user_phone']),0)
            except:
                return "setUserCancel error"

        return "true"
    return "/user_approve error"


@bp.route("/idcheck",methods=['GET','POST'])
def check_user_id():
    if request.method == 'POST' and 'user_id' in request.form and 'user_phone' in request.form:
        dao = user_dao.UserDao()
        if dao.idCheck(request.form.get('user_id'))== True:
            session['user_id'] = request.form.get('user_id')
            session['user_phone'] = request.form.get('user_phone')
            session.modified = True
            return "true"
        else:
            dao = user_dao.UserDao()
            account = dao.getUserInfo(request.form.get('user_id'))
            #print(account)
            session["user_info"]=account
            print("user_info")
            print(session["user_info"])
            session["loggedin"] = True
            session["user_id"] = account['user_id']
            if session["user_id"] ==  "user":
                session["isTrial"] = True
                #print("it is trial")
            else:
                session["isTrial"] = False
            session["user_my_hangout"] = account['user_my_hangout']
            session["user_my_past_hangout"] = account["user_past_hangout"]
            session["user_age"] = account["user_birth"]
            session["user_nation"] = account["user_nation"]
            session["user_university"] = account["user_university"]
            session["user_name"] = account["user_name"]
            session["user_gender"] = account["user_gender"]
            session.modified = True
            return "false"


@bp.route("/signup",methods=['GET','POST'])
def signup():
    print("it is render")
    if request.method == 'POST' and 'name' in request.form:

        #print(request.get_json())
        #-----info
        user_id = session['user_id']
        user_phone = session['user_phone']
        #print(user_id)
        #print("-----")
        dao = user_dao.UserDao()
        # request 처리해서 user 객체 생성
        user = user_dao.User(dao.count_user()+1)
        user.create_user(request.form,user_id,user_phone)

        # 생성된 객체를 데이터베이스에 넣기
        dao.insert_user(user)

        account = dao.getUserInfo(user_id)
        session["user_info"]=account
        session["loggedin"] = True
        session["user_id"] = account['user_id']
        session["user_my_hangout"] = account['user_my_hangout']
        session["user_my_past_hangout"] = account["user_past_hangout"]
        session["user_age"] = account["user_birth"]
        session["user_nation"] = account["user_nation"]
        session["user_university"] = account["user_university"]
        session["user_name"] = account["user_name"]
        session["user_gender"] = account["user_gender"]

        session.modified = True
        return redirect(url_for('hangout_bp.hangout_list'))

    else:
        #print("it is render")
        return render_template("signup.html")



@bp.route("/login",methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'id' in request.form and 'password' in request.form:
        dao = user_dao.UserDao()
        input_password = request.form['password']
        input_id = request.form.get('id')
        account, check_password = dao.login_check(input_id,input_password)
        if check_password == True:
            session["user_info"]=account
            session["loggedin"] = True
            session["user_id"] = account['user_id']
            session["user_my_hangout"] = account['user_my_hangout']
            session["user_my_past_hangout"] = account["user_past_hangout"]
            session["user_age"] = account["user_birth"]
            session["user_nation"] = account["user_nation"]
            session["user_university"] = account["user_university"]
            session["user_name"] = account["user_name"]
            session["user_gender"] = account["user_gender"]
            session.modified = True
            return redirect(url_for('hangout_bp.hangout_list'))
        elif check_password == False and account != None:
            msg = "승인되지않은 사용자입니다."
        else:
            msg="존재하지않는 계정이거나 비밀번호가 틀렸습니다."

    if 'user_info' in session and session["isTrial"]==False:
        return redirect(url_for('hangout_bp.hangout_list'))

    return render_template("login.html",result=msg)
