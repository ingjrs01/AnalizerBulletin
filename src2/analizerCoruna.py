#!/usr/bin/python3

from datetime import datetime
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from noticiasm import Noticia

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
        self.__tablename = "entry"
    
    # Busca si la noticia contiene una serie de palabras
    def isNotificable(self, new):
        words = ['OPOSICIÓN', 'SELECTIVOS', 'FUNCIONARIO','EMPREGO']
        for word in words:
            if (word in new):
                return True

        return False

    def analizeWebDeco(self,url):
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

            #print(res.find("h2",{"class":"numero"}).getText())
            info = res.find("div",{"id":"infoBoletin"}).find("a").getText()
            cachos = info.split()
            numero = int(cachos[4])
            print (numero)
            dia = int(cachos[7])
            print (dia)
            mes = 11#self.__meses.index(cachos[9]) + 1
            ano = int(cachos[11])
            fecha = date(ano,mes,dia)
            print (fecha)

            anuncios = res.findAll("div",{"class":"bloqueAnuncio"})
            for anuncio in anuncios: 
                noticia = Noticia()
                #noticia.id = 0
                noticia.bulletin = "BOPCO"
                noticia.bulletin_year = ano
                noticia.bulletin_no = numero
                noticia.bulletin_date = fecha                
                ## Procesamos la información
                
                if (anuncio.find("h2")):
                    noticia.autonomia = anuncio.find("h2").getText()

                if (anuncio.find("h3")):
                    noticia.organismo = anuncio.find("h3").getText()

                if (anuncio.find("h4")):
                    noticia.organo = anuncio.find("h4").getText()

                if (anuncio.find("h5")):
                    noticia.servicio = anuncio.find("h4").getText()
                
                noticia.seccion = anuncio.findPrevious('h1',{"class":"administracion"}).getText()
                #for otro in otros: 
                resumen = anuncio.find("p",{"class":"resumenSumario"})
                noticia.url = "https://bop.dacoruna.gal/bopportal/publicado/" + str(ano) + "/" + str(mes) + "/" + str(dia) + "/" + resumen.select("a")[0]['href']
                noticia.newname = resumen.select("a")[0].getText().strip() + " - " + resumen.select("a")[1].getText().strip()
                # la notificación hay que comprobarla
                noticia.notify = 0
                noticia.organization = ""
                noticia.fav = 0
                noticia.readed = 0
                noticia.created_at = datetime.now()
                noticia.updated_at = datetime.now()
                noticia.imprimir()
                noticia.save()


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

    def urlGeneratorDeco(self): 
        urls = ["https://bop.dacoruna.gal/bopportal/ultimoBoletin.do"]
        hoy = datetime.now()
        tempdate = hoy
        for i in range(1,self.__days):
            tempdate = tempdate - timedelta(days=1)
            if (tempdate.weekday() not in [5,6]): 
                url = "https://bop.dacoruna.gal/bopportal/cambioBoletin.do?fechaInput=" + str(tempdate.day) + "/" + format(tempdate.month, '02') + "/" + format(tempdate.year, '04')
                urls.append(url)

        return urls


    def run(self): 
        #self.registerListener()
        lista = self.urlGeneratorDeco()
        for item in lista:
            print(item)
            self.analizeWebDeco(item)
            #self.analizeWebDepo(item)

        #l2 = self.urlGeneratorXunta()
        #for item in l2:
        #    self.analizeWebXunta(item)

        #self.getData()

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


