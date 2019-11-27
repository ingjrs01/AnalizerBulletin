from datetime import datetime
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from noticiasm import Noticia

import pymysql
import telebot
import re
import configparser
import requests
import time

class AnalizerDeou(): 

    def __init__(self,numero):
        config = configparser.ConfigParser()
        config.read('analizer.cfg')

        self.__days = numero
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
        self.__tablename = "entry"
    
    # Busca si la noticia contiene una serie de palabras
    def isNotificable(selft, new):
        words = ['OPOSICIÓN', 'SELECTIVOS', 'FUNCIONARIO','EMPREGO']
        for word in words:
            if (word in new):
                return True

        return False

    def analize(self):
        url = 'https://bop.depourense.es/portal/cambioBoletin.do'
        fechas = self.urlGenerator()
        for f in fechas:
            print (url + "   ." + f + ".")

        for fecha in fechas: 
            post_params = {'fechaInput':fecha}
            response = requests.post(url, data=post_params)   
            res = BeautifulSoup(response.text, 'html.parser')    

            sumario = res.find("div",{"class":"resumenSumario"}).getText().split()
            numero = int(sumario[4])
            year = int(sumario[11])
            mes =  11#self.__meses.index(info[len(info)-6]) + 1 # El array comienza en 0
            dia = int(sumario[7])
            fecha = date(year, mes, dia)
            v_url = "https://bop.depourense.es/portal/" + res.find("a",{"class":"enlacePdfS"})['href']

            if  (self.checkNumber(year,numero,"BOPOU") == False):
                grupo = res.findAll("td",{"class":"textoS","width":"90%"})

                for elemento in grupo:
                    noticia = Noticia()
                    noticia.newname = elemento.getText().strip()
                    noticia.organismo = elemento.findPrevious('span',{"class":"tituloS"}).getText()
                    noticia.seccion = elemento.findPrevious('span',{"class":"seccionS"}).getText()
                    noticia.bulletin = "BOPOU"
                    noticia.bulletin_year = year
                    noticia.bulletin_no = numero
                    noticia.bulletin_date = fecha
                    noticia.servicio  = ""
                    noticia.url = v_url
                    noticia.created_at = datetime.now()
                    noticia.updated_at = datetime.now()
                    if (self.isNotificable(noticia.newname)):
                        noticia.notify = 1

                    self.normalizar(noticia)
                    noticia.imprimir()
                    #noticia.save()
            else:
                print ("Paso al siguiente")
            print ("Esperando")
            time.sleep(10)
            print("Reanudando")

    def normalizar(self,noticia):
        if (noticia.seccion == "IV. ENTIDADES LOCAIS"):
            noticia.seccion = "Administración Local"

        if (noticia.seccion == "V. TRIBUNAIS E XULGADOS"):
            noticia.seccion = " ADMINISTRACIÓN DE XUSTIZA"
    
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
        fechas = []
        hoy = datetime.now()
        tempdate = hoy
        for i in range(1,self.__days):
            #tempdate = tempdate - timedelta(days=1)
            if (tempdate.weekday() not in [6]): # Publica los sábados
                sfecha = format(tempdate.day, '02') +  "/" + format(tempdate.month, '02') + "/" + str(tempdate.year)
                fechas.append(sfecha)
            tempdate = tempdate - timedelta(days=1)

        return fechas

    def run(self): 
        #self.registerListener()
        self.analize()
        self.getData()

    def prueba(self):
        print ("Analizando desde Ourense")