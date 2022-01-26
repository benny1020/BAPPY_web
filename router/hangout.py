from flask import Blueprint,request, session, redirect, url_for
from flask.templating import render_template

import json
from collections import OrderedDict
from model import hangout_dao
from . import hangout
from . import sign



bp = Blueprint('hangout_bp', __name__, url_prefix='/hangout')

@bp.route("/list",methods=['GET','POST'])
def hangout_list():
    if 'loggedin' in session and session['loggedin']==True:
        h = hangout_dao.hangout_data()
        h.title = "#test #test #test"
        h.meet_time = "1월 30일 12시 30분"
        h.location = "test location"
        h.profile_image = ["bird.png","bird.png","person.png","person.png"]
        h.nation_image = ["usa.png","usa.png","nation.png","nation.png"]
        h.age = ["20","30","?","?"]
        h.gender = ["M","F","?","?"]
        h.join = "join"
        h.join_url = "/sign/login"
        h.location_url = "naver.com"
        h.openchat = "google.com"
        return render_template("hangout.html",hangout_data = h)


    return redirect(url_for("sign_bp.login"))


@bp.route("/register",methods=['GET','POST'])
def register_hangout():
    #print(request.form.get('code'))
    msg = ""
    #제출했을때
    if request.method == 'POST' and 'code' in request.form:
        #print(request.form.get('code'))

        if request.form.get('code') == "code":
            if request.form.get('title')=="" or request.form.get('openchat')=='' or request.form.get('location')=='' or request.form.get('time')=="":
                msg="빈칸 없이 입력하라했잖아 다시 입력해 ㅡㅡ"
            else:
                dao = hangout_dao.HangoutDao()
                hangout = hangout_dao.Hangout(dao.count_hangout())
                hangout.create_hangout(request)
                dao.insert_hangout(hangout)
                return redirect(url_for('hangout_bp.hangout_list'))

        else:
            msg = "code 틀렸어 ㅡㅡ 너 어드민 아니지? ㅗ"
        #print(request.form.get('code'))

    return render_template('admin.html',msg=msg)
