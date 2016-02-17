# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 10:33:24 2016

@author: Emerson Martins
"""

import formulas

from random import uniform
from time import sleep

percurso = 17500.0
bateria = range(101)
bateria.reverse()
latitude = 52.014897
longitude = 4.692556
dlong = 0.002618
dados = []

for i in bateria:
    dados.append([i, latitude, longitude])
    longitude += dlong

for i in range(100):
    run = formulas.calcula(dados[i+1][0], dados[i+1][1], dados[i+1][2],
                           dados[i][1], dados[i][2], uniform(25.0, 30.0),
                           percurso)
    print "bateria: "+`dados[i][0]`+" %"
    print "percurso restante: "+`percurso`+" m"
    print "rotacao do motor: "+`run[1]`+" Hz"
    print "tensao no motor: "+`run[2]`+" V"
    print "tempo de autonomia: "+`run[3]`+" s"
    print "velocidade: "+`run[6]`+" nos"
    print "velocidade calculada: "+`run[5]`+" nos"
    print "corrente calculada: "+`run[0]`+" A"
    print "balanco: "+`run[8]`+" J"
    print ""
    percurso -= run[7]

    sleep(10)
