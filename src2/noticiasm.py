from datetime import datetime
from datetime import date, datetime, timedelta

import pymysql
import sys
import re
import configparser

class Noticia(): 

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('analizer.cfg')
        # Nuestros Campos
        self.id = 0
        self.bulletin = ""
        self.bulletin_year = 0
        self.bulletin_no = 0
        self.bulletin_date = datetime.now()
        self.organization = ""
        self.newname = ""
        self.url = ""
        self.fav = 0
        self.notify = 0
        self.readed = 0
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        # Campos nuevos
        self.seccion   = ""
        self.organismo = ""
        self.organo    = ""
        self.servicio  = ""        

        self.__meses = ['xaneiro','febreiro','marzo','abril','maio','xuño','xullo','agosto','setembro','outubro','novembro','decembro'] 

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
        self.__tablename = "noticias"

    def imprimir(self):
        self.upper()
        print ("Sección: "   + self.seccion)
        print ("Organismo: " + self.organismo)
        print ("Órgano: "    + self.organo)
        print ("Servicio: "  + self.servicio)
        print ("Noticia: "   + self.newname)
        print ("Url: "       + self.url)
        print ("----------------------------------------------------------------------------")

    def save(self):
        self.upper()
        cursor = self.__db.cursor()
        sql = "INSERT INTO " + self.__tablename
        sql += "(bulletin, bulletin_year, bulletin_no, bulletin_date, seccion, organismo, organo, servicio, organization, newname,"
        sql += " url, fav, notify, readed, created_at, updated_at)"
        sql += " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)"

        recordTuple = (self.bulletin, self.bulletin_year, self.bulletin_no, self.bulletin_date, self.seccion, self.organismo, self.organo, self.servicio, self.organization, self.newname, self.url, self.fav, self.notify, self.readed, self.created_at, self.updated_at)
        try:
           cursor.execute(sql,recordTuple)
           self.__db.commit()
        except Error as e:
           self.__db.rollback()
           print("No se ha podido introducir el dato: ")
        #self.__db.close()
        
    def checkNumber(self,year, numero, bulletin): 
        cursor = self.__db.cursor()
        sql = "SELECT * FROM " + self.__tablename + " WHERE bulletin_no = %s AND bulletin_year = %s AND bulletin = %s "
        cursor.execute(sql,(numero,year,bulletin))
        rows = cursor.fetchall()
        if (cursor.rowcount == 0):
            return False        
        return True
    
    def upper(self): 
        self.bulletin     = self.bulletin.upper()    
        self.organization = self.organization.upper()
        self.seccion      = self.seccion.upper()
        self.organismo    = self.organismo.upper()
        self.organo       = self.organo.upper()
        self.servicio     = self.servicio.upper()
        self.newname      = self.newname.upper()

    