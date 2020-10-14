from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from noticiasm import Noticia
from analizer import Analizer
import time

#import re

class AnalizerDepo(Analizer): 

    def __init__(self,f):
        Analizer.__init__(self)
        self.__date = f

    def analize(self,url):
        try: 
            print("Dentro de analize")
            print (url);
            html = urlopen(url)
        except HTTPError as e:
            print(e)
        except URLError as u:
            print("Servidor depo no encontrado " + url)
            print(u)
        else:
            content = html.read().decode('utf-8', 'ignore')
            res = BeautifulSoup(content,"html.parser")
            strnumero = res.find("h2",{"class":"numero"})
            
            if (strnumero is None):
                print ("No existe boletín para este día")
                return False

            numero = int(strnumero.getText().split()[2])            
            info = res.find("span",{"class":"fecha"}).getText().split()
            year = int(info[len(info)-4])
            mes = self.meses.index(info[len(info)-6]) + 1 # El array comienza en 0
            dia = int(info[len(info)-8])
            fecha = date(year, mes, dia)

            if (self.checkNumber(year,numero,"BOPPO")):
                return True

            self.beginAnalysis(fecha)
            self.setAnalysisState("BOPPO",fecha,"INICIADO")

            grupo = res.findAll("ul",{"class":"listadoSumario"})

            for tag in grupo:
                organismo = tag.findPrevious('p',{"class":"Org"}).getText()
                seccion = tag.findPrevious('h4',{"class":"tit"}).getText()
                tmp = tag.fetchPreviousSiblings()[0]
                
                # Busco los elementos anteriores                    
                lis = tag.findAll("li")
                for li in lis:
                    noticia = Noticia()
                    noticia.bulletin = "BOPPO"
                    noticia.bulletin_year = year
                    noticia.bulletin_no = numero
                    noticia.bulletin_date = fecha
                    noticia.created_at = datetime.now()
                    noticia.updated_at = datetime.now()
                    noticia.seccion   = seccion
                    noticia.organismo = organismo
                    noticia.organo    = li.span.getText()
                    noticia.servicio  = ""        
                    noticia.organization = li.span.getText()
                    noticia.newname = li.p.getText()
                    
                    if (tmp.get("class")[0] == "inst"):
                        noticia.organo = tmp.getText()

                    if (self.isNotificable(noticia.newname)):
                        noticia.notify = 1

                    noticia.url = "https://boppo.depo.gal" + li.a['href']
                    self.normalizar(noticia)
                    noticia.imprimir()
                    noticia.save()
            # LLegados aquí, ha finalizado el análisis
            self.setAnalysisState("BOPPO",fecha,"FINALIZADO")

    def normalizar(self,noticia):
        if (noticia.seccion == "XUNTA DE GALICIA"):
            noticia.servicio = noticia.organo
            noticia.organo = noticia.organismo
            noticia.organismo = "XUNTA DE GALICIA"
            noticia.seccion = "ADMINISTRACIÓN AUTONÓMICA"
        if (noticia.organo == "DEPUTACIÓN PROVINCIAL"):
            noticia.organismo = "DEPUTACIÓN DE PONTEVEDRA"
            noticia.organo = ""
            noticia.servicio = ""

        if  "Municipal" in noticia.organismo:
            print ("Encontrado municipio")
            noticia.organismo = noticia.organo
            noticia.organo = ""  
            noticia.servicio = ""

        if (noticia.seccion == "SECCIÓN NON OFICIAL"):
            noticia.organismo = noticia.organo
            noticia.organo = ""
            noticia.servicio = ""
        
    def urlGenerator(self): 
        #urls = ["https://boppo.depo.gal/web/boppo"]
        urls = []
        #hoy = datetime.now()
        tempdate = self.__date
        url = "https://boppo.depo.gal/detalle/-/boppo/" + str(tempdate.year) + "/" + format(tempdate.month, '02') + "/" + format(tempdate.day, '02')
        urls.append(url)

        return urls

    def run(self): 
        print("Me mandan trabajar")
        l = self.urlGenerator()
        for item in l:
            self.analize(item)
            print ("Esperando")
            time.sleep(5)
            print("Reanudando")

        self.getData()
    
    def imprimir(self):
        print ("Soy AnalizerDepo")
