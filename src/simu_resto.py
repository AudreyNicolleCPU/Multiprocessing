#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 08:01:43 2022

@author: audrey.nicolle & emma.begard
"""
#Import--------------------------------------------------------------------------------
import ctypes
import multiprocessing as mp
import sys,os,time
import curses as c
import random
from time import sleep
import signal

#Variables-----------------------------------------------------------------------------
CLEARSCR="\x1B[2J\x1B[;H"    #  Clear SCreen
#Fonction------------------------------------------------------------------------------
def effacer_ecran() : print(CLEARSCR,end='')
def erase_line_from_beg_to_curs() : print("\033[1K",end='')

def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end='')


def display(i,j,imprime) :
    move_to(i,j)
    print(imprime)
    
def efface_ligne(i,j) :
    move_to(i,j)
    erase_line_from_beg_to_curs()

"""
@brief : Cette fonction réalise les actions du major d'homme. Il permet d'afficher l'état des commandes 
        en cours et celle qui sont en attente.

@param : 
        tab_commandes : liste contenant 50 valeurs partagées de 20 bytes chacune (class RawArray, multiprocessing)
        sem : Semaphore de 1 jeton (class Semaphore, multiprocessing)
        num : numéro du serveur(int)
        val : valeur partagé pour signifier l'arrêt du process (class Value, multiprocessing)
        event : evenement qui permet de savoir si le majeur d'homme lit ou non (class Event, multtiprocessing)
    
@return : none
"""   
def major(tab_commandes,val,event) :
    
    # Clear screen
    effacer_ecran()
    count = 0
    while val.value == 0 :
        lst_com = []
        
            
        for com in tab_commandes :
                             
                if len(com.value) == 9 :  
                    if com.value[8] == "0" :
                        display (0,0,' Le cuistot 0 prepare un {} pour le client {} suivie par le serveur {}.'\
                        .format(com.value[4],com.value[0:3],com.value[6]))
                        
                    if com.value[8] == "1" :
                        display(2,0,' Le cuistot 1 prepare un {} pour le client {} suivie par le serveur {}.'\
                        .format(com.value[4],com.value[0:3],com.value[6]))
            
                    if com.value[8] == "2" :
                        display(4,0,' Le cuistot 2 prepare un {} pour le client {} suivie par le serveur {}.'\
                        .format(com.value[4],com.value[0:3],com.value[6]))
                        
                if len(com.value) == 10 : 
                    display(10,0,' Le serveur {} a servie le client {}.'\
                    .format(com.value[6],com.value[0:3]))
                    com.value ="v"
                    #print(com.value,file=sys.stderr)
                
                if len(com.value) == 5 :
                    count += 1
                    lst_com.append(("Client :" + com.value[0:3], "Commande :" + com.value[4]))
        
        #Affichage commande en attente et nombre
        efface_ligne(6,0)
        efface_ligne(8,0)
        if lst_com != []:
            display(6,0,' Les commandes clients en attente : {} .'.format(lst_com))
        display(8,0,' Nombres de commandes en attente: {} .'.format(count))
        count = 0
        
        #on permet aux autres process de travailler
        event.set()
                
#python3 simu_resto.py > out ou python3 simu_resto.py 2> out


"""
@brief : Cette fonction réalise les actions du serveur, soit récupérer les commandes des clients et les servir.

@param : 
        tab_commandes : liste contenant 50 valeurs partagées de 20 bytes chacune (class RawArray, multiprocessing)
        sem : Semaphore de 1 jeton (class Semaphore, multiprocessing)
        num : numéro du serveur(int)
        val : valeur partagé pour signifier l'arrêt du process (class Value, multiprocessing)
        event : evenement qui permet de savoir si le majeur d'homme lit ou non (class Event, multtiprocessing)
    
@return : none
"""   
def serveurs (tab_commandes,sem,num,val,event) :
    
    while val.value == 0 :
        
        #on attend l'autorisation du major d'homme
        event.wait()
        #on verifie d'être le seul à regarder le tabelau de valeurs partagées
        sem.acquire()
        
        #on cherche une commande adequate à recuperer (5) ou servir (9)
        j = 0
        while j < 49 and (not len(tab_commandes[j].value ) == 5  \
                or not len(tab_commandes[j].value ) == 9) :
                j += 1 

        #recuperation commande client, modification et donner au cuistot
        if len(tab_commandes[j].value ) == 5 :
            tab_commandes[j].value += "_" + str(num)
            print(("prise" + tab_commandes[j].value,num),file=sys.stderr)
            sleep(2) #temps de service
                
        #commande servie
        if len(tab_commandes[j].value ) == 9 :
            tab_commandes[j].value += "S"
            print(("servie" + tab_commandes[j].value, num),file=sys.stderr)
            sleep(2) #temps de service
        sem.release()
 

"""
@brief : Cette fonction réalise les actions des clients. On crée donc des commandes selon un certain temps 
        aléatoire et on les places dans le tableau de valeur partagée.

