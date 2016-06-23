# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 10:33:24 2016

@author: Emerson Martins
"""

from math import pi, sqrt, sin, cos, asin


def calcula(porcentagem_de_bateria,
            latitude1, longitude1,
            latitude2, longitude2,
            intervalo_de_tempo, distancia_a_percorrer):
    """
    Retorna a ultima corrente calculada para que o
    balanco de energia nao seja negativo.

    Unidades
    ========

    Velocidade        nos
    Tensao            Volt
    Corrente          Ampere
    Diametro          metro
    Distancia         metro
    Densidade         kg/m^3
    Energia           Joule
    Rotacao           Hertz
    Torque            N.m
    Potencia          Watt
    Tempo             segundo

    """
    diametro_do_helice = 0.23
    densidade_da_agua = 1000.0
    corrente_calculada = None
    energia_gasta = -1.0         # valor inicial padrao
    energia_remanescente = -1.0  # valor inicial padrao
    balanco_de_energia = energia_gasta + energia_remanescente
    
    # calculo da velocidade
    latitude1 = (latitude1*pi)/180.0
    longitude1 = (longitude1*pi)/180.0
    latitude2 = (latitude2*pi)/180.0
    longitude2 = (longitude2*pi)/180.0
    diferenca_latitude = latitude2 + (-1*latitude1)
    diferenca_longitude = longitude2 + (-1*longitude1)
    a = (sin(diferenca_latitude/2.0)**2 +
        cos(latitude1)*cos(latitude2)*sin(diferenca_longitude/2.0)**2)
    c = 2*asin(sqrt(a))
    distancia = 6378140.0*c

    velocidade = (distancia/intervalo_de_tempo)/0.51444
    V_estipulada = 0.1

    # loop que varia a velocidade estipulada ate convergir
    while balanco_de_energia < 0.0 or balanco_de_energia > 99.99:
        rotacao_do_motor = ((-((-1.78263*(10**-1))*(V_estipulada/
            diametro_do_helice)) + sqrt(((-1.78263*(10**-1))*(V_estipulada/
            diametro_do_helice))**2 - 4*(3.29365*(10**-1))*((-7.83463*
            (10**-2)) - (V_estipulada/(densidade_da_agua*
            diametro_do_helice**4)))))/(2*3.29365*(10**-1)))
        coeficiente_de_avanco = (V_estipulada/
            (rotacao_do_motor*diametro_do_helice))
        coeficiente_de_torque = ((-1.07624*(10**-1)*coeficiente_de_avanco**2-
            1.93858*(10**-1)*coeficiente_de_avanco + 4.28652*(10**-1))/10.0)
        torque = (coeficiente_de_torque*densidade_da_agua*rotacao_do_motor**2*
            diametro_do_helice**5)
        tensao_no_motor = (rotacao_do_motor*60)/50.0
        corrente_calculada = (torque - 0.41)/0.194
        potencia_requerida = corrente_calculada*tensao_no_motor
        tempo_de_autonomia = distancia_a_percorrer/(V_estipulada*0.51444)
        energia_gasta = potencia_requerida*tempo_de_autonomia
        energia_remanescente = (1520.0)*3600.0*(porcentagem_de_bateria/100.0)
        balanco_de_energia = energia_gasta + energia_remanescente
        velocidade_calculada = V_estipulada
        if balanco_de_energia > 0.0:
            V_estipulada += 0.1
        if balanco_de_energia < 0.0:
            V_estipulada -= 0.00001

    return (corrente_calculada,
            rotacao_do_motor,
            tensao_no_motor,
            tempo_de_autonomia,
            balanco_de_energia,
            velocidade_calculada,
            velocidade,
            distancia)


# print calcula(99.0, 52.014897, 4.692556, 52.014791, 4.689938, 30.0, 17750.0)
