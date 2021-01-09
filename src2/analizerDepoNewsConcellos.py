from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from analizer import Analizer
import time

#import re
class Noticia(): 

    def __init__(self):
        self.id      = 0
        self.url     = ""
        self.title   = ""
        self.entry   = ""
        self.text    = ""
        self.date    = ""
        self.council = ""
    
    def print(self):
        print("Título: " + self.title)
        print("Url: " + self.url)
        print("Fecha: " + self.date)
        print("Concello: " + self.council)
        print("---------------------------------------------------------------------------------------------")


class AnalizerDepoNewsConcellos: 

    def __init__(self):
        self.__name = "Concellos Pontevedra"
        self.news = []

    def analizeGeneral(self,url):
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

            noticia_m = Noticia()
            noticias_list = res.find("ul",{"class":"listNoticias"})
            noticias = noticias_list.findAll("li")
            for noticia in noticias: 
                noticia_m.url = 'https://www.depo.gal' + noticia.a['href'].strip()
                tmp = noticia.find("div",{"class","fecha_noticia"})
                noticia_m.date = tmp.span.getText()
                noticia_m.council = noticia.find("span",{"class":"concello"}).span.getText()

                self.analizeNew(noticia_m)
                noticia_m.print()
                #self.news.append(noticia_m)

    def analizeNew(self,new_tmp):
        print(new_tmp.url)
        try: 
            html = urlopen(new_tmp.url)
        except HTTPError as e:
            print(e)
        except URLError as u:
            print("Servidor depo no encontrado " + url)
            print(u)
        else:
            content = html.read().decode('utf-8', 'ignore')
            res = BeautifulSoup(content,"html.parser")

            tmp = res.find("div",{"class":"noticias_detalle"})
            new_tmp.title = tmp.find("h2").getText()

            new_tmp.print()




    def run(self): 
        self.analizeGeneral("https://www.depo.gal/noticias-concellos")
    
    def imprimir(self):
        print ("Soy AnalizerDepo")


## aqúi el main

a = AnalizerDepoNewsConcellos()
#a.analizeConcello("https://www.depo.gal/web/edepo/-/concellos-guarda")
a.run()