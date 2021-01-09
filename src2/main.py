from analizer import Analizer
from AnalizerModel import AnalizerModel

import sys

print ("Working...")

num_days = 1
if (len(sys.argv) > 1):
    num_days = int(sys.argv[1])
p = Analizer()
analizerm = AnalizerModel()
analizers = analizerm.getActive()
for a in analizers:
    module = __import__(a.module)
    class_ = getattr(module, a.classname)
    instance = class_(num_days)
    #instance.imprimir()
    p.addAnalizer(instance)
p.work()
print ("End.")
