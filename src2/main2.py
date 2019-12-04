from analizerXunta import AnalizerXunta
from analizerDepo import AnalizerDepo
from analizerCoruna import AnalizerCoruna
from analizerDelu import AnalizerDelu
from analizerDeou import AnalizerDeou
from analizer import Analizer
from datetime import date, datetime, timedelta

import sys

print ("Herramienta de pruebas...")


p = Analizer()

fecha = date.today()
bulletin = "BOPPO"

#p.beginAnalysis(fecha)
p.setAnalysisState(bulletin,fecha,"INICIADO")

