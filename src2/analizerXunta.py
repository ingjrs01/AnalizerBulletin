#!/usr/bin/python3
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from noticiasm import Noticia
from analizer import Analizer

import re
import time

class AnalizerXunta(Analizer): 

    def __init__(self,numero):
        Analizer.__init__(self)
        self.__days = numero
   
    def analize(self,url):
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
            mes = self.meses.index(temp[len(temp)-3]) + 1
            dia = int(temp[len(temp)-5])
            fecha = date(year,mes,dia)

            if  (self.checkNumber(year, numero,"DOGA") == True):
                return True
            self.beginAnalysis(fecha)
            self.setAnalysisState("DOGA",fecha,"INICIADO")
            sections = res.findAll("div",{"id":re.compile('secciones*')})
            for section in sections:
                lines = section.findAll("li")
                for line in lines:
                    if (line.a is not None):
                        noticia = Noticia()
                        noticia.bulletin = "DOGA"
                        noticia.bulletin_year = year
                        noticia.bulletin_no = numero
                        noticia.bulletin_date = fecha
                        noticia.seccion   = ""
                        noticia.organismo = line.findPrevious('p',{'class':'dog-toc-organismo'}).getText()
                        noticia.organo    = ""  #li.span.getText()
                        noticia.servicio  = ""        
                        noticia.newname = line.a.getText()
                        noticia.url = "https://www.xunta.gal" + line.a['href'] 
                        self.normalizar(noticia)
                        pseccion =  line.findPrevious('p',{'class':'dog-toc-nivel-2'})
                        if (pseccion is not None):                                
                            if (pseccion.getText() == 'c) Outros anuncios'):
                                noticia.seccion = 'SECCIÓN NON OFICIAL'
                        if (self.isNotificable(noticia.newname)):
                            noticia.notify = 1
                        noticia.fav = 0
                        noticia.readed = 0
                        noticia.created_at = datetime.now()
                        noticia.updated_at = datetime.now()
                        noticia.imprimir()
                        noticia.save()
            self.setAnalysisState("DOGA",fecha,"FINALIZADO")

    def normalizar(self,noticia): 
        if "Xulgado" in noticia.organismo:
            noticia.seccion = 'ADMINISTRACIÓN DE XUSTIZA'
            noticia.organismo = noticia.organismo.upper()

        if "Concello" in noticia.organismo:
            noticia.seccion = 'ADMINISTRACIÓN LOCAL'
            noticia.organismo = noticia.organismo.upper()

        if "Deputación" in noticia.organismo:             
            noticia.seccion = 'ADMINISTRACIÓN LOCAL'
            noticia.organismo = noticia.organismo.upper()

        if "Consellería" in noticia.organismo:
            noticia.seccion = 'ADMINISTRACIÓN AUTONÓMICA'
            noticia.organo = noticia.organismo.upper()
            noticia.organismo = 'XUNTA DE GALICIA'

        if "Universidade" in noticia.organismo: 
            noticia.seccion = "UNIVERSIDADES"
            noticia.organismo = noticia.organismo.upper()

        if "Augas de Galicia" in noticia.organismo: 
            noticia.seccion = 'ADMINISTRACIÓN AUTONÓMICA'
            noticia.organismo = 'XUNTA DE GALICIA'
            noticia.organo = 'CONSELLERÍA DE INFRAESTRUTURAS E MOBILIDADE'
            noticia.servicio = 'AUGAS DE GALICIA'

        if "Axencia Galega de Infraestruturas" in noticia.organismo: 
            noticia.seccion = 'ADMINISTRACIÓN AUTONÓMICA'
            noticia.organismo = 'XUNTA DE GALICIA'
            noticia.organo = 'CONSELLERÍA DE INFRAESTRUTURAS E MOBILIDADE'
            noticia.servicio = 'AXENCIA GALEGA DE INFRAESTRUCTURAS'

        if "Escola Galega de Administración Pública" in noticia.organismo:
            noticia.seccion = 'ADMINISTRACIÓN AUTONÓMICA'
            noticia.organismo = 'XUNTA DE GALICIA'
            noticia.organo = 'VICEPRESIDENCIA E CONSELLERÍA DE PRESIDENCIA, ADMINISTRACIÓNS PÚBLICAS E XUSTIZA'
            noticia.servicio = "ESCOLA GALEGA DE ADMINISTRACIÓN PÚBLICA"

        if 'Fondo Galego de Garantía Agraria' in noticia.organismo:
            noticia.seccion = 'ADMINISTRACIÓN AUTONÓMICA'
            noticia.organismo = 'XUNTA DE GALICIA'
            noticia.organo = 'CONSELLERÍA DO MEDIO RURAL'
            noticia.servicio = 'FONDO GALEGO DE GARANTÍA AGRARIA'

        if 'Servizo Galego de Saúde' in noticia.organismo: 
            noticia.seccion = 'ADMINISTRACIÓN AUTONÓMICA'
            noticia.organismo = 'XUNTA DE GALICIA'
            noticia.organo = 'CONSELLERÍA DE SANIDADE'
            noticia.servicio = 'SERVIZO GALEGO DE SAÚDE'

        if 'Axencia Turismo de Galicia' in noticia.organismo: 
            noticia.seccion = 'ADMINISTRACIÓN AUTONÓMICA'
            noticia.organismo = 'XUNTA DE GALICIA'
            noticia.organo = 'CONSELLERÍA DE CULTURA E TURISMO'
            noticia.servicio = 'AXENCIA TURISMO DE GALICIA'

        if 'Servizo de Emprego e Economía Social' in noticia.organismo: 
            noticia.seccion = 'ADMINISTRACIÓN AUTONÓMICA'
            noticia.organismo = 'XUNTA DE GALICIA'
            noticia.organo = 'CONSELLERÍA DE ECONOMÍA, EMPREGO E INDUSTRIA'
            noticia.servicio = 'SERVIZO DE EMPREGO E ECONOMÍA SOCIAL'

        if 'Axencia de Protección da Legalidade Urbanística' in noticia.organismo: 
            noticia.seccion = 'ADMINISTRACIÓN AUTONÓMICA'
            noticia.organismo = 'XUNTA DE GALICIA'
            noticia.organo = 'CONSELLERÍA DE  MEDIO AMBIENTE, TERRITORIO E VIVENDA'
            noticia.servicio = 'AXENCIA DE PROTECCIÓN DA LEGALIDADE URBANÍSTICA'

        if 'Portos de Galicia' in noticia.organismo:
            noticia.seccion = 'ADMINISTRACIÓN AUTONÓMICA'
            noticia.organismo = 'XUNTA DE GALICIA'
            noticia.organo = 'CONSELLERÍA DO MAR'
            noticia.servicio = 'PORTOS DE GALICIA'

        if 'Axencia Galega de Innovación' in noticia.organismo: 
            noticia.seccion = 'ADMINISTRACIÓN AUTONÓMICA'
            noticia.organismo = 'XUNTA DE GALICIA'
            noticia.organo = 'CONSELLERÍA DE ECONOMÍA, EMPREGO E INDUSTRIA'
            noticia.servicio = 'AXENCIA GALEGA DE INNOVACIÓN'

        if 'Instituto Galego de Promoción Económica' in noticia.organismo: 
            noticia.seccion = 'ADMINISTRACIÓN AUTONÓMICA'
            noticia.organismo = 'XUNTA DE GALICIA'
            noticia.organo = 'CONSELLERÍA DE ECONOMÍA, EMPREGO E INDUSTRIA'
            noticia.servicio = 'INSTITUTO GALEGO DE PROMOCIÓN ECONÓMICA'

        if 'Instituto Galego da Vivenda e Solo' in noticia.organismo:
            noticia.seccion = 'ADMINISTRACIÓN AUTONÓMICA'
            noticia.organismo = 'XUNTA DE GALICIA'
            noticia.organo = 'CONSELLERÍA DE INFRAESTRUCTURAS E VIVENDA'
            noticia.servicio = 'INSTITUTO GALEGO DA VIVENDA E SOLO'


        return True
        
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
        #self.registerListener()
        l2 = self.urlGeneratorXunta()
        for item in l2:
            self.analize(item)
            print ("Esperando")
            time.sleep(5)
            print("Reanudando")

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
                    if (li.a['href'].find("#") < 0):
                        urls_in.append("https://www.xunta.gal/diario-oficial-galicia/" + li.a['href'])
        return urls_in

    def imprimir(self):
        print ("Soy AnalizerXunta")
