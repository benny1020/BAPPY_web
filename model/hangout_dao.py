import json
from flask import Flask, request, session, jsonify
from . import bappy_db

host = '18.118.131.221'
db_id = 'benny'
pw = 'benny'
db_name = 'bappy_web'

class hangout():
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


class HangoutDao():
    def __init__(self):
        self.database = bappy_db.Database()

    def hangout_insert():
