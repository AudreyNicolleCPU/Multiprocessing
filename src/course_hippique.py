"""
@author: audrey.nicolle & emma.begard
"""
# Nov 2021
# Course Hippique (version élèves)
# Version très basique, sans mutex sur l’écran, sans arbitre, sans annoncer le gagnant, ... ...
# −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# VT100 : Actions sur le curseur
# Quelques codes d’échappement (tous ne sont pas utilisés)
CLEARSCR="\x1B[2J\x1B[;H" # Clear SCReen
CLEAREOS = "\x1B[J" # Clear End Of Screen
CLEARELN = "\x1B[2K" # Clear Entire LiNe
CLEARCUP = "\x1B[1J" # Clear Curseur UP
GOTOYX = "\x1B[%.2d;%.2dH" # (’H’ ou ’f’) : Goto at (y,x), voir le code
DELAFCURSOR = "\x1B[K" # effacer après la position du curseur
CRLF = "\r\n" # Retour à la ligne
CURSON = "\x1B[?25h" # Curseur visible
CURSOFF = "\x1B[?25l" # Curseur invisible
# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m" # Normal
BOLD = "\x1B[1m" # Gras
UNDERLINE = "\x1B[4m" # Souligné
# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m" # Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m" # Rouge
CL_GREEN="\033[22;32m" # Vert
CL_BROWN = "\033[22;33m" # Brun
CL_BLUE="\033[22;34m" # Bleu
CL_MAGENTA="\033[22;35m" # Magenta
CL_CYAN="\033[22;36m" # Cyan
CL_GRAY="\033[22;37m" # Gris
# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m" # Gris foncé
CL_LIGHTRED="\033[01;31m" # Rouge clair
CL_LIGHTGREEN="\033[01;32m" # Vert clair
CL_YELLOW="\033[01;33m" # Jaune
CL_LIGHTBLU= "\033[01;34m" # Bleu clair
CL_LIGHTMAGENTA="\033[01;35m" # Magenta clair
CL_LIGHTCYAN="\033[01;36m" # Cyan clair
CL_WHITE="\033[01;37m" # Blanc
#−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−
# Juin 2019
# Cours hippique
# Version très basique, sans mutex sur l’écran, sans arbitre, sans annoncer le gagant, ... ...
# Quelques codes d’échappement (tous ne sont pas utilisés)
CLEARSCR="\x1B[2J\x1B[;H" # Clear SCReen
CLEAREOS = "\x1B[J" # Clear End Of Screen
CLEARELN = "\x1B[2K" # Clear Entire LiNe
CLEARCUP = "\x1B[1J" # Clear Curseur UP
GOTOYX = "\x1B[%.2d;%.2dH" # (’H’ ou ’f’) : Goto at (y,x), voir le code
DELAFCURSOR = "\x1B[K" # effacer après la position du curseur
CRLF = "\r\n" # Retour à la ligne
# VT100 : Actions sur le curseur
CURSON = "\x1B[?25h" # Curseur visible
CURSOFF = "\x1B[?25l" # Curseur invisible
# VT100 : Actions sur les caractères affichables
NORMAL = "\x1B[0m" # Normal
BOLD = "\x1B[1m" # Gras
UNDERLINE = "\x1B[4m" # Souligné
# VT100 : Couleurs : "22" pour normal intensity
CL_BLACK="\033[22;30m" # Noir. NE PAS UTILISER. On verra rien !!
CL_RED="\033[22;31m" # Rouge
CL_GREEN="\033[22;32m" # Vert
CL_BROWN = "\033[22;33m" # Brun
CL_BLUE="\033[22;34m" # Bleu
CL_MAGENTA="\033[22;35m" # Magenta
CL_CYAN="\033[22;36m" # Cyan
CL_GRAY="\033[22;37m" # Gris
# "01" pour quoi ? (bold ?)
CL_DARKGRAY="\033[01;30m" # Gris foncé
CL_LIGHTRED="\033[01;31m" # Rouge clair
CL_LIGHTGREEN="\033[01;32m" # Vert clair
CL_YELLOW="\033[01;33m" # Jaune
CL_LIGHTBLU= "\033[01;34m" # Bleu clair
CL_LIGHTMAGENTA="\033[01;35m" # Magenta clair
CL_LIGHTCYAN="\033[01;36m" # Cyan clair
CL_WHITE="\033[01;37m" # Blanc
#−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−

