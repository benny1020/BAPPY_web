from flask import Blueprint,request, session, redirect, url_for, flash
from flask.templating import render_template

import json
from collections import OrderedDict
from model import hangout_dao
from model import user_dao
from . import hangout
from . import sign
from werkzeug.utils import secure_filename




dao = hangout_dao.HangoutDao()

bp = Blueprint('hangout_bp', __name__, url_prefix='/hangout')

@bp.route("checkCancelTime",methods = ['GET','POST'])
def checkcanceltime():
    if request.method == 'GET':
        #index = request.form.get("index")
        index = request.args["index"]
        dao = hangout_dao.HangoutDao()
        if dao.checkCancelTime(index) == False:
            return "false"
        else:
            return "true"
    else:
        return "checkcanceltime error"


@bp.route("/filterList",methods=['GET','POST'])
def hangoutfilterList():
    if request.method == 'POST':
        filterVal = request.form.get("filterVal")
        session['hangoutFilterVal']=filterVal
        session.modified = True
        dao = hangout_dao.HangoutDao()
        res = dao.get_hangout_data_list(filterVal)
        hangoutDataList = []
        for data in res:
            #print(data.index)
            hangoutDataList.append(hangout_dao.dumper(data))

        return json.dumps(hangoutDataList,ensure_ascii=False)

    else:
        return "Please contact us through the bappy kakao channel"

@bp.route("/moreList",methods=['GET','POST'])
def hangoutMoreList():
    if request.method == 'POST':
        print("it is ",session['hangoutFilterVal'])
        pageNum = request.form.get('pageNum',type=int)
        #print("pageNum " + str(pageNum))
        #print("pageNum : ",pageNum)
        dao = hangout_dao.HangoutDao()
        res = dao.get_hangout_data_list(session['hangoutFilterVal'],pageNum)
        hangoutDataList = []
        for data in res:
            #print(data.index)
            hangoutDataList.append(hangout_dao.dumper(data))

        #print(res[1].join_url)
        #print(json.dumps(hangoutDataList,ensure_ascii=False))
        return json.dumps(hangoutDataList,ensure_ascii=False)
    else:
        return "Please contact us through the bappy kakao channel"
        #return "abcddds"


@bp.route("/join", methods=['GET','POST'])
def hangout_join():
    if request.method == 'POST': # trial
        if session['user_info']['user_id']=="user":
            flash("trial")
            return redirect(url_for('hangout_bp.hangout_list'))

    if request.method == 'POST' and 'user_info' in session and 'index' in request.form:
        dao = user_dao.UserDao()

        idx = request.form.get('index')
        dao = hangout_dao.HangoutDao()
        res = dao.join_hangout_byidx(session['user_info']['user_my_hangout'],idx,session['user_id'],session['user_nation'],session['user_gender'],session['user_age'])

        # 같은 국가 3명 이상인 경우
        if res == 0:
            #session['cancel']='true'
            return "0"
        # 이미 참가한 행아웃에서 4시간 이내인경우
        elif res == 1:
            return "1"
        else:
            dao = user_dao.UserDao()

            userMyHangout = dao.str_to_li(session['user_info']['user_my_hangout'])
            userMyHangout.append(idx)

            session['user_info']['user_my_hangout']=dao.list_to_str(userMyHangout)
            #print(session['user_info'])
            dao.updateUsermyHangout(session['user_info']['user_idx'],session['user_info']['user_my_hangout'])
            ret = dao.getUserCancel(session['user_info']['user_id'])
            dao.setUserCancel(session['user_info']['user_id'],dao.getUserCancel(session['user_info']['user_id'])-1)

            session.modified = True
            return "2"
        session.modified = True
        return redirect(url_for('hangout_bp.hangout_list'))
    else:
        return "Please contact us through the bappy kakao channel"

@bp.route("/cancel",methods=['GET','POST'])
def hangout_cancel():
    if request.method == 'POST' and 'index' in request.form and 'user_info' in session:
        idx = request.form.get('index',type=str)
        #print("hangout index for delete : ",idx)
        dao = hangout_dao.HangoutDao()
        res = dao.cancel_hangout_byidx(idx,session['user_id'],session['user_nation'],session['user_gender'],session['user_age'])
        #print(res)
        if res == "true":
            dao = user_dao.UserDao()
            userMyHangout = dao.str_to_li(session['user_info']['user_my_hangout'])
            #print(userMyHangout)
            try:
                userMyHangout.remove(idx)
            except:
                print("There is no myHangout index")

            session['user_info']['user_my_hangout']=dao.list_to_str(userMyHangout)
            session.modified = True
            dao.updateUsermyHangout(session['user_info']['user_idx'],session['user_info']['user_my_hangout'])
            hangoutdao = hangout_dao.HangoutDao()
            if hangoutdao.checkCancelTime(idx) == False:
                dao.setUserCancel(session['user_info']['user_id'],0)
            return "true"

        session.modified = True
        return "cancel fail"
    else:
        return "Please contact us through the bappy kakao channel"

@bp.route("/trial",methods=['GET','POST'])
def hangoutTrial():
    if request.method=="GET":
        print("asd")

@bp.route("/list",methods=['GET','POST'])
def hangout_list():
    if 'loggedin' in session and session['loggedin']==True and 'user_info' in session:
        if 'checkTimeHangout' in session and session['checkTimeHangout']=='false':
            flash(str("4시간 이내 참가 불가"))
            session['checkTimeHangout']='true'
        if 'cancel' in session and session['cancel'] == 'true':
            flash(str("Bappy hangout consists of 2 Koreans and 2 internationals. There are no spots for your nationality."))
            session['cancel']='false'

        #필터 적용안된경우
        if 'filterVal' not in request.form:
            filterVal="default"
        else:
            filterVal = request.form.get('filterVal')

        print("Filter is ",filterVal)

        session["hangoutFilterVal"] = filterVal

        if session['isTrial']==True:
            print("hangout trial")

        dao = hangout_dao.HangoutDao()
        hangout_list = dao.get_hangout_data_list(filterVal=filterVal)
        session.modified = True
        if session['isTrial']==True:
            return render_template("hangout_trial.html",hangout_data = hangout_list,filterVal=filterVal)
        return render_template("hangout.html",hangout_data = hangout_list,filterVal=filterVal)
    session.modified = True
    return redirect(url_for("sign_bp.login"))


@bp.route("/register",methods=['GET','POST'])
def register_hangout():
    msg = ""
    #print(request.form.get('code'))
    if request.method == 'POST':
        #print(request.form.get("code"))
        #제출했을때
        if request.method == 'POST' and 'code' in request.form:
            #print(request.form.get('code'))
            #print(request.form.get('index'))
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
                return "code 틀렸어 ㅡㅡ 너 어드민 아니지? ㅗ"
        #print(request.form.get('code'))
    else: # GET
        return render_template('admin.html',msg=msg)
