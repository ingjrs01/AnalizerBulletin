from datetime import date, datetime, timedelta

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
            self.db = pymysql.connect(self.__host,self.__user,self.__password,self.__db)
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
        cursor = self.db.cursor()

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
            self.db.commit()
        except: 
            self.db.rollback()
            print("Error actualizando las filas vistas")
        
    def checkNumber(self,year, numero, bulletin):             
        cursor = self.db.cursor()
        sql = "SELECT * FROM " + self.__tablename + " WHERE bulletin_no = %s AND bulletin_year = %s AND bulletin = %s "
        cursor.execute(sql,(numero,year,bulletin))
        rows = cursor.fetchall()
        if (cursor.rowcount == 0):
            return False        
        return True

    def checkBulletinExists(self,bulletin,fecha):
        cursor = self.db.cursor()
        sql = "SELECT `id` FROM `analyses` WHERE `analysis_date` = %s AND " + bulletin.lower() + " = 'FINALIZADO' "        
        cursor.execute(sql,(fecha))
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

    def work(self):
        for a in self.__analizers:
            a.run()
        return True

    def beginAnalysis(self,adate): 	
        cursor = self.db.cursor()
        sql = "SELECT id FROM `analyses` WHERE `analysis_date` = %s "
        cursor.execute(sql,(adate))
        rows = cursor.fetchall()
        if (cursor.rowcount > 0):
            return False        

        sql = "INSERT INTO `analyses` (`analysis_date`,`doga`,`boppo`,`bopco`,`boplu`,`bopou`,`created_at`,`updated_at`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        now = datetime.now()     
        estado = 'CREADO'   

        recordTuple = (adate,estado,estado,estado,estado,estado, now, now)
        try:
           cursor.execute(sql,recordTuple)
           self.db.commit()
        except Error as e:
           self.db.rollback()
           print("No se ha podido introducir el dato: ")
         

        return True

    def setAnalysisState(self,bulletin,fecha,state): 
        cursor = self.db.cursor()
        fieldname = bulletin.lower()

        now = datetime.now()
        sql = "UPDATE `analyses` SET " + fieldname + " = %s, `updated_at` = %s WHERE `analysis_date` = %s"  
        recordTuple = (state, now, fecha)
        try:
           cursor.execute(sql,recordTuple)
           self.db.commit()
        except Error as e:
           self.db.rollback()
           print("No se ha podido introducir el dato: ")
        return True