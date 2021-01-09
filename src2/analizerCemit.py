from datetime import datetime
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta

import pymysql
import telebot
import sys
import re
import configparser

class Analizer(): 

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('analizer.cfg')

        self.__tb = telebot.TeleBot(config['General']['TOKEN'])
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
    

    def analize(self,url):
        url = "https://cemit.xunta.gal/"
        url = "https://aulascemit.xunta.es/usuarios/spring/actividades?execution=e3s1"
        url = "https://cemit.xunta.gal/actividade/30379"
        url = "https://cemit.xunta.gal/gl/centro/5"
        try: 
            print (url)
            html = urlopen(url)
        except HTTPError as e:
            print(e)
            print ("No he podido abrir la página")
        except URLError:
            print("Servidor no encontrado")
        else:        
            content = html.read().decode('utf-8', 'ignore')
            res = BeautifulSoup(content,"html.parser")

            actividades = res.findAll("tr",{'class','rich-table-row'})
            for actividad in actividades: 
                # lalala
                print(actividad)
            return True


    def insertLine(self, bulletin, bulletin_no, bulletin_year,heading, title, urline, notify):
        cursor = self.__db.cursor()
        sql = "INSERT INTO " + self.__tablename
        sql += "(bulletin,bulletin_year, bulletin_no, organization, newname, url,fav , notify, readed,created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
        organization = heading
        newname = title
        url = urline
        readed = 0
        fav = 0
        created = datetime.now()
        recordTuple = (bulletin, bulletin_year, bulletin_no, organization, newname, url,fav ,notify, readed,created)
         
        try:
           cursor.execute(sql,recordTuple)
           self.__db.commit()
        except Error as e:
           self.__db.rollback()
           print("No se ha podido introducir el dato: ")
        #self.__db.close()
    
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

    def urlGeneratorXunta(self): 
        url_fija =  "https://www.xunta.gal/diario-oficial-galicia/mostrarContenido.do?ruta=/u01/app/oracle/shared/resources/pxdog100/doga/Publicados/"
        urls = []
        hoy = datetime.now()
        tempdate = hoy
        for i in range(1,self.__days+1):
            if (tempdate.weekday() not in [5,6]): 
                url = url_fija + str(tempdate.year) + "/" + str(tempdate.year) + format(tempdate.month, '02') + format(tempdate.day, '02')
                url += "/Secciones1_gl.html&paginaCompleta=false&fecha=" +  format(tempdate.day, '02') + "/" + format(tempdate.month, '02') + "/" + str(tempdate.year)
                url_tmp = self.analizarPrincipal(url)
                if (len(url_tmp) > 0):
                    for i in url_tmp:
                        urls.append(i)
            tempdate = tempdate - timedelta(days=1)

        return urls

    def run(self):         
        url = "https://cemit.xunta.gal/gl/actividades?idCentro=61"
        self.analize(url)

        #self.getData()


# Seccion principal a ejecutar.
p = Analizer()
p.run()