# Import-----------------------------------------------------------------
import multiprocessing as mp
from multiprocessing import Manager
from multiprocessing import managers
import os, time,math, random, sys, ctypes
from pickle import FALSE, TRUE
from urllib import request
# Une liste de couleurs à affecter aléatoirement aux chevaux
lyst_colors=[CL_WHITE, CL_RED, CL_GREEN, CL_BROWN , CL_BLUE, CL_MAGENTA, CL_CYAN, CL_GRAY,
CL_DARKGRAY, CL_LIGHTRED, CL_LIGHTGREEN, CL_LIGHTBLU, CL_YELLOW, CL_LIGHTMAGENTA, CL_LIGHTCYAN]

#Fonctions --------------------------------------------------------------

def effacer_ecran() : print(CLEARSCR,end="")

def erase_line_from_beg_to_curs() : print("\033[1K",end="")

def curseur_invisible() : print(CURSOFF,end="")

def curseur_visible() : print(CURSON,end="")

def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end="")

def en_couleur(Coul) : print(Coul,end="")

def en_rouge() : print(CL_RED,end="") # Un exemple !

def liste(tab):
    """ Création de la liste pour le classement des chevaux
    Parameters:
        entrée : 
            tab : positoin des chevaux dans l'ordre croissant
    """
    chevaux_pos = [] 
    for a in range(0, len(tab)):
        chevaux_pos .append( [chr(ord("A")+a),tab[a]] )
    return chevaux_pos
    
def up_date(tab, liste):
    """ cette fonction met à jour la position des chevaux dans la liste qui contient le classement
    parametres : 
        entrées:
            tab : liste des position sdes chevaux dans l'ordre alphabétique
            listre: la liste du classement à mettre à jour
    """
    # on met a jour les positions de chevaux
    for i in range(len(liste)) :
        # on cherche le nom du cheval a mettre a jour dans tab
        for l in range(len(tab)):
            # si le nom du cheval correspond on met sa position a jour
            if liste[i][0] ==str(chr(ord("A")+l)):
                liste[i][1] = tab[i]
                
    return liste

def tri(lst) :
    """ cette fonction tri les chevaux dans l'ordre décroissant
    paramatres :
        entrée :
            lst : la liste de listes [cheval, position] à trier
    """
    for i in range(0, len(lst)):
        for l in range(i,len(lst)):
            if lst[i][1] < lst[l][1]:
                lst[i], lst[l]= lst[l], lst[i]
    return lst

def disp_scores(lst, pos):
    """ cette fonction affiche les scores
    Parametres :
        entrée :
            lst : liste du classmeent 
            pos : la ligne d'affichage sur le terminal
    """
    premier = 0
    deuxieme = 0
    troisieme = 0
    dernier = 0
    move_to(pos, 2)
    en_couleur(CL_WHITE)
    # pour eviter d'afficher qui n'xistent pas et causer des erreurs d'index dans la liste
    if len(lst) <= 2:
        premier = lst[0][0]
        deixieme = lst[1][0]
        troisieme = 'aucun'

    elif len(lst) <= 1:
        premier = lst[0][0]
        deixieme = 'aucun'
        troisieme = 'aucun'

    else :
        premier = lst[0][0]
        deuxieme = lst[1][0]
        troisieme = lst[2][0]

    print("Premier :{} , Deuxième:{}, Troisième:{}, Dernier : {}".format(premier,deuxieme,troisieme, lst[len(lst)-1][0] ))

