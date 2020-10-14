from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from noticiasm import Noticia
from analizer import Analizer
import time

class AnalizerBoe(Analizer): 

    def __init__(self,fecha):
        Analizer.__init__(self)
        self.meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'] 
        self.__date = fecha
        self.bulletin = "BOE"
        self.urls = [] # Aquí vamos metiendo las urls que hay que analizar en las diferentes pasadas. 
        self.urls_visited = []

    def analize(self,url):
        try: 
            html = urlopen(url)
        except HTTPError as e:
            print(e)
        except URLError as u:
            print("Servidor BOE no encontrado " + url)
            print(u)
        else:
            print ("Iniciando Análisis del BOE...")
            print(url)
            content = html.read().decode('utf-8', 'ignore')
            res = BeautifulSoup(content,"html.parser") 

            cabecera = res.find('div',{'class':"tituloSumario"})
            print(cabecera)
            partes = cabecera.getText().split()
            dia = int(partes [5])
            mes = self.meses.index(partes[7]) + 1
            ano = int(partes[9][:-1])
            numero = partes[11]
            fecha = date(ano,mes,dia)

                #<div class="solapasMultiplesBOES"><ul>
                #    <li class="current"><abbr title="Número">Núm.</abbr> 89</li>
                #    <li><a href="index.php?d=88"><abbr title="Número">Núm.</abbr> 88</a></li>
                #    </ul>
                #</div>
            multiple = res.find('div',{'class':'solapasMultiplesBOES'})
            if multiple is not None:
                print("Encontrado día múltiple")
                numero = int(multiple.find('li',{'class':'current'}).getText().split(" ")[1])
                ano = int(partes[9])

                if "/index.php?d=" not in url:
                    otros = multiple.findAll("li",{'class': None})
                    for o in otros:
                        newurl = url + o.a['href']
                        print(newurl)
                        if newurl not in self.urls_visited:
                            self.urls.append(newurl)

            fecha = date(ano,mes,dia)

            # Comprobamos si ya existe
            #if (self.checkBulletinExists(self.bulletin,fecha) == True):
            if (self.checkNumber(ano,numero,"BOE") == True):
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
        print("Generando urls")
        urls = []
        tempdate = self.__date
        url = "https://www.boe.es/boe/dias/" + str(tempdate.year) + "/" + format(tempdate.month, '02') + "/" + format(tempdate.day, '02')
        print ("Url: " + url)
        urls.append(url)

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
    
    def execute(self,url):
        self.urls.append(url)
        while len(self.urls) > 0:
            u = self.urls.pop()
            self.analize(u)
    
    def imprimir(self):
        print ("Soy AnalizerBoe")


a = AnalizerBoe(1)
a.execute("https://www.boe.es/boe/dias/2020/03/27/")