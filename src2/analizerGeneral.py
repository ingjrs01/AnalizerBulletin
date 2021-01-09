#!/usr/bin/python3

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
        self.__tablename = "noticias"
    
    # Busca si la noticia contiene una serie de palabras
    def isNotificable(selft, new):
        words = ['OPOSICIÓN', 'SELECTIVOS', 'FUNCIONARIO','EMPREGO']
        for word in words:
            if (word in new):
                return True

        return False

    def analizeWebDepo(self,url):
        try: 
            html = urlopen(url)
        except HTTPError as e:
            print(e)
        except URLError as u:
            print("Servidor depo no encontrado " + url)
            print(u)
        else:
            content = html.read().decode('utf-8', 'ignore')
            res = BeautifulSoup(content,"html.parser")             
            print(res.find("h2",{"class":"numero"}).getText())
            numero = int(res.find("h2",{"class":"numero"}).getText().split()[2])
            # Obtener el año
            info = res.find("span",{"class":"fecha"}).getText().split()
            year = int(info[len(info)-4])
            mes = self.__meses.index(info[len(info)-6]) + 1 # El array comienza en 0
            dia = int(info[len(info)-8])
            fecha = date(year, mes, dia)

            if (self.checkNumber(year,numero,"BOPO") == False):
                tags = res.findAll("ul",{"class":"listadoSumario"})

                for tag in tags:
                    lis = tag.findAll("li")
                    for li in lis: 
                        cabecera = li.span.getText()
                        titulo   = li.p.getText()
                        if (self.isNotificable(titulo)):
                            notify = 1
                        else:
                            notify = 0

                        uri      = "https://boppo.depo.gal" + li.a['href']
                        self.insertLine("BOPO",numero,year ,cabecera,titulo,uri,notify,fecha)
            else:
                print ("Paso al siguiente")

    def analizeWebXunta(self,url):
        try: 
            html = urlopen(url)
        except HTTPError as e:
            print(e)
        except URLError:
            print("Servidor no encontrado")
        else:        
            content = html.read().decode('utf-8', 'ignore')
            res = BeautifulSoup(content,"html.parser")
            info = res.find("div",{"id":"publicacionInfo"})
            numero = int(info.span.getText().split()[1]) 
            # obtener el año. 
            info = res.find("span",{"id":"DOGData"})
            temp = info.getText().split()
            year = int(temp[len(temp)-1])
            mes = self.__meses.index(temp[len(temp)-3]) + 1
            dia = int(temp[len(temp)-5])
            fecha = date(year,mes,dia)

            if  (self.checkNumber(year, numero,"DOGA") == False):
                sections = res.findAll("div",{"id":re.compile('secciones*')})
                for section in sections:
                    lines = section.findAll("li")
                    for line in lines:
                        if (line.a is not None): 
                            cabecera = "N/D"
                            titulo   = line.a.getText() # laalala
                            uri      = "https://www.xunta.gal" + line.a['href'] 
                            self.insertLine("DOGA",numero, year, cabecera,titulo,uri,1,fecha)
            else: 
                print ("Pasando Xunta")

    def insertLine(self, bulletin, bulletin_no, bulletin_year,heading, title, urline, notify,fecha):
        cursor = self.__db.cursor()
        sql = "INSERT INTO " + self.__tablename
        sql += "(bulletin,bulletin_year, bulletin_no, organization, newname, url,fav , notify, readed,created_at,bulletin_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)"
        organization = heading
        newname = title
        url = urline
        readed = 0
        fav = 0
        created = datetime.now()
        recordTuple = (bulletin, bulletin_year, bulletin_no, organization, newname, url,fav ,notify, readed,created,fecha)
         
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

    def urlGeneratorDepo(self): 
        urls = ["https://boppo.depo.gal/web/boppo"]
        hoy = datetime.now()
        tempdate = hoy
        for i in range(1,self.__days):
            tempdate = tempdate - timedelta(days=1)
            if (tempdate.weekday() not in [5,6]): 
                url = "https://boppo.depo.gal/detalle/-/boppo/" + str(tempdate.year) + "/" + format(tempdate.month, '02') + "/" + format(tempdate.day, '02')
                urls.append(url)

        return urls

    def run(self): 
        #self.registerListener()
        l = self.urlGeneratorDepo()
        for item in l:
            self.analizeWebDepo(item)

        l2 = self.urlGeneratorXunta()
        for item in l2:
            self.analizeWebXunta(item)

        self.getData()

    def log(self, msg):
        print(type(msg))
        if (type(msg) != bytes):
            print (msg.encode("utf-8", errors="ignore"))

    # Función experimental. para sacar las urls de las distintas secciones    
    def analizarPrincipal(self, url): 
        urls_in = []
        try: 
            html = urlopen(url)
        except HTTPError as e:
            print("Error: " + e)
        except URLError:
            print("Servidor no encontrado")
        else:        
            content = html.read()
            res = BeautifulSoup(content,"html.parser")
            index = res.find("div",{"class","contidoDesplegado"})    
            lis = index.findAll("li",{"class","dog-toc-sumario"})
            for li in lis:
                if (li.a is not None):
                    if (li.a.getText().find('concursos') > 0):
                        urls_in.append("https://www.xunta.gal/diario-oficial-galicia/" + li.a['href'])
        return urls_in

# Seccion principal a ejecutar.
num_days = 1
if (len(sys.argv) > 1):
    print ("Cuantos dias analizar: " + sys.argv[1])
    num_days = int(sys.argv[1])

p = Analizer(num_days)
p.run()


