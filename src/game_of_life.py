"""
@author: audrey.nicolle & emma.begard
"""
# game of life 7
# Import ---------------------------------------------------------------------------------------------------
import multiprocessing as mp 
import random, time

# Fonctions ------------------------------------------------------------------------------------------------
CLEARSCR="\x1B[2J\x1B[;H" # Clear SCReen
CLEARCUP = "\x1B[1J" # Clear Curseur UP
CL_BLACK="\033[22;30m" # Noir.  UTILISER. On verra rien, donc ça ferra comme si la cellule avait disparue !!

def move_to(lig, col) : print("\033[" + str(lig) + ";" + str(col) + "f",end="")
def erase_line_from_beg_to_curs() : print("\033[1K",end="")

# Classe ---------------------------------------------------------------------------------------------------
class game_of_life:
    """ Classe qui gère le jeu de la vie et l'affiche """
    def __init__(self, nb_colones, nb_lignes):
        # attributs pour création de la grille de cellules
        self.__nb_colonnes =  nb_colones
        self.__nb_lignes =  nb_lignes
        
    def initialisation(self):
        """ Cette fonction crée la grille de cellule et leur attribut un état aléatoire à la création """
        taille = self.__nb_colonnes*self.__nb_lignes
        # on stocke notre grille partagée
        self.grille = mp.Array('i', [random.randint(0,1) for _ in range(taille)]) 

    def recup_environnement(self, debut, fin):
        """ Cette fonction recupere l'état de l'environnement des cellules et leur donne un état
        Parameters:
            entrées :
                debut : indice de départ de la zone de tableau traitée
                fin : indice de fin de la zone de tableau traitée
        """
        while True:
            i = debut # indice de la première celule traitée par le process
            indice_max = self.__nb_colonnes*self.__nb_lignes-1
            nb_lignes = len(self.grille[debut:fin])/self.__nb_colonnes
            time.sleep(0.2)

            # pour chaque ligne
            for l in range( int(nb_lignes) ):
                # pour chaque collone
                for c in range(self.__nb_colonnes):
                    
                    if i == 0: # coin haut gauche du tableau partagé
                        self.cell_life(['None', 'None','None', i+1, i+1+self.__nb_colonnes, i+self.__nb_colonnes, 'None','None'], i)
                    
                    elif i == self.__nb_colonnes-1: # coin haut droit du tableau partagé
                        self.cell_life(['None', 'None', 'None','None','None', i+self.__nb_colonnes, i-1+self.__nb_colonnes, i-1], i)

                    # si il s'agit de la premiere ligne du tableau partagé
                    elif i >0 and i <(self.__nb_colonnes-1) :
                        self.cell_life(['None', 'None', 'None', i+1 , i+self.__nb_colonnes, i+self.__nb_colonnes-1,i+self.__nb_colonnes-2, i-1], i)
                    
                    elif i == (indice_max - self.__nb_colonnes +1): # coin bas gauche
                        self.cell_life(['None', i-self.__nb_colonnes, i-self.__nb_colonnes+1, i+1, 'None','None','None','None'], i)
                    
                    elif i == indice_max :# coin bas droit du tableau partagé
                        self.cell_life( [i-1-self.__nb_colonnes, i-self.__nb_colonnes, 'None', 'None', 'None', 'None', 'None', i-1], i)
                    
                    # on teste si on est pas sur la dernière ligne du tableau partagé 
                    elif i > (indice_max - self.__nb_colonnes +1) and i<indice_max: # on est sur la dernière ligen du tableau 
                        self.cell_life([i-1-self.__nb_colonnes, i-self.__nb_colonnes, i-self.__nb_colonnes+1, i+1, 'None', 'None','None', i-1], i)
                    
                    # il ne reste plus qu'à détecter les bords
                    elif c == 0:# bord gauche
                        self.cell_life( ['None', i-self.__nb_colonnes, i-self.__nb_colonnes+1, i+1, i+self.__nb_colonnes+1, i+self.__nb_colonnes, 'None', 'None'] , i)     

                    elif c == (self.__nb_colonnes-1) : # bord droit 
                        self.cell_life( [i-self.__nb_colonnes-1, i-self.__nb_colonnes, 'None', 'None', 'None', i+self.__nb_colonnes, i+self.__nb_colonnes-1, i-1] , i)     
                    
                    else :
                        self.cell_life( [i-self.__nb_colonnes-1, i-self.__nb_colonnes, i-self.__nb_colonnes+1, i+1, i+self.__nb_colonnes+1, i+self.__nb_colonnes, i+self.__nb_colonnes-1, i-1], i)
                    
                    i +=1

    def  cell_life(self, liste, index_cellule):
        """ cette fonction donne un état à la cellule
        Parametres :
            entrées :
                liste : la liste des cellules voisines
                index_cellule: l'index de la cellule dans le tableau partagé
        """
        vivants, morts = 0 ,0
        for cellule in liste :
            # on est dans le cas ou il n'y a pas de cellule voisine à la position
            try :
                if cellule =='None':
                # on est dans le cas ou il n'y a pas de cellule voisine à la position
                    pass
                elif self.grille[cellule] == 1:
                    vivants += 1
                else : 
                    morts += 1
            except :
                print('pb avec indice', cellule)

        # cas où la cellule meurt 
        if self.grille[index_cellule] ==1 :
            if vivants < 2 or vivants > 3:
                self.grille[index_cellule] = 0 

        # la cellule vie 
        else :
            if vivants == 2 or vivants == 3:
                self.grille[index_cellule] = 1

    def display(self):
        """ Cette fonction gère l'affichage du tableau"""
        run = True
        i=0
        while run:
            move_to(i+5, 5)
            erase_line_from_beg_to_curs()
            depart = i*(self.__nb_colonnes)
            fin = depart + self.__nb_colonnes
            #print('A')
            print(self.grille[depart: fin])
            i+=1
            if i >= self.__nb_lignes :
                run = False

    def main(self):
        """Cette fonction fait tourner le jeux """
        self.initialisation()
        run = True
        p1= mp.Process(target=self.recup_environnement, args=(0, 2*self.__nb_colonnes))
        p2 = mp.Process( target=self.recup_environnement, args=(2*self.__nb_colonnes, self.__nb_lignes*self.__nb_colonnes) )
        p1.start()
        p2.start()
        while run :
            self.display()

# Main -----------------------------------------------------------------------------------    
jeux= game_of_life(15,15)
jeux.main()