def arbitre(tab, fin, lettre, parie, Nb_process) : 
    """ cette fonction affiche le classment et l'affichage du pari
    Paramtres :
        entrées :
            tab : position des chevaux dans l'rdre alphabetique 
            fin : la position de fin de course
            lettre : le cheval sur leque le joueur a parié
            parie : un booléen qui indique si le joueur a parié ou pas
            Nb_process : nombre de chevaux+1 qiu courent, pour gerer l'afichage dans arbitre
    """
    # on crée l aliste des chevaux avec leurs positions
    result  = liste(tab)
   # tant que le troisième cheval n'est pas arrivé 
    while result[-1][1] < fin-1 :
        # on met a jour la liste
        result = up_date(tab, result)
        # on tri la liste avec des colones decroissantes
        result=tri(result)
        # on affiche les resultats
        disp_scores(result, (Nb_process-1)*4+4)
        pari(result, lettre, parie, (Nb_process-1)*4+3)
    # si le joueur a parié
    if parie== True :
        move_to((Nb_process-1)*4+5,2)
        en_couleur(CL_WHITE)
        # la chevl a gagné
        if result[0][0] == lettre:
            print(" Le cheval {} a gagné !!!! ".format(lettre))

        # le cheval du pari n'a pas gagné
        else :
            print(" Le cheval {} n'as pas gagné  ".format(lettre))

