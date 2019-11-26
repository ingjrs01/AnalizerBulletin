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
    def isNotificable(selft, new):
        words = ['OPOSICIÓN', 'SELECTIVOS', 'FUNCIONARIO','EMPREGO']
        for word in words:
            if (word in new):
                return True

        return False

    def analize(self):
        url = 'http://deputacionlugo.gal/boletin-oficial-da-provincia-de-lugo/ultimo-bop'
        url = 'http://deputacionlugo.gal/gl/node/72645'
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

            # Vamos a por el número: 
            grupo_codigo = res.find('div',{"class":"field--name-field-ail-codigo"})
            numero = int(grupo_codigo.find('div',{'class','field__item'}).getText())
            grupo_codigo = res.find('div',{'class','field--name-field-ail-bop-fecha-publicacion'})
            sfecha = grupo_codigo.find('div',{'class':'field__item'}).getText().split()
            dia = int(sfecha[1])
            mes = self.__meses.index(sfecha[3].lower()) + 1 
            anio = int(sfecha[5])
            fecha = date(anio,mes,dia)
            if (self.checkNumber(anio,numero,"BOPLU") == False):
                div = res.find("div",{"class":"field--name-field-ail-bop-contenido"})
                lista = div.find("ul")
                secciones = lista.children
                for seccion in secciones: 
                    if hasattr(seccion, 'strong'):                    
                        seccion_nombre = seccion.strong.getText()

                    if (not hasattr(seccion, 'children')):                    
                        continue
                        
                    lista = seccion.findChildren("ul" , recursive=False)
                    for elemento in lista:  
                        organismos = elemento.children
                        for organismo in organismos:
                            if hasattr(organismo, 'strong'):                    
                                v_concello = organismo.strong.getText()

                            if hasattr(organismo, 'ul'):
                                noticias = organismo.ul.children
                                for noticia_v in noticias:                     
                                    if hasattr(noticia_v,"a"):
                                        noticia = Noticia()
                                        noticia.bulletin = "BOPLU"
                                        noticia.bulletin_year = anio
                                        noticia.bulletin_no = numero
                                        noticia.bulletin_date = fecha
                                        noticia.created_at = datetime.now()
                                        noticia.updated_at = datetime.now()
                                        noticia.seccion   = seccion_nombre
                                        noticia.autonomia = ""
                                        noticia.organismo = v_concello
                                        noticia.organo    = v_concello
                                        noticia.servicio  = ""        
                                        noticia.organization = v_concello
                                        noticia.newname = noticia_v.a.getText()

                                        if (self.isNotificable(noticia.newname)):
                                            noticia.notify = 1

                                        noticia.url = "https://boppo.depo.gal" + noticia_v.a['href']
                                        self.normalizar(noticia)
                                        noticia.imprimir()
                                        #noticia.save()
            else:
                print ("Paso al siguiente")

    def normalizar(self,noticia):
        if (noticia.seccion == "XUNTA DE GALICIA"):
            noticia.seccion = "Administración Autonómica"
            noticia.organismo = "Xunta de Galicia"
        if (noticia.seccion == "EXCMA. DEPUTACIÓN PROVINCIAL DE LUGO"):
            noticia.seccion = 'Administración Local'
            noticia.organismo = "Deputación de Lugo"        
        if (noticia.seccion == "CONCELLOS"):
            noticia.seccion = 'Administración Local'
            noticia.organo = ""
            noticia.servicio = ""
        if (noticia.seccion == "MINISTERIO PARA A TRANSICIÓN ECOLÓXICA"):
            noticia.organismo = noticia.seccion
            noticia.seccion = "Administración Estatal"
            

    
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
        self.analize()
        self.getData()

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

