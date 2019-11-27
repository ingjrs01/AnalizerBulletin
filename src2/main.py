from analizerXunta import AnalizerXunta
from analizerDepo import AnalizerDepo
from analizerCoruna import AnalizerCoruna
from analizerDelu import AnalizerDelu
from analizerDeou import AnalizerDeou
from analizer import Analizer

import sys

print ("Comenzamos a trabajar")

num_days = 1
if (len(sys.argv) > 1):
    print ("Cuantos dias analizar: " + sys.argv[1])
    num_days = int(sys.argv[1])

p = Analizer()

#a1 = AnalizerXunta(num_days)
a2 = AnalizerDepo(num_days)
#a3 = AnalizerCoruna(num_days)
#a4 = AnalizerDelu(num_days)
#a5 = AnalizerDeou(num_days)

#p.addAnalizer(a1)
p.addAnalizer(a2)
#p.addAnalizer(a3)
#p.addAnalizer(a4)
#p.addAnalizer(a5)

p.work()

