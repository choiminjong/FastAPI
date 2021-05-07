import time
import datetime

#databases utili  
import pymysql
from dataclasses import asdict
from app.config.environment import conf

class DBConnector :

    def __init__(self, mod='test', type="") :

        # Mod에 따라 DB modConfig 변경
        dbData={}
        for configData in [config.split("=") for config in asdict(conf(mod))[type].split(";")] :
            dbData[configData[0]]=configData[1]

        self.__host     = dbData['HOST']
        self.__user     = dbData['USER']
        self.__password = dbData['PWD']
        self.__database = dbData['DB']
        self.__charset  = dbData['CHARSET']

    def __open(self):
        try:
            cnx =  pymysql.connect(host=self.__host, user=self.__user, password=self.__password, db=self.__database, charset=self.__charset)
            self.__connection = cnx
            self.__session = cnx.cursor(pymysql.cursors.DictCursor)       

        except pymysql.connector.Error as e:
            print ("Error %d: %s" % (e.args[0],e.args[1]))
    ## End def __open

    def __close(self):
        self.__session.close()
        self.__connection.close()
    ## End def __close

    def select(self,Query):
        self.__open()
        self.__session.execute(Query)
        number_rows = self.__session.rowcount
        number_columns = len(self.__session.description)

        if number_rows >= 1 and number_columns > 1:
            result = [item for item in self.__session.fetchall()]
        else:
            result = [item[0] for item in self.__session.fetchall()]
        self.__close()
        
        return result

    def insert(self, table, *args, **kwargs):
        values = None
        query = "INSERT INTO %s " % table
        if kwargs:
            keys = kwargs.keys()
            values = tuple(kwargs.values())
            query += "(" + ",".join(["`%s`"] * len(keys)) %  tuple (keys) + ") VALUES (" + ",".join(["%s"]*len(values)) + ")"
        elif args:
            values = args
            query += " VALUES(" + ",".join(["%s"]*len(values)) + ")"

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()
        self.__close()

        return self.__session.lastrowid

    def update(self, table, where=None, *args, **kwargs):
        query  = "UPDATE %s SET " % table
        keys   = kwargs.keys()
        values = tuple(kwargs.values()) + tuple(args)
        l = len(keys) - 1
        for i, key in enumerate(keys):
            query += "`"+key+"` = %s"
            if i < l:
                query += ","
   
        ## End for keys
        query += " WHERE %s" % where

        self.__open()
        self.__session.execute(query, values)
        self.__connection.commit()

        # Obtain rows affected
        update_rows = self.__session.rowcount
        self.__close()

        return update_rows
    ## End function update