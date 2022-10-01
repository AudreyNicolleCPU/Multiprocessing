#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 3 10:32:03 2022

@author: audrey.nicolle & emma.begard
"""
#Import----------------------------------------------------------------------------------------
import multiprocessing as mp
import sys,os,time,signal

#Fonction--------------------------------------------------------------------------------------
"""
@brief : Cette fonction arrête le processus en cours en affcihant son Pid.

@Param : 
        sig/frame = parametre l'utilisation des signaux
        
@Ret : none
"""
def arret(sig,frame) :
    print("Arret programme : ", os.getpid())
    sys.exit(0)
 
    
"""
@brief : Cette fonction permet au processus de damnder le nombre de bille dont
        il a besoin si celle-ci sont disponible. Sinon il se met en attente. Le
        nombre de billes disponibles est mis à jour.

@Param : 
        k_voulu = nombre de billes voulus (int)
        sem = semaphore à 1 jeton (class multiprocessing)
        
@Ret : none
"""
def demander(k_voulu,sem) :
    print("Je suis " + str(os.getpid()) + " et je demande ", k_voulu)
    while k_voulu > nb_k_dispo.value :
        print("Je suis " + str(os.getpid()) + " et j'attends pour ", k_voulu)
        sem.acquire()
    print("Je suis " + str(os.getpid()) + " et j'ai pris", k_voulu)
    nb_k_dispo.value -= k_voulu


"""
@brief : Cette fonction permet au processus courant de récupérer ces billes
        et met à jour le nombres de billes disponibles.

@Param : 
        k_rendu = nombre de billes récupérées
        sem = semaphore à 1 jeton (class multiprocessing)
        
@Ret : none
"""    
def rendre(k_rendu,sem) :
    print("Je suis " + str(os.getpid()) + " et je rends ", k_rendu)
    sem.release()
    nb_k_dispo.value += k_rendu
    

"""
@brief : Cette fonction permet des gérer les actions du processeur qui travailent, soit demander
        "travailler", rendre.

@Param : 
        k_billes : nombre de billes voulus et reprises (int)
        sem = semaphore à 1 jeton (class mutliprocessing)
        
@Ret : none
"""   
def travailleur(k_billes,sem,j) :
    lst_proc[j] = os.getpid()
    signal.signal(signal.SIGUSR1,arret)
    for i in range(3) :
        print("Je suis " + str(os.getpid()) + " et c'est le tour ", i)
        demander(k_billes,sem)
        time.sleep(2)
        print("Je suis " + str(os.getpid()) + " et je joue aux billes.")
        rendre(k_billes,sem)


"""
@brief : Cette fonction permet de vérfier que les processus trvaillent correctement. 
        Si le nombre de de billes dépasse le nombre maximal, cette fonction envoie un
        signal pour arrêter tous les processus.

@Param : 
        k_max : nombre maximale de billes en jeu (int)
        
@Ret : none
"""     
def surveillant(k_max) :
    while check_end.value == "0" :
        if nb_k_dispo.value > k_max :
            print("ALERTE ROUGE !!!!!!!!")
            for i in range(4) :
                os.kill(lst_proc[i],signal.SIGUSR1)
    
    sys.exit(0)

#Main ------------------------------------------------------------------------------------------
#Generation des variables
nb_k_dispo = mp.Value('i',9) #nombre de billes disponibles
lst_proc = mp.Array('i',4) #liste des processus
check_end = mp.Value('i',0) #variable pour vérifier si les processus ont fini de travailler
sem_trav = mp.Semaphore(1) #semaphore à 1 jeton
k_max = 9 #nombre maximal de billes

#Creation processus
lst_proc[0] = os.getpid()
proc_1 = mp.Process(target= travailleur, args = (5,sem_trav,1))
proc_2 = mp.Process(target= travailleur, args = (2,sem_trav,2))
proc_3 = mp.Process(target= travailleur, args = (4,sem_trav,3))
proc_surv = mp.Process(target= surveillant, args = (k_max,))

#Gestion processus
proc_1.start();proc_2.start();proc_3.start(); proc_surv.start()
proc_1.join();proc_2.join();proc_3.join()
check_end.value = 1

sys.exit(0)            