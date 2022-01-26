import json
from flask import Flask, request, session, jsonify
from . import bappy_db
from datetime import datetime

host = '18.118.131.221'
db_id = 'benny'
pw = 'benny'
db_name = 'bappy_web'

class hangout_data():
    def __init__(self):
        self.title = ""
        self.meet_time = ""
        self.location = ""
        self.profile_image = []
        self.nation_image = []
        self.age = []
        self.gender = []
        self.join = "join"
        self.join_url = "" # cancel join redirct
        self.location_url = "naver.com"
        self.openchat = ""

    def make_hangout_data(self,Hangout):
        self.title = Hangout.title
        self.meet_time = Hangout.meet_time
        self.location = Hangout.location
        #--- 이미지
        #if Hangout.image == ""
        #self.image = ""

class Hangout():
    def __init__(self,idx):
        self.idx = idx
        self.participants_id = ""
        self.participants_nation = ""
        self.participants_image = ""
        self.participants_num = 0
        self.participants_gender = ""
        self.participants_age = ""
        self.click_num = 0
        self.openchat = ""
        self.location = ""
        self.title = ""
        self.meet_time = ""
        self.register_time = ""
        self.city=""
#print(datetime.now())
    def create_hangout(self, request):
        self.openchat = request.form.get('openchat')
        self.location = request.form.get('location')
        self.title = request.form.get('title')
        self.meet_time = request.form.get('meet_time')
        self.register_time = datetime.now().strftime('%m-%d %H:%M')
        self.city= request.form.get('city')

class HangoutDao():
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

    def count_hangout(self):
        sql = """select count(0) as cnt from bp_hangout"""
        return self.database.executeAll(sql)[0]['cnt']

    def insert_hangout(self, hangout):
        sql = """
        INSERT INTO bp_hangout (hg_city,idx, hg_participants_num, hg_click_num, hg_openchat, hg_location, hg_title, hg_meet_time, hg_register_time)
        VALUES ('%s','%d', '%d', '%d', '%s', '%s', '%s', '%s', '%s')
        """%(hangout.city,hangout.idx, hangout.participants_num, hangout.click_num,hangout.openchat,hangout.location,hangout.title,hangout.meet_time,hangout.register_time)
        self.database.execute(sql)
