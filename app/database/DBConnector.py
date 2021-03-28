import time
import datetime

#DB
import pymysql
from app.common.consts import Mysql

class DBConnector :

    def __init__(self):
        self._conn = pymysql.connect(host=Mysql.HOST, user=Mysql.USER, password=Mysql.PASSWORD, db=Mysql.DATABASES, charset=Mysql.CHARSET)
        self._cursor = self._conn.cursor(pymysql.cursors.DictCursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._conn.close()

    def fetchall(self, selectQuery):
        self._cursor.execute(selectQuery)
        return self._cursor.fetchall()

    def fetchone(self,selectQuery):
        self._cursor.execute(selectQuery)
        return self._cursor.fetchone()

    def insertQuery(self, table, val) :
        columns_string = ",".join(val.keys())
        values_string = '"' + '","'.join(map(str, val.values())) + '"'
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table, columns_string, values_string)
        return sql

    def updateQuery(self, table, val, condition):

        # 데이터 합치기
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        executedata = {'updated_at': timestamp}
        executedata.update(dict(val))
        '''
        for key, value in executedata.items():
            if value is None:
                print ("None 1111!")
                return False
            elif value is "":
                print("None 222!")
                return False
        '''

        #데이터생성
        fiedle = format(', '.join('{}={}'.format(k,executedata[k]) for k in executedata))
        where = format(' and '.join('{}={}'.format(k,condition[k]) for k in condition))
        sql = "UPDATE  %s SET %s WHERE %s " % (table, fiedle, where)

        return sql

    def execute(self, Query):
        try:
            self._cursor.execute(Query)
            self._conn.commit()
        except pymysql.Error as e:
            self._conn.rollback()
            self._conn.close()
            raise
        else:
            self._conn.commit()
            self._conn.close()
