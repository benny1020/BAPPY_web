from flask import Blueprint,request, session, redirect, url_for, flash
from flask.templating import render_template

import json
from collections import OrderedDict
from model import hangout_dao
from model import user_dao
from . import hangout
from . import sign




dao = hangout_dao.HangoutDao()

bp = Blueprint('hangout_bp', __name__, url_prefix='/hangout')

@bp.route("/moreList",methods=['GET','POST'])
def hangoutMoreList():
    if request.method == 'POST':
        pageNum = request.form.get('pageNum',type=int)
        #print("pageNum : ",pageNum)
        dao = hangout_dao.HangoutDao()
        res = dao.get_hangout_data_list(session['hangoutFilterVal'],pageNum)
        hangoutDataList = []
        for data in res:
            hangoutDataList.append(hangout_dao.dumper(data))

        #print(res[1].join_url)
        #print(json.dumps(hangoutDataList,ensure_ascii=False))
        return json.dumps(hangoutDataList,ensure_ascii=False)
        #return "abcddds"


@bp.route("/join", methods=['GET','POST'])
def hangout_join():
    if request.method == 'POST':
        print("join")
        idx = request.form.get('index')
        dao = hangout_dao.HangoutDao()
        res = dao.join_hangout_byidx(idx,session['user_id'],session['user_nation'],session['user_gender'],session['user_age'])
        if res == "false":
            session['cancel']='true'
        else:
            dao = user_dao.UserDao()
            userMyHangout = dao.str_to_li(session['user_info']['user_my_hangout'])
            userMyHangout.append(idx)
            #print("myhangout : ",userMyHangout)

            session['user_info']['user_my_hangout']=dao.list_to_str(userMyHangout)
            print(session['user_info'])
            dao.updateUsermyHangout(session['user_info']['user_idx'],session['user_info']['user_my_hangout'])

        session.modified = True
        return redirect(url_for('hangout_bp.hangout_list'))

@bp.route("/cancel",methods=['GET','POST'])
def hangout_cancel():

    idx = request.form.get('index')
    print("hangout index for delete : ",idx)
    dao = hangout_dao.HangoutDao()
    res = dao.cancel_hangout_byidx(idx,session['user_id'],session['user_nation'],session['user_gender'],session['user_age'])
    if res == "true":
        dao = user_dao.UserDao()
        userMyHangout = dao.str_to_li(session['user_info']['user_my_hangout'])
        try:
            userMyHangout.remove(idx)
        except:
            print("There is no myHangout index")

        session['user_info']['user_my_hangout']=dao.list_to_str(userMyHangout)
        dao.updateUsermyHangout(session['user_info']['user_idx'],session['user_info']['user_my_hangout'])

    session.modified = True
    return redirect(url_for('hangout_bp.hangout_list'))


@bp.route("/list",methods=['GET','POST'])
def hangout_list():
    if 'loggedin' in session and session['loggedin']==True and 'user_id' in session:
        if 'cancel' in session and session['cancel'] == 'true':
            flash(str("You cannot join this hangout"))
            session['cancel']='false'

        #필터 적용안된경우
        if 'filterVal' not in request.form:
            filterVal="default"
        else:
            filterVal = request.form.get('filterVal')

        print("Filter is ",filterVal)

        session["hangoutFilterVal"] = filterVal


        dao = hangout_dao.HangoutDao()
        hangout_list = dao.get_hangout_data_list(filterVal=filterVal)

        return render_template("hangout.html",hangout_data = hangout_list,filterVal=filterVal)
    session.modified = True
    return redirect(url_for("sign_bp.login"))


@bp.route("/register",methods=['GET','POST'])
def register_hangout():
    #print(request.form.get('code'))
    msg = ""
    #제출했을때
    if request.method == 'POST' and 'code' in request.form:
        #print(request.form.get('code'))
        print(request.form.get('index'))
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