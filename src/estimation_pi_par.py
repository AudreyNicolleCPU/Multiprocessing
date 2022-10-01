#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 3 9:25:03 2022

@author: audrey.nicolle & emma.begard
"""

#Import-----------------------------------------------------------------------------
import random, time
import multiprocessing as mp

#Fonction--------------------------------------------------------------------------
"""
@brief : cette foction permet de calculer le nbr de hits dans un cercle unitaire et 
        de parteger son compte avec les autres processus.

@param :
        nb_iterations : nombre d'iterations de calculs de hits (int)
        sem : semaphore de 1 jeton (class multiprocessing)

@return :
        count : nombre de hit, point dans le cercle unité (int)
"""
def frequence_de_hits_pour_n_essais(nb_iteration, sem):
    count = 0
    for i in range(int(nb_iteration)):
        x = random.random()
        y = random.random()
        
        # si le point est dans l’unit circle
        if x * x + y * y <= 1: count += 1
        
    sem.acquire()
    share.value += count/nb_iteration
    sem.release()
    
#Main------------------------------------------------------------------------------
# Nombre d’essai pour l’estimation
nb_total_iteration = 10000000
share = mp.Value('f',0.0)
sem = mp.Semaphore(1)

#creation des processus
proc_1 = mp.Process(target = frequence_de_hits_pour_n_essais,args = (nb_total_iteration/4,sem))
proc_2 = mp.Process(target = frequence_de_hits_pour_n_essais,args = (nb_total_iteration/4,sem))
proc_3= mp.Process(target = frequence_de_hits_pour_n_essais,args = (nb_total_iteration/4,sem))
proc_4 = mp.Process(target = frequence_de_hits_pour_n_essais,args = (nb_total_iteration/4,sem))

#gestion temps, démarrage processus
time_set = time.time()
proc_1.start();proc_2.start();proc_3.start();proc_4.start()
proc_1.join();proc_2.join();proc_3.join();proc_4.join()
time_end = time.time()
time_exec = time_end - time_set

#Affichage
print("Valeur estimée Pi par la méthode Multi−Processus 1 : ", round(share.value,5))
print("Temps : " + str(round(time_exec,5)))
#TRACE :
# Calcul Mono−Processus : Valeur estimée Pi par la méthode Mono−Processus : 3.1412604