from analizer import Analizer
from AnalizerModel import AnalizerModel
from datetime import date, datetime

import sys


def extract_date(date_str):
    f = date_str.split("/")
    dia = int(f[0])
    mes = int(f[1])
    ano = int(f[2])

    fecha = date(ano,mes,dia)
    return fecha


print ("Arrancando el nuevo analizador")

num_days = 1
#analysis_date = ''
if (len(sys.argv) > 1):
    if (sys.argv[1] == "-d"):
        analysis_date = extract_date(sys.argv[2])
else:
    analysis_date = datetime.now()

#https://boppo.depo.gal/detalle/-/boppo/2020/05/20
#https://boppo.depo.gal/detalle/-/boppo/2020/09/16
#print("Fecha a analizar")
#print(analysis_date.month)
#exit(0)

print("Inicializando analizador general:")
p = Analizer()
print("Analizador general inicializado")

analizerm = AnalizerModel()
analizers = analizerm.getActive()
for a in analizers:
    module = __import__(a.module)
    class_ = getattr(module, a.classname)
    instance = class_(analysis_date)
    #instance.imprimir()
    p.addAnalizer(instance)

p.work()
print ("End.")
