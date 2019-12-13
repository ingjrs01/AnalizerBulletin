from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from noticiasm import Noticia
from analizer import Analizer
import time

class AnalizerBoe(Analizer): 

    def __init__(self,numero):
        Analizer.__init__(self)
        self.meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'] 
        self.__days = numero
        self.bulletin = "BOE"

    def analize(self,url):
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

            cabecera = res.find('div',{'class':"tituloSumario"})
            partes = cabecera.getText().split()
            dia = int(partes [5])
            mes = self.meses.index(partes[7]) + 1
            ano = int(partes[9][:-1])
            numero = partes[11]
            fecha = date(ano,mes,dia)

            # Comprobamos si ya existe
            if  (self.checkBulletinExists(self.bulletin,fecha) == True):
                print ("Ya he encontrado datos")
                return True
                
            self.beginAnalysis(fecha)
            self.setAnalysisState(self.bulletin,fecha,"INICIADO")
            
            noticias = res.findAll("li",{"class":"dispo"})

            i = 1
            for n in noticias: 
                print ("Noticia número: " + str(i))
                noticia = Noticia()
                noticia.bulletin = self.bulletin
                noticia.bulletin_year = ano
                noticia.bulletin_no = numero
                noticia.bulletin_date = fecha
                noticia.created_at = datetime.now()
                noticia.updated_at = datetime.now()
                noticia.newname = n.p.getText()
                noticia.seccion = ""
                if (self.isNotificable(noticia.newname)):
                    noticia.notify = 1
                noticia.url = "https://www.boe.es" + n.div.ul.li.a['href']

                # Encontrar los antecesores: 
                h3 = n.findPrevious('h3')
                if (h3 is not None):
                    noticia.seccion = h3.getText()

                h4 = n.findPrevious('h4')
                if (h4 is not None):
                    noticia.organismo = h4.getText()

                h5 = n.findPrevious('h5')
                if (h5 is not None):
                    h4b = h5.findPrevious('h4')
                    if (h4b.getText() == h4.getText()):
                        noticia.organo = h5.getText()
                
                # self.normalizar(noticia)
                noticia.imprimir()
                noticia.save()

                i += 1

            self.setAnalysisState(self.bulletin,fecha,"FINALIZADO")

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
        urls = []
        tempdate = datetime.now()
        for i in range(1,self.__days+1):
            if (tempdate.weekday() not in [5,6]): 
                url = "https://www.boe.es/boe/dias/" + str(tempdate.year) + "/" + format(tempdate.month, '02') + "/" + format(tempdate.day, '02')
                urls.append(url)
            tempdate = tempdate - timedelta(days=1)

        return urls

    def run(self): 
        l = self.urlGenerator()
        print ("Dentro de run")
        print (l)
        for item in l:
            print (item)
            self.analize(item)
            print ("Esperando")
            time.sleep(5)
            print("Reanudando")

        self.getData()
    
    def imprimir(self):
        print ("Soy AnalizerBoe")
