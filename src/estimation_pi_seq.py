#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 3 8:19:03 2022

@author: audrey.nicolle & emma.begard
"""
#Import-----------------------------------------------------------------------------
import random, time

#Fonction--------------------------------------------------------------------------
"""
@brief : cette foction permet de calculer le nbr de hits dans un cercle unitaire.

@param :
        nb_iterations : nombre d'iterations de calculs de hits (int)

@return :
        count : nombre de hit, point dans le cercle unité (int)
"""
def frequence_de_hits_pour_n_essais(nb_iteration):
    
    count = 0
    
    for i in range(nb_iteration):
        x = random.random()
        y = random.random()
        
        # si le point est dans l’unit circle
        if x * x + y * y <= 1: count += 1

    return count

#Main-------------------------------------------------------------------------------
# Nombre d’essai pour l’estimation
nb_total_iteration = 10000000

#gestion temps, appel fonction
time_set = time.time()
nb_hits = frequence_de_hits_pour_n_essais(nb_total_iteration)
time_end = time.time()
time_exec = time_end - time_set

#Affihage
print("Valeur estimée Pi par la méthode Mono−Processus : ", round(4 * nb_hits / nb_total_iteration,5))
print("Temps : " + str(round(time_exec,5)))
#TRACE :
# Calcul Mono−Processus : Valeur estimée Pi par la méthode Mono−Processus : 3.1412604