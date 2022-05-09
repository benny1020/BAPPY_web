import pymysql

class Database():
    def __init__(self):
        self.db = pymysql.connect(
            host='3.143.245.81',
            #host='127.0.0.1',
            user='thunder',
            password='thunder',
            db='bappy_web'
        )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query,args)
        self.db.commit()
        #self.db.close()

    def executeOne(self, query, args={}):
        self.cursor.execute(query,args)
        row = self.cursor.fetchone()
        #self.db.commit()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        #self.db.commit()
        return row
    def close(self):
        #self.db.commit()
        self.db.close()
