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

    def create_user(self,rf):
        character = []
        interest = []
        language = []

        for i in range(2):
            self.character.append(rf.get('ch' + str(i+1)))

        for i in range(9):
            self.interest.append(rf.get('int'+str(i+1)))

        for i in range(6):
            self.language.append(rf.get('lang'+str(i+1)))

        self.id = rf.get('id')
        self.password = (bcrypt.hashpw(rf.get('password').encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')
        self.phone = rf.get('phone')
        self.gender = rf.get('gender')
        self.name = rf.get('name')

        self.birth = rf.get('birth')
        self.nation = rf.get('country_selector')
        self.university = rf.get('university')
        self.visit = 0
        self.cancel = 0
        self.reg_time = datetime.now()
        self.login_time = datetime.now()


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
    def str_to_li(self, db_str):
        return db_str.split(',')

    def count_user(self):
        sql = """select count(0) as cnt from bp_user"""
        return self.database.executeAll(sql)[0]['cnt']

    def insert_user(self, user):
        sql = """insert into bp_user(
        user_idx,user_id,user_password,user_phone,user_name,user_gender,user_birth,user_nation,user_university,user_visit,user_reg_time,user_cancel,user_character,user_interests,user_language,user_login_time)values(%d,'%s','%s','%s','%s','%s','%s','%s','%s',%d,'%s',%d,'%s','%s','%s','%s')"""%(user.idx,user.id,user.password,user.phone,user.name,user.gender,user.birth, user.nation,user.university,user.visit, user.reg_time, user.cancel,self.list_to_str(user.character), self.list_to_str(user.interest), self.list_to_str(user.language),user.login_time )
        print(sql)
        self.database.execute(sql)

    def login_check(self,id,input_password):
        sql = """select * from bp_user where user_id = '%s' """%(id)
        account = self.database.executeOne(sql)
        input_password = input_password.encode('UTF-8')
        check_password = bcrypt.checkpw(input_password, account['user_password'].encode('UTF-8'))
        return account, check_password
