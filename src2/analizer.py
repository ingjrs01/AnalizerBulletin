#from urllib.request import urlopen
#from urllib.error import HTTPError
#from urllib.error import URLError
#from bs4 import BeautifulSoup
#from datetime import date, datetime, timedelta

import pymysql
import telebot
#import sys
import configparser

class Analizer(): 

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('analizer.cfg')

        self.__tb = telebot.TeleBot(config['General']['TOKEN'])
        self.meses = ['xaneiro','febreiro','marzo','abril','maio','xuño','xullo','agosto','setembro','outubro','novembro','decembro'] 

        self.__loadDBConnection()
        self.__analizers = []
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

    def addAnalizer(self,a):
        self.__analizers.append(a)

    # Busca si la noticia contiene una serie de palabras
    def isNotificable(self, new):
        n = new.upper()
        words = ['OPOSICIÓN', 'SELECTIVOS', 'FUNCIONARIO','EMPREGO']
        for word in words:
            if (word in n):
                return True

        return False

    def analize(self,url):
        return True

    def getData(self):
        cursor = self.__db.cursor()

        where = " WHERE `notify` = 1 "
        sql = " SELECT bulletin,bulletin_no,newname FROM " + self.__tablename + " " + where

        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            msg = row[0] + " " + str(row[1]) + " - " + row[2]
            self.sendTelegram(msg)
        sql = "UPDATE " + self.__tablename + " SET `notify` = 0 " + where
        try: 
            cursor.execute(sql)
            self.__db.commit()
        except: 
            self.__db.rollback()
            print("Error actualizando las filas vistas")
        
    def checkNumber(self,year, numero, bulletin):             
        cursor = self.__db.cursor()
        sql = "SELECT * FROM " + self.__tablename + " WHERE bulletin_no = %s AND bulletin_year = %s AND bulletin = %s "
        cursor.execute(sql,(numero,year,bulletin))
        rows = cursor.fetchall()
        if (cursor.rowcount == 0):
            return False        
        return True

    def sendTelegram(self, msj):
        self.__tb.send_message(172454149, msj)

    def listener(self, *mensajes): 
        for l in mensajes:
            if (type(l) == list): 
                for m in l:
                    chat_id = m.chat.id
                    if m.content_type == 'text':
                        text = m.text
                        self.__tb.send_message(chat_id,"Me copio de tu texto")
                        self.__tb.send_message(chat_id, text)
    
    def registerListener(self):
        self.__tb.set_update_listener(self.listener)
        #self.__tb.polling(True)

    def urlGenerator(self): 
        print ("urlGenerator de Padre")
        urls = []
        return urls

    def run(self): 
        l = self.urlGenerator()
        for item in l:
            self.analize(item)
        self.getData()

    def work(self):
        for a in self.__analizers:
            a.run()
