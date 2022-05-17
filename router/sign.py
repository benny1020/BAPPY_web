from flask import Blueprint,request, session, redirect, url_for
from flask.templating import render_template
import json
from collections import OrderedDict
from model import user_dao
from . import hangout

import urllib.request
import os

import bcrypt

def list_to_str(li):
    if len(li)==1:
        return str(li[0])
    for i in range(len(li)):
        li[i]=str(li[i])
    return ','.join(li)
# "1,2,3,4"->[1,2,3,4]
def str_to_li( db_str):
    db_str = str(db_str)
    if db_str == "None":
        return []
    if db_str ==  "":
        return []
    return db_str.split(',')

bp = Blueprint('sign_bp', __name__, url_prefix='/sign')
#
#

class userData():
    def __init__(self,user_info):
        self.user_name = user_info['user_name']
        self.user_gender = user_info['user_gender']
        self.user_university = user_info['user_university']
        self.user_nation = user_info['user_nation']
        self.user_birth = user_info['user_birth']

        character = user_info['user_character']
        interests = user_info['user_interests']
        language = user_info['user_language']

        character = str_to_li(character)
        interests = str_to_li(interests)
        language = str_to_li(language)

        self.user_character = []
        self.user_interests = []
        self.user_language = []

        interests_list = ['Movies','Books','Sports','Games','Talking','Drinking','Travelling','Vegan','Cooking']
        language_list = ['Korean','English','Spanish','French','Chinese','Japanese']

        for ch in character:
            self.user_character.append(ch)

        for i in range(len(interests)):
            if interests[i] == 'on':
                self.user_interests.append(interests_list[i])

        for i in range(len(language)):
            if language[i] == 'on':
                self.user_language.append(language_list[i])

        len_int = len(self.user_interests)
        len_lan = len(self.user_language)
        for i in range(9-len_int):
            self.user_interests.append(" ")

        self.user_language = list_to_str(self.user_language)

@bp.route("/profileImage",methods = ['POST'])
def setProfileImage():
    if request.method == 'POST':
        #url = "http://k.kakaocdn.net/dn/JHuM3/btryU2LLwhn/zDqZDcjcqVbLkZ1ufpoSc1/img_110x110.jpg"
        url = request.form['profileImageUrl']
        urllib.request.urlretrieve(url,"./static/profileImage/"+session['user_id']+".png")
        return "200"


@bp.route("/userInfo/<user_id>", methods = ['GET'])
def get_userinfo(user_id):
    if request.method == 'GET':
        dao = user_dao.UserDao()

        user_info = dao.getUserInfo(user_id)
        if user_info == None:
            return "404"
        else:
            data = userData(user_info)
            path = "./static/profileImage/"
            file_list = os.listdir(path)
            if user_id+".png" not in file_list:
                user_id = "bird"
            return render_template("userinfo.html",user_info = data,user_id=user_id)





    else:
        return "404 error"
@bp.route("/getUserCancel",methods=['GET','POST'])
def getUserCancel():
    if request.method == 'GET':
        #print(user_dao.UserDao().getUserCancel(request.form['user_id']))
        #print("asd")

        return str(user_dao.UserDao().getUserCancel(session['user_info']['user_id']))
    return "/getUserCancel error"

@bp.route("/usermanage",methods=['GET','POST'])
def user_manage():
    if request.method == 'GET':
        return render_template("user_manage.html")
    return "user_manage false"

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
            session["isTrial"] = False
            session.modified = True
            return "true"
        else:
            dao = user_dao.UserDao()
            account = dao.getUserInfo(request.form.get('user_id'))
            #print(account)
            session["user_info"]=account
            session["loggedin"] = True
            session["user_id"] = account['user_id']
            if session["user_id"] ==  "user":
                session["isTrial"] = True
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

            if 'user_info' in session:
                res = dao.update_loginTime(session['user_info']['user_id'])
                try:
                    dao.update_visit(session['user_info']['user_id'])
                except:
                    print("user visit update failed")
                if res != True:
                    print(res)
                print(session['user_info']['user_name'] + "login")

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
