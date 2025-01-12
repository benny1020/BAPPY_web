import json
from flask import Flask, request, session, jsonify
from . import bappy_db
from datetime import datetime
from  datetime import timedelta
import os

timedelta(hours=1)
db_id = 'benny'
pw = 'benny'
db_name = 'bappy_web'

def dumper(obj):
    try:
        return obj.toJSON()
    except:
        return obj.__dict__

class Hangout_Data():
    def __init__(self):
        self.index = 0
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
        self.openchat = "none"
        self.participants_num=0
        self.active = "enabled"
        self.image = "default"
        self.participants_id = []

    def make_hangout_data(self,Hangout,filterVal):
        #Hangout.meet_time = datetime.strptime(Hangout.meet_time,"%y-%m-%d %H:%M:%S")
        #print("--------")
        #print(Hangout.meet_time)
        self.participants_id = str_to_li(Hangout.participants_id)
        for i in range(4-len(str_to_li(Hangout.participants_id))):
            self.participants_id.append("none")

        self.image = Hangout.image

        if Hangout.meet_time < datetime.now():
            self.join = "Expired"
            self.active ="disabled"
            self.join_url ="/"
            self.openchat = "none"

        elif 'user_id' in session and session['user_id'] in str_to_li(Hangout.participants_id) or session['user_id']=='2129422973':
            self.join="cancel"
            self.join_url = "/hangout/cancel"
            self.openchat = Hangout.openchat

        elif Hangout.participants_num >=4:
            self.join = "\"No Seat\""
            self.join_url ="/"
            self.openchat = "none"
            self.active="disabled"

        elif 'user_id' in session and session['user_id'] not in str_to_li(Hangout.participants_id):
            self.join = "join"
            self.join_url = "/hangout/join"
            self.openchat = Hangout.openchat


        else:
            print("make_hangout_data error")
        print(self.join)


        month_list = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        st = ["1","21","31"]
        nd = ["2","22"]
        rd = ["3","23"]
        self.index = Hangout.idx
        self.title = Hangout.title

        #self.meet_time = Hangout.meet_time

        month = Hangout.meet_time.strftime("%m")
        month = month_list[int(month)-1]
        day = str(int(Hangout.meet_time.strftime("%d")))
        if day in st:
            day = day+"st"
        elif day in nd:
            day = day+"nd"
        elif day in rd:
            day = day+"rd"
        else:
            day = day+"th"
        hour = Hangout.meet_time.strftime("%H")
        minute = Hangout.meet_time.strftime("%M")
        self.meet_time = day + " "+month +" "+ hour + ":"+minute

        self.location = Hangout.location
        self.location_url = Hangout.location_url
        self.participants_num = Hangout.participants_num



        images = str_to_li(Hangout.participants_image)
        nations = str_to_li(Hangout.participants_nation)
        ages = str_to_li(Hangout.participants_age)
        gender = str_to_li(Hangout.participants_gender)

        path = "./static/profileImage/"
        file_list = os.listdir(path)

        # 이미지 나라 설정

        # 내가 참여한  행ㅇ아웃
        if self.join == "cancel"  or self.join == "Expired":
            for i in range(Hangout.participants_num):
                if images[i]+".png" not in file_list:
                    self.profile_image.append("bird")
                else:
                    self.profile_image.append(images[i])
                self.nation_image.append(nations[i])
                #self.nation_image.append('nation')
                self.age.append(ages[i])
                self.gender.append(gender[i])

            for i in range(4-Hangout.participants_num):
                self.profile_image.append("person")
                self.nation_image.append("nation")
                self.age.append("?")
                self.gender.append("?")
        else:
            for i in range(Hangout.participants_num):
                self.profile_image.append("bird")
                self.nation_image.append('nation')
                self.age.append(" ")
                self.gender.append(" ")

            for i in range(4-Hangout.participants_num):
                self.profile_image.append("bird")
                self.nation_image.append("nation")
                self.age.append(" ")
                self.gender.append(" ")

        # it is my hangout
        #print(str_to_li(Hangout.participants_id))










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
        self.woman=0
        self.man=0
        self.location_url=""
        self.korean=0
        self.foreign=0
        self.image = "default"
