from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from noticiasm import Noticia
from analizer import Analizer
import time

class AnalizerCoruna(Analizer): 

    def __init__(self,numero):
        Analizer.__init__(self)
        self.__days = numero
        self.bulletin = "BOPCO"
        self.meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'] 

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

            s_info = res.find("div",{"id":"infoBoletin"})
            if (s_info is None):
                print ("No se ha encontrado boletín")
                return False

            info = s_info.find("a").getText()
            cachos = info.split()
            numero = int(cachos[4])
            dia = int(cachos[7])
            mes = self.meses.index(cachos[9]) + 1
            ano = int(cachos[11])
            fecha = date(ano,mes,dia)

            if (self.checkNumber(ano,numero,self.bulletin)):
                return True # Ya existen. 
                
            self.beginAnalysis(fecha)
            self.setAnalysisState(self.bulletin,fecha,"INICIADO")

            anuncios = res.findAll("div",{"class":"bloqueAnuncio"})
            for anuncio in anuncios: 
                noticia = Noticia()
                noticia.bulletin = self.bulletin
                noticia.bulletin_year = ano
                noticia.bulletin_no = numero
                noticia.bulletin_date = fecha                
                
                if (anuncio.find("h2")):
                    noticia.organismo = anuncio.find("h2").getText()
                    noticia.organo = anuncio.find("h3").getText()
                    servi = anuncio.find("h4")
                    if (servi is not None):
                        noticia.servicio = anuncio.find("h4").getText()
                else:
                    tmp = anuncio.find("h3")
                    if (tmp is not None): 
                        noticia.organismo = anuncio.find("h3").getText()
                    else:
                        noticia.organismo = "OTROS"

                    if (anuncio.find("h4")):
                        noticia.organo = anuncio.find("h4").getText()

                    noticia.servicio = ""
                noticia.seccion = anuncio.findPrevious('h1',{"class":"administracion"}).getText()
                
                resumen = anuncio.find("p",{"class":"resumenSumario"})
                noticia.url = "https://bop.dacoruna.gal/bopportal/publicado/" + str(ano) + "/" + str(mes) + "/" + str(dia) + "/" + resumen.select("a")[0]['href']
                noticia.newname = resumen.select("a")[0].getText().strip() + " - " + resumen.select("a")[1].getText().strip()
                # la notificación hay que comprobarla
                if (self.isNotificable(noticia.newname)):
                    noticia.notify = 1
                noticia.fav = 0
                noticia.readed = 0
                noticia.created_at = datetime.now()
                noticia.updated_at = datetime.now()
                noticia.imprimir()
                noticia.save()
            self.setAnalysisState("BOPCO",fecha,"FINALIZADO")


    def urlGenerator(self): 
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
        lista = self.urlGenerator()
        for item in lista:
            self.analize(item)
            print ("Esperando")
            time.sleep(5)
            print("Reanudando")

        self.getData()

    def imprimir(self):
        print ("Soy AnalizerCoruña")
