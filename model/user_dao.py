import json
from flask import Flask, request, session, jsonify
from . import bappy_db
from datetime import datetime
import bcrypt


#host = '18.118.131.221'
host = '127.0.0.1'
db_id = 'benny'
pw = 'benny'
db_name = 'bappy_web'

class User():
    def __init__(self,idx):
        self.idx = idx
        self.id = ""
        self.password = ""
        self.phone = ""
        self.name = ""
        self.gender = ""
        self.birth = ""
        self.nation = ""
        self.university = ""
        self.visit = 0
        self.past_hangout = ""
        self.my_hangout = ""
        self.reg_time = ""
        self.login_time = ""
        self.cancel = 0
        self.character = []
        self.interest = [] # interests 개수 9개
        self.language = []
        self.isKorean = 0

    def create_user(self,rf,user_id):
        character = []
        interest = []
        language = []

        for i in range(2):
            self.character.append(rf.get('ch' + str(i+1)))

        for i in range(9):
            self.interest.append(rf.get('int'+str(i+1)))

        for i in range(6):
            self.language.append(rf.get('lang'+str(i+1)))

        #self.password = (bcrypt.hashpw(rf.get('password').encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')
        self.phone = rf.get('phone')
        self.gender = rf.get('gender')
        self.name = rf.get('name')
        self.id = user_id

        self.birth = rf.get('birth')
        self.nation = rf.get('country_selector')
        if self.nation == "kr":
            self.isKorean = 1
        else:
            self.isKorean = 0
        self.university = rf.get('university')
        self.visit = 0
        self.cancel = 0
        self.reg_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.login_time = datetime.now().strftime('%Y-%m-%d %H:%M')

print(datetime.now().strftime('%Y-%m-%d %H:%M'))

class UserDao():
    def __init__(self):
        self.database = bappy_db.Database()

    def list_to_str(self, li):
        if len(li)==1:
            return str(li[0])
        for i in range(len(li)):
            li[i]=str(li[i])
        return ','.join(li)
    # "1,2,3,4"->[1,2,3,4]
    def str_to_li(self,db_str):
        db_str = str(db_str)
        if db_str == "None":
            return []
        if db_str ==  "":
            return []
        return db_str.split(',')

    def updateUsermyHangout(self,idx,myHangout):
        sql =  """update bp_user set user_my_hangout = '%s' where user_idx = %d """%(myHangout,int(idx))
        print(sql)
        self.database.execute(sql)

    def count_user(self):
        sql = """select count(0) as cnt from bp_user"""
        return self.database.executeAll(sql)[0]['cnt']

    def insert_user(self, user):
        sql = """insert into bp_user(
        user_approve,user_isKorean,user_idx,user_id,user_phone,user_name,user_gender,user_birth,user_nation,user_university,user_visit,user_reg_time,user_cancel,user_character,user_interests,user_language,user_login_time)values(%d,%d,"%s","%s","%s","%s","%s","%s","%s","%s",%d,"%s",%d,"%s","%s","%s","%s")"""%(0,user.isKorean,user.idx,user.id,user.phone,user.name,user.gender,user.birth, user.nation,user.university,user.visit, user.reg_time, user.cancel,self.list_to_str(user.character), self.list_to_str(user.interest), self.list_to_str(user.language),user.login_time )
        print(sql)
        #print(sql)
        self.database.execute(sql)

    def idCheck(self,id):
        sql = """select * from bp_user where user_id = '%s' """%(id)
        account = self.database.executeOne(sql)
        if(account == None):
            return True
        else:
            return False

    def getUserInfo(self,id):
        sql = """select * from bp_user where user_id = '%s'"""%(id)
        account  = self.database.executeOne(sql)
        return  account

    def login_check(self,id,input_password):
        sql = """select * from bp_user where user_id = '%s' """%(id)
        account = self.database.executeOne(sql)
        if account == None:
            return account, False
        if account['user_approve']==0:
            return account, False
        input_password = input_password.encode('UTF-8')
        check_password = bcrypt.checkpw(input_password, account['user_password'].encode('UTF-8'))
        return account, check_password
