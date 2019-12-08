from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from noticiasm import Noticia
from analizer import Analizer

import requests
import time

class AnalizerDeou(Analizer): 

    def __init__(self,numero):
        Analizer.__init__(self)
        self.__days = numero
        self.meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'] 

    def isNotificable(selft, new):
        words = ['OPOSICIÓN', 'SELECTIVOS', 'FUNCIONARIO','EMPREGO']
        for word in words:
            if (word in new):
                return True

        return False

    def analize(self):
        url = 'https://bop.depourense.es/portal/cambioBoletin.do'
        fechas = self.urlGenerator()
        #for f in fechas:
        #    print (url + "   ." + f + ".")

        for fecha in fechas: 
            post_params = {'fechaInput':fecha}
            response = requests.post(url, data=post_params)   
            res = BeautifulSoup(response.text, 'html.parser')    

            sumario = res.find("div",{"class":"resumenSumario"}).getText().split()
            numero = int(sumario[4])
            year = int(sumario[11])
            mes =  self.meses.index(sumario[9]) + 1 # El array comienza en 0
            dia = int(sumario[7])
            fecha = date(year, mes, dia)
            self.beginAnalysis(fecha)
            self.setAnalysisState("BOPOU",fecha,"INICIADO")
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
                    noticia.save()
            else:
                print ("Paso al siguiente")

            self.setAnalysisState("BOPOU",fecha,"FINALIZADO")
            print ("Esperando")
            time.sleep(5)
            print("Reanudando")


    def normalizar(self,noticia):
        if (noticia.seccion == "IV. ENTIDADES LOCAIS"):
            noticia.seccion = "ADMINISTRACIÓN LOCAL"

        if (noticia.seccion == "V. TRIBUNAIS E XULGADOS"):
            noticia.seccion = " ADMINISTRACIÓN DE XUSTIZA"
        
        if (noticia.seccion == "II. ADMINISTRACIÓN XERAL DO ESTADO"):
            noticia.seccion = "ADMINISTRACIÓN ESTATAL" 

        if (noticia.seccion == "III. COMUNIDADE AUTÓNOMA"):
            noticia.seccion = "ADMINISTRACIÓN AUTONÓMICA"
            noticia.organo = noticia.organismo
            noticia.organismo = "XUNTA DE GALICIA"
        
        if ("DEPUTACIÓN" in noticia.seccion): 
            noticia.seccion = "ADMINISTRACIÓN LOCAL"

        if ("-" in noticia.organismo): 
            noticia.organo = noticia.organismo [noticia.organismo.find('-')+1: ] 
            noticia.organismo = noticia.organismo [:noticia.organismo.find('-')] 
        
        if ("CONCELLO" in noticia.organismo):
            cosas = noticia.organismo.split()
            noticia.organismo = " ".join(cosas[2:])

    def urlGenerator(self): 
        fechas = []
        hoy = datetime.now()
        tempdate = hoy
        for i in range(0,self.__days):
            if (tempdate.weekday() not in [6]): # Publica los sábados
                sfecha = format(tempdate.day, '02') +  "/" + format(tempdate.month, '02') + "/" + str(tempdate.year)
                fechas.append(sfecha)
            tempdate = tempdate - timedelta(days=1)

        return fechas

    def run(self): 
        #self.registerListener()
        self.analize()
        self.getData()

    def imprimir(self):
        print ("Soy AnalizerOrense")

