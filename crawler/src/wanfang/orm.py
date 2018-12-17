# coding=utf-8
# date:下午1:15 
# author:chenjunbiao
import pymysql


class Mysql(object):
    def __init__(self, host="", user='', password="", database=''):
        self.host = host
        self.password = password
        self.database = database
        self.user = user
        self.charset = 'utf8'
        self.db = None
        self.cursor = None

    def __del__(self):
        self.db.close()

    def connect(self):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset=self.charset)
        self.cursor = self.db.cursor()

    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except BaseException as e:
            print(e)
            self.db.rollback()

    def update(self, sql):
        self.insert(sql)

    def fetch_one(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchone()
        return results

    def fetch_all(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    @staticmethod
    def get_connection_instance(db_config):
        with open(db_config, 'r') as f:
            line = f.readline()
            db_config = line.split(',')
        mysql = Mysql(db_config[0], db_config[1], db_config[2], db_config[3])
        mysql.connect()
        return mysql