#print(datetime.now())
    def create_hangout(self, request,filename):
        self.openchat = request.form.get('openchat')
        self.location = request.form.get('location')
        self.title = request.form.get('title')
        day = request.form.get('day')
        month = request.form.get('month')
        hour = request.form.get('hour')
        minute = request.form.get('minute')
        #self.meet_time = datetime.now().strftime('%y-%m-%d %H:%M:%S')
        self.meet_time = "2022-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)
        #self.meet_time = request.form.get('meet_time')
        self.register_time = datetime.now().strftime('%y-%m-%d %H:%M')
        self.city= request.form.get('city')
        self.location_url = request.form.get('location_url')

        # 이미지 처리

        self.image = filename


class HangoutDao():
    def __init__(self):
        self.database = bappy_db.Database()

    def find_user_li(self,users_id,user_id):
        for i in range(len(users_id)):
            if users_id[i] ==  user_id:
                return i
        return "there are no user id"

    def get_hangout_byidx(self,idx):
        sql = """select * from bp_hangout where  idx = %s"""%(idx)
        return self.database.executeOne(sql)

    def cancel_hangout_byidx(self,idx,user_id, user_nation, user_gender, user_age):
        hangout = self.get_hangout_byidx(idx)
        users_id = str_to_li(hangout['hg_participants_id'])
        users_nation = str_to_li(hangout['hg_participants_nation'])
        users_image = str_to_li(hangout['hg_participants_image'])
        users_age = str_to_li(hangout['hg_participants_age'])
        users_gender = str_to_li(hangout['hg_participants_gender'])
        users_num = hangout['hg_participants_num']
        users_man = hangout['hg_man']
        users_woman = hangout['hg_woman']
        users_korean = hangout['hg_korean']
        users_foreign = hangout['hg_foreign']

        index = self.find_user_li(users_id, user_id)
        print("삭제해야할 인덱스는 ",index)
        users_id.pop(index)
        users_nation.pop(index)
        users_image.pop(index)
        users_age.pop(index)
        users_gender.pop(index)
        users_num -= 1

        if session['user_info']['user_isKorean'] == 1:
            users_korean -=1
        else:
            users_foreign -=1


        if user_gender == 'M':
            users_man -= 1
        else:
            users_woman -= 1

        users_id = list_to_str(users_id)
        users_nation = list_to_str(users_nation)
        users_image = list_to_str(users_image)
        users_gender = list_to_str(users_gender)
        users_age = list_to_str(users_age)
        users_num = str(users_num)


        return self.update_hangout(users_korean,users_foreign,idx, users_image,users_id, users_nation, users_gender, users_age,users_num, users_man, users_woman)


    def update_hangout(self,users_korean,users_foreign,idx,users_image, users_id, users_nation, users_gender, users_age, users_num, users_man, users_woman):
        sql = """ update bp_hangout set hg_korean = %d, hg_foreign = %d, hg_man = '%s', hg_woman = '%s', hg_participants_id = '%s', hg_participants_nation = '%s', hg_participants_image = '%s', hg_participants_age = '%s', hg_participants_gender = '%s', hg_participants_num = '%s' where idx = '%s'"""% (users_korean,users_foreign,users_man,users_woman,users_id,users_nation,users_image,users_age,users_gender, users_num, idx)
        self.database.execute(sql)
        return "true"

    def checkTimeHangout(self,joinIndex,myHangoutIndex):
        joinTime = self.get_hangout_byidx(joinIndex)['hg_meet_time']
        #joinTime = datetime.strptime(joinTime,"%y-%m-%d %H:%M:%S")
        if myHangoutIndex == None or myHangoutIndex == "":
            return "true"
        sql = """
        select hg_meet_time from bappy_web.bp_hangout where idx in(%s)"""%(myHangoutIndex)
        res = self.database.executeAll(sql)

        if res == None:
            return "true"

        for hangoutTime in res:
            #date_diff = joinTime - datetime.strptime(hangoutTime,"%y-%m-%d %H:%M:%S")
            date_diff = abs(joinTime - hangoutTime['hg_meet_time'])
            if date_diff.total_seconds() / 3600 <= 4:
                #print(hangoutTime['hg_meet_time'])
                #print(joinTime)
                #print(date_diff.total_seconds())
                return "false"

        return "true"


    def checkCancelTime(self, cancelIndex):
        #print("cancel idx : ",cancelIndex)
        cancelTime = self.get_hangout_byidx(cancelIndex)['hg_meet_time']
        #print(cancelTime)
        now = datetime.now()
        diff = abs(cancelTime - now)
        print(diff.seconds)
        print(diff.days)
        if(diff.days == 0 and diff.seconds <= 3600):
            print("1시간 미만 남은 행아웃 캔슬")
            return False
        else:
            print("1시간 이상 남은 행아웃 캔슬")
            return True

    def join_hangout_byidx(self,myHangout,idx,user_id, user_nation, user_gender, user_age):
        #print("my hangout", myHangout)
        if self.checkTimeHangout(idx,myHangout)=="false":
            print("cant join cause time")
            return 1


        hangout = self.get_hangout_byidx(idx)


        # 성별 제한  없애기
        #
        #if user_gender == "M":
        #    if hangout["hg_man"]>= 2:
        #        return 0
        #else:
        #    if hangout["hg_woman"]>=2:
        #        return 0

        # 국가제한 2 2
        #if session['user_info']['user_isKorean'] == 1:
        #    if hangout["hg_korean"]>=2:
        #        return 0
        #else:
        #    if hangout["hg_foreign"]>=2:
        #        return 0


        users_id = str_to_li(hangout['hg_participants_id'])
        users_nation = str_to_li(hangout['hg_participants_nation'])
        users_image = str_to_li(hangout['hg_participants_image'])
        users_age = str_to_li(hangout['hg_participants_age'])
        users_gender = str_to_li(hangout['hg_participants_gender'])
        users_num = hangout['hg_participants_num']
        users_man = hangout['hg_man']
        users_woman = hangout['hg_woman']
        users_korean = hangout['hg_korean']
        users_foreign = hangout['hg_foreign']

        # 같은 국가 3명 이상 안됨
        tot = 0
        for nation in users_nation:
            if nation == user_nation:
                tot = tot + 1
        print(tot)
        if tot >=2:
            return 0

        if session['user_info']['user_isKorean']==1:
            users_korean +=1
        else:
            users_foreign +=1


        if user_gender == "M":
            users_man += 1
        else:
            users_woman += 1



        users_id.append(user_id)
        users_nation.append(user_nation)
        users_image.append(user_id)
        users_gender.append(user_gender)
        users_age.append(user_age)
        users_num +=1

        users_id = list_to_str(users_id)
        users_nation = list_to_str(users_nation)
        users_image = list_to_str(users_image)
        users_gender = list_to_str(users_gender)
        users_age = list_to_str(users_age)
        users_num = str(users_num)

        sql = """ update bp_hangout set hg_korean = %d, hg_foreign = %d,hg_man = '%s', hg_woman = '%s', hg_participants_id = '%s', hg_participants_nation = '%s', hg_participants_image = '%s', hg_participants_age = '%s', hg_participants_gender = '%s', hg_participants_num = '%s' where idx = '%s'"""% (users_korean,users_foreign,users_man,users_woman,users_id,users_nation,users_image,users_age,users_gender, users_num, idx)

        self.database.execute(sql)

        return "true"




    def count_hangout(self):
        sql = """select count(0) as cnt from bp_hangout"""
        return self.database.executeAll(sql)[0]['cnt']

    #def insert_hangout(self, hangout):

    #    sql = """
    #    INSERT INTO bp_hangout (hg_korean,hg_foreign,hg_location_url,hg_man,hg_woman,hg_city,idx, hg_participants_num, hg_click_num, hg_openchat, hg_location, hg_title, hg_meet_time, hg_register_time)
    #    VALUES (%d,%d,'%s',%d,%d,'%s',%d, %d, %d, '%s', '%s', '%s', '%s', '%s')
    #    """%(0,0,hangout.location_url,0,0,hangout.city,hangout.idx, hangout.participants_num, hangout.click_num,hangout.openchat,hangout.location,hangout.title,hangout.meet_time,hangout.register_time)
        #print(sql)
    #    self.database.execute(sql)
    def get_last_idx(self):
        sql = """SELECT max(idx) FROM bp_hangout"""
        return self.database.executeAll(sql)[0]['max(idx)']

    def insert_hangout(self, hangout):
        hangout.idx = self.get_last_idx()+1
        sql = """
        INSERT INTO bp_hangout (hg_image,hg_korean,hg_foreign,hg_location_url,hg_man,hg_woman,hg_city,idx, hg_participants_num, hg_click_num, hg_openchat, hg_location, hg_title, hg_meet_time, hg_register_time)
        VALUES ('%s',%d,%d,'%s',%d,%d,'%s',%d, %d, %d, '%s', '%s', '%s', '%s', '%s')
        """%(hangout.image,0,0,hangout.location_url,0,0,hangout.city,hangout.idx, hangout.participants_num, hangout.click_num,hangout.openchat,hangout.location,hangout.title,hangout.meet_time,hangout.register_time)
        #print(sql)
        self.database.execute(sql)

    def get_hangout_list(self,pageNum,filterVal):
        if filterVal == "default": #default
            #print(pageNum)
            print("It is default hangout list")
            #print("%d ~ %d"%(pageNum,pageNum+5))
            sql = """
            select * from bp_hangout where hg_meet_time >= '%s' order by hg_meet_time asc, idx asc limit %d,%d;
            """%( (datetime.now()+timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M:%S"),pageNum,5)
            #print(sql)
        elif filterVal == "complete":
            print("It is completed hangout list")
            sql = """
                select * from bp_hangout where hg_participants_num >= 2  and hg_meet_time < '%s' order by hg_meet_time desc, idx asc limit %d,%d;
            """%(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),pageNum,5)

        elif filterVal == "myhangout": #my hangout
            if session['user_info']['user_my_hangout']=="None" or session['user_info']['user_my_hangout']=="":
                return []
            print("It is myhangout list")
            sql = """select * from bp_hangout where idx in(%s) and hg_meet_time >= '%s' order by hg_meet_time asc, idx asc limit %d,%d"""%(session['user_info']['user_my_hangout'],datetime.now().strftime("%Y-%m-%d %H:%M:%S"),pageNum,5)
            #print(sql)
        #나머지 도시들
        else:
            print("It is "+str(filterVal)+"hangout list")
            sql = """
            select * from bp_hangout where hg_city=\'%s\' and hg_participants_num !=4 and hg_meet_time >= '%s' order by hg_meet_time asc, idx asc limit %d,%d;
            """%(filterVal,(datetime.now()+timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),pageNum,5)

        #sql = """
        #select * from bp_hangout order by hg_meet_time asc limit %d,%d;
        #"""%(pageNum,5)
        res = self.database.executeAll(sql)
        hangout_list = []

        for h in res:
            hangout = Hangout(h['idx'])
            hangout.idx = h['idx']
            hangout.participants_id = h['hg_participants_id']
            hangout.participants_nation = h['hg_participants_nation']
            hangout.participants_image = h['hg_participants_image']
            hangout.participants_num = h['hg_participants_num']
            hangout.click_num = h['hg_click_num']
            hangout.openchat = h['hg_openchat']
            hangout.location = h['hg_location']
            hangout.title = h['hg_title']
            hangout.participants_gender = h['hg_participants_gender']
            hangout.participants_age = h['hg_participants_age']

            hangout.meet_time = h['hg_meet_time']
            hangout.register_time = h['hg_register_time'].strftime("%Y-%m-%d %H:%M")
            hangout.city = h['hg_city']
            hangout.man = h['hg_man']
            hangout.woman = h['hg_woman']
            hangout.location_url = h['hg_location_url']
            if h['hg_image'] == None or h['hg_image'] == "":
                hangout.image = "default"
            else:
                hangout.image = h['hg_image']
            hangout_list.append(hangout)
        return hangout_list

    def get_hangout_data_list(self,filterVal,pageNum=0):
        hl = self.get_hangout_list(pageNum,filterVal)
        hangout_data_list = []
        for h in hl:
            hangout_data = Hangout_Data()
            hangout_data.make_hangout_data(h,filterVal)
            hangout_data_list.append(hangout_data)
        return hangout_data_list

    def list_to_str(self,li):
        if len(li)==1:
            return str(li[0])
        for i in range(len(li)):
            li[i]=str(li[i])
        return ','.join(li)
    # "1,2,3,4"->[1,2,3,4]
    def str_to_li( self,db_str):
        db_str = str(db_str)
        if db_str == "None":
            return []
        if db_str ==  "":
            return []
        return db_str.split(',')

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
