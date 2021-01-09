from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from noticiasm import Noticia
from analizer import Analizer
import time

#import re
class Concello(): 

    def __init__(self):
        self.id = 0
        self.name     = ""
        self.email    = ""
        self.web      = ""
        self.telefono = ""
        self.sede     = ""
        self.arquivo  = ""
        self.eiel     = ""
    
    def write(self):
        print(self.name + ";" + self.email + ";" + self.web + ";" + self.telefono + ";" + self.sede + ";" + self.arquivo + ";" + self.eiel)


class AnalizerDepoConcellos: 

    def __init__(self):
        self.__name = "Concellos Pontevedra"
        self.urls = []
        self.concellos = []

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

            concellos_list = res.find("ul",{"class":"listSede"})
            concellos = concellos_list.findAll("li")
            for concello in concellos: 
                #print(concello.a['href'])
                url = 'https://www.depo.gal' + concello.a['href']
                self.urls.append(url)

    def analizeConcello(self,url):
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
            concello = Concello()

            concello.name = res.find("div",{"class":"titular"}).getText()

            lista = res.find("div",{"class":"tablaDetalle"}).ul
            elementos = lista.findAll("li")
            for elemento in elementos:
                #print(elemento.strong)
                if elemento.find('strong'):
                    p = elemento.strong.getText()

                    if (p is not None):
                        if "Web" in p:
                            concello.web =  elemento.a['href']
                        if "e-mail" in p: 
                            concello.email = elemento.a['href'][7:]
                        if "Teléfono" in p: 
                            concello.telefono = elemento.getText()[11:]
                else:
                    if "Sede" in elemento.getText():
                        concello.sede =  elemento.a['href']
                    if "Arquivo" in elemento.getText():
                        concello.arquivo = elemento.a['href']
                    if "EIEL" in elemento.getText():
                        concello.eiel = elemento.a['href']

            self.concellos.append(concello)



            # Pasamos a analizar el concello en profundidad: 




    def run(self): 
        self.analizeGeneral("https://www.depo.gal/listado-concellos")
        for c in self.urls:
            self.analizeConcello(c)
        
        for c in self.concellos:
            c.write()
    
    def imprimir(self):
        print ("Soy AnalizerDepo")


## aqúi el main

a = AnalizerDepoConcellos()
#a.analizeConcello("https://www.depo.gal/web/edepo/-/concellos-guarda")
a.run()