def saisie(Nb_process):
    """ cette fonction demande a l'utilisateur si il veut parier et renvoit le reponse et le pari
    Param :
        sortie:
            val : le cheval choisit, ou 'N' si le joueur n'as pas voulut parier
            parie : true ou false si le joueur a voulut parier
    """
    valeurs = ['A', 'B', 'C','D', 'E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    run = True 
    parie = False
    parier = input('Parier sur un cheval ? : O / N \n') 
    # pour proteger la saisie
    if parier in ['O', 'N']:
        if parier =='O':
            parie= True
            # ta,t que l'on a pas renseig,é une valeur correcte pour le pari
            while run :
                val = input('Entrer un cheval pour parrier !  lettre majuscule A à {} \n'.format(valeurs[Nb_process-2])) 
                if val in valeurs[:Nb_process] :
                    return val, parie   
        else :
            return 'N',pari  

def forme (ma_ligne, col, anim):
    """ Cette fonction dessine le cheval
    Parametres :
        entrées : 
            ma_ligne : le debut de l'affichage
            col : la colonne du début
            anim : int qui permet de choisir un modéle

        sortie : 
            anim : la forme que le cheval prendra au prochain tour
    """
    ligne = ma_ligne*3
    if anim == 0:
        # on fait la tête du cheval
        move_to(ligne+1,col+7) # pour effacer toute ma ligne   
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        # on set la couleur
        print("("+chr(ord("A")+ma_ligne)+">")
        # on fait le corps du cheval
        move_to(ligne+2,col) # pour effacer toute ma ligne   
        erase_line_from_beg_to_curs()
        # on set la couleur
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print('/|-----|')
        # on fait les pattes du cheval
        move_to(ligne+3,col+1) # pour effacer toute ma ligne   
        erase_line_from_beg_to_curs()
        # on set la couleur
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print('| | | |')
        return 1
    elif anim == 1:
        # on fait la tête du cheval
        move_to(ligne+1,col+7) # pour effacer toute ma ligne   
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        # on set la couleur
        print("("+chr(ord("A")+ma_ligne)+">")
        # on fait le corps du cheval
        move_to(ligne+2,col) # pour effacer toute ma ligne   
        erase_line_from_beg_to_curs()
        # on set la couleur
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print('/|-----|')
        # on fait les pattes du cheval
        move_to(ligne+3,col+1) # pour effacer toute ma ligne   
        erase_line_from_beg_to_curs()
        # on set la couleur
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print('\ \ \ \ ')
        return 2 
    else :
        # on fait la tête du cheval
        move_to(ligne+1,col+7) # pour effacer toute ma ligne   
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        # on set la couleur
        print("("+chr(ord("A")+ma_ligne)+">")
        # on fait le corps du cheval
        move_to(ligne+2,col) # pour effacer toute ma ligne   
        erase_line_from_beg_to_curs()
        # on set la couleur
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print('/|-----|')
        # on fait les pattes du cheval
        move_to(ligne+3,col+1) # pour effacer toute ma ligne   
        erase_line_from_beg_to_curs()
        # on set la couleur
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print('/ / / / ')
        return 1 

# La tache d’un cheval
def un_cheval(ma_ligne : int, keep_running, cadna, tab) : # ma_ligne commence à 0
    col=1
    # booléen pour l'animation
    anim = 0
    while col < LONGEUR_COURSE and keep_running.value :
        # on demande un jetton 
        cadna.acquire()
        """move_to(ma_ligne+1,col) # pour effacer toute ma ligne
        erase_line_from_beg_to_curs()
        en_couleur(lyst_colors[ma_ligne%len(lyst_colors)])
        print("("+chr(ord("A")+ma_ligne)+">")"""
        anim = forme(ma_ligne, col, anim)
        tab[ma_ligne]= col
        # on rends le jetton
        cadna.release()
        col+=1
        time.sleep(0.1*random.randint(1,5))
  
def pari(lst, lettre, parie, pos_afficher):
    """ cette fonction gere le pari, elle demande le cheval sur lequel l'utilisateur veux parier et valide seulement des lettres de l'alphabet en majuscule
    Parameters:
        entrée :        
            lst : liste avec les positions des chevaux dans l'ordre alphabetique
            lettre : la lettre du cheval sur lequel le joueur a parrié
            parie : un booléen qui indique si le joueur a voulu parier
            pos_afficher : la ligne où afficher le pari
        """
    # Si le joueur a dit vouloir parier
    if parie== True :
        # on recupere la position du cheval en temps réel
        pos = 0
        for valeur in lst :
            if valeur[0] ==  lettre :
                pos = lst.index(valeur)
        move_to(pos_afficher,2)
        en_couleur(CL_WHITE)
        # on affiche le nom du cheval et sa position dans la course
        print("Vous avez parié sur le Cheval {} ! Il est en position : {} ".format(lettre, pos+1))
    # le joueur n'as pas voulut parier
    else :
        move_to(pos_afficher,2)
        en_couleur(CL_WHITE)
        print(" Pas de pari enregistré ")
 
#−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−

# Main -----------------------------------------------------------------------------------------
def course_hippique(keep_running) :

    Nb_process=10+1
    lock = mp.Semaphore(1)
    mes_process = [0 for i in range(Nb_process) or i in range(Nb_process)]
    # la position des chevaux de chaque sous process
    tab = mp.Array('i', range(Nb_process-1) )
    # on entre une valeur pour parier
    val_pari, parie = saisie(Nb_process)


    effacer_ecran()
    curseur_invisible()


    for i in range(Nb_process): # Lancer Nb_process processus
        # si on est au dernier terme de la liste on a crée tt les chevaux, donc on lance l'arbitre
        if i == Nb_process-1:
            mes_process[i] = mp.Process(target=arbitre, args=(tab,LONGEUR_COURSE, val_pari, parie, Nb_process))
            mes_process[i].start()
        #on crée tt les chevaux
        else : 
            mes_process[i] = mp.Process(target=un_cheval, args= (i,keep_running,lock,tab))
            mes_process[i].start()


    move_to( (Nb_process-1)*4+1, 10)
    en_couleur(CL_WHITE)
    print("C'est parti !!!! ")

    for i in range(Nb_process): 
        mes_process[i].join()


    move_to((Nb_process-1)*4+6, 1)
    curseur_visible()
    print("Course finie")

if __name__ == "__main__" :
    LONGEUR_COURSE = 100# Tout le monde aura la même copie (donc no need to have a ’value’)
    keep_running=mp.Value(ctypes.c_bool, True)

    course_hippique(keep_running)