@param : 
        tab_commandes : liste contenant 50 valeurs partagées de 20 bytes chacune (class RawArray, multiprocessing)
        val : valeur partagé pour signifier l'arrêt du process (class Value, multiprocessing)
        sem : Semaphore de 1 jeton (class Semaphore, multiprocessing)
        event : evenement qui permet de savoir si le majeur d'homme lit ou non (class Event, multtiprocessing)
    
@return : none
"""      
def clients (tab_commandes,val,sem,event) :
    
    i = 0
    #menu du restaurant
    alphabet = ["A","B","C","D","E","F","G","H","I","J","K",\
            "L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    
    while val.value == 0 :
            
            #on attend l'autorisation du major d'homme
            event.wait()
            #on verifie d'être le seul à regarder le tabelau de valeurs partagées
            sem.acquire()
            
            #creation commande
            lettre = 25*random.random() #a+(b-a)*random() a = 0, b = 25, loi normale
            if len(str(i)) == 1:
                num_c = "00" + str(i)
            if len(str(i)) == 2:
                num_c = "0" + str(i)
            commande = num_c + "_" + alphabet[int(lettre)] 
            print(commande,file=sys.stderr )
            
            #On regarde quel place sont disponibles dans le tableau partagé
            j = 0
            while j < 49 and (not tab_commandes[j].value != "v" ):
                j += 1
            
            #on ajoute notre commande
            if tab_commandes[j].value == "v" :
                tab_commandes[j].value = commande
                print("in " + tab_commandes[j].value,file=sys.stderr )

            sem.release()
            
            #pause avant la prochaine commande
            sleep (random.random()*2.5)
            i += 1 #client suivant
 
"""
@brief : Cette fonction réalise les actions des cuisiniers Il récupère les commandes foruni par les serveurs, les prépare 
        et le rende aux serveurs via le tableau de valeur partagée.

@param : 
        tab_commandes : liste contenant 50 valeurs partagées de 20 bytes chacune (class RawArray, multiprocessing)
        sem : Semaphore de 1 jeton (class Semaphore, multiprocessing)
        num : numéro du cuistot (int)
        val : valeur partagé pour signifier l'arrêt du process (class Value, multiprocessing)
        event : evenement qui permet de savoir si le majeur d'homme lit ou non (class Event, multtiprocessing)
    
@return : none
"""         
def cuistots (tab_commandes,sem,num,val,event) :

    while val.value == 0 :
        #on attend l'autorisation du major d'homme
        event.wait()
        #on verifie d'être le seul à regarder le tabelau de valeurs partagées
        sem.acquire()
        
        #On regarde quel place sont disponibles dans le tableau partagé
        j = 0 
        while  j < 49 and(not len(tab_commandes[j].value) == 7):
            j += 1
        
        #recuperation commandes, modification, rendu aux serveurs.   
        if len(tab_commandes[j].value) == 7 :
            tab_commandes[j].value += "_" + str(num)
            print(("cuistot"+ tab_commandes[j].value, num),file=sys.stderr)
            sleep(random.random()*15) #temps de préparation
        
        sem.release()   
            


#Main---------------------------------------------------------------------------------
#c'est une liste de 50 tableau partagé contanant des caractères sur 20bytes
tab_commandes = [mp.RawArray(ctypes.c_wchar, 20) for _ in range(50)]
val = mp.Value('i',0)
event_mj = mp.Event()

#initialisation de tab_commandes
for i in range(50) :
    tab_commandes[i].value = "v"

lst_serveurs = []
lst_cuistots = []
sem = mp.Semaphore(1)
nb_serv = 5
nb_cuistot = 3

#creation des process
for i in range(nb_serv) : 
    serveur = mp.Process(target = serveurs, args = (tab_commandes,sem,i,val,event_mj))
    lst_serveurs.append(serveur)
    serveur.start()
    
for i in range (nb_cuistot) :
    cuistot = mp.Process(target = cuistots, args = (tab_commandes,sem,i,val,event_mj))
    lst_cuistots.append(cuistot)
    cuistot.start()

p_clients = mp.Process(target = clients, args = (tab_commandes,val,sem,event_mj))
major_dhomme = mp.Process(target = major, args = (tab_commandes,val,event_mj))

major_dhomme.start();p_clients.start()

sleep(240) #les processus
val.value = 1 #fin des process

#fin processus
for serveur in lst_serveurs :
    serveur.join()
    
for cuistot in lst_cuistots :
    cuistot.join()

p_clients.join();major_dhomme.join()

sys.exit(0)