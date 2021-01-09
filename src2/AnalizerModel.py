from datetime import date, datetime, timedelta

import pymysql
import sys
import re
import configparser

class AnalizerModel(): 

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('analizer.cfg')
        # Nuestros Campos
        self.id = 0
        self.name = ""
        self.active = 0
        self.classname = ""
        self.module = ""
        self.description = ""
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        self.__loadDBConnection()
        try:
            self.__db = pymysql.connect(self.__host,self.__user,self.__password,self.__db)
        except: 
            print("Database don't connected !")            

    def __loadDBConnection(self): 
        self.__host      = "db" 
        self.__user      = "root"
        self.__db        = "analizerdb"
        self.__password  = "test"
        self.__tablename = "analizers"

    def imprimir(self):
        print ("Id: "   + str(self.id))
        print ("Nombre: " + self.name)
        print ("Classname: "    + self.classname)
        print ("Modulo: " + self.module)
        print ("Descripción: "  + str(self.description))
        print ("Fecha Creación: "   + str(self.created_at))
        print ("Fecha Actualización: "   + str(self.updated_at))
        print ("----------------------------------------------------------------------------")

    def save(self):
        #self.upper()
        cursor = self.__db.cursor()
        sql = "INSERT INTO " + self.__tablename
        sql +=  " (`name`,`active`,`classname`, `module`,`description`,`created_at`,`updated_at`)"
        sql += "  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        recordTuple = (self.name, self.active, self.classname, self.module, self.description, self.created_at, self.updated_at)
        try:
           cursor.execute(sql,recordTuple)
           self.__db.commit()
        except Error as e:
           self.__db.rollback()
           print("No se ha podido introducir el dato: ")
        #self.__db.close()
        
    def getActive(self): 
        cursor = self.__db.cursor()
        sql = "SELECT `id`, `name`,`active`,`classname`, `module`,`description`,`created_at`,`updated_at` "
        sql += " FROM " + self.__tablename + " WHERE `active` = 1 "
        cursor.execute(sql)

        resultados = []
        for row in cursor: 
            obj = AnalizerModel()
            obj.id = row[0]
            obj.name = row[1]
            obj.active = row[2]
            obj.classname = row[3]
            obj.module    = row[4]
            obj.description = row[5]
            obj.created_at = row[6]
            obj.updated_at = row[7]
            resultados.append(obj)            

        return (resultados)
    
