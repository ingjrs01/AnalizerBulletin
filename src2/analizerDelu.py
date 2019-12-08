from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from noticiasm import Noticia
from analizer import Analizer
import time

class AnalizerDelu(Analizer): 

    def __init__(self,numero):
        Analizer.__init__(self)
        self.__days = numero
        #self.__meses = ['xaneiro','febreiro','marzo','abril','maio','xuño','xullo','agosto','setembro','outubro','novembro','decembro'] 

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

            # Vamos a por el número: 
            grupo_codigo = res.find('div',{"class":"field--name-field-ail-codigo"})
            numero = int(grupo_codigo.find('div',{'class','field__item'}).getText())
            grupo_codigo = res.find('div',{'class','field--name-field-ail-bop-fecha-publicacion'})
            sfecha = grupo_codigo.find('div',{'class':'field__item'}).getText().split()
            dia = int(sfecha[1])
            mes = self.meses.index(sfecha[3].lower()) + 1 
            anio = int(sfecha[5])
            fecha = date(anio,mes,dia)

            if (self.checkNumber(anio,numero,"BOPLU")):
                return True
            self.beginAnalysis(fecha)
            self.setAnalysisState("BOPLU",fecha,"INICIADO")

            div = res.find("div",{"class":"field--name-field-ail-bop-contenido"})
            lista = div.find("ul")
            secciones = lista.children
            for seccion in secciones: 
                if hasattr(seccion, 'strong'):                    
                    seccion_nombre = seccion.strong.getText()

                if (not hasattr(seccion, 'children')):                    
                    continue                    
                lista = seccion.find("ul")
                if (lista is not None):
                    organismos = lista.findChildren("li",recursive=False)
                    for organismo in organismos: 
                        noticias = organismo.find("ul")
                        if ((organismo.strong is None) or (noticias is None)):
                            noticia = Noticia()
                            noticia.bulletin = "BOPLU"
                            noticia.bulletin_year = anio
                            noticia.bulletin_no = numero
                            noticia.bulletin_date = fecha
                            noticia.created_at = datetime.now()
                            noticia.updated_at = datetime.now()
                            noticia.seccion   = "OTROS"
                            noticia.organismo = seccion_nombre
                            noticia.organo    = ""
                            noticia.servicio  = ""        
                            noticia.organization = ""
                            if (organismo.a is not None):
                                noticia.newname = organismo.a.getText()
                                noticia.url = "http://deputacionlugo.gal" + organismo.a['href']
                            else:
                                print ("Ha habido una incidencia")
                                noticia.newname = "INCIDENCIA: "

                            if (self.isNotificable(noticia.newname)):
                                noticia.notify = 1
                            
                            self.normalizar(noticia)
                            noticia.imprimir()
                            noticia.save()
                        else: 
                            noticias = organismo.ul.findChildren("li")
                            for n in noticias:
                                noticia = Noticia()
                                noticia.bulletin = "BOPLU"
                                noticia.bulletin_year = anio
                                noticia.bulletin_no = numero
                                noticia.bulletin_date = fecha
                                noticia.created_at = datetime.now()
                                noticia.updated_at = datetime.now()
                                noticia.seccion   = seccion_nombre
                                noticia.organismo = organismo.strong.getText()
                                noticia.organo    = ""
                                noticia.servicio  = ""        
                                noticia.organization = ""
                                noticia.newname = n.a.getText()

                                if (self.isNotificable(noticia.newname)):
                                    noticia.notify = 1

                                noticia.url = "http://deputacionlugo.gal" + n.a['href']
                                self.normalizar(noticia)
                                noticia.imprimir()
                                noticia.save()
                else: 
                    print ("Lista vacía")
            self.setAnalysisState("BOPLU",fecha,"FINALIZADO")

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
    
    def urlGenerator(self):
        paginas = (self.__days // 10) + 1

        indices = []
        for i in range(0,paginas):
            url_indice = 'http://deputacionlugo.gal/gl/boletin-oficial-da-provincia-de-lugo/bop?fecha_publicacion%5Bmin%5D=&fecha_publicacion%5Bmax%5D=&field_ail_codigo_value=&field_ail_bop_contenido_value=&page=' + str(i)
            indices.append(url_indice)

        cont = 0
        urls = []
        # Vamos a buscar las direcciones: 
        for url in indices:
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

                tabla = res.find('table')
                lineas = tabla.tbody.findAll('tr')
                for linea in lineas:
                    cont += 1
                    if (cont > self.__days):
                        return urls

                    celdas = linea.findAll('td')
                    nodo = 'http://deputacionlugo.gal' + celdas[1].a['href']
                    urls.append(nodo)

    def run(self): 
        l2 = self.urlGenerator()
        for item in l2:
            self.analize(item)
            print ("Esperando")
            time.sleep(5)
            print("Reanudando")

        self.getData()        

    def imprimir(self):
        print ("Soy AnalizerLugo")
