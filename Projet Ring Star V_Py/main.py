#*-*coding : utf-8 -*
"""
AUTEUR : DIAKITE SOUMAILA
"""

from packages.classRingStar import *
import time as tps


if __name__ == "__main__":

    nomFichier = input("\nEntrez le nom du fichier : ")
    tailleGraphe = int(input("Entrez la taille du graphe : "))
    tailleCycle = int(input("Entrez la taille du cycle : "))
    noeudInitial = int(input("Entrez le noeud initial : "))
    nbreGeneration = int(input("Entrez le nombre de génération : "))
    nbreByIteration = int(input("Nombre d'échantillons par itération : "))
    probEllitisme = float(input("Entrez la probabilité d'éllitisme : "))
    pourcentage_stabilite = int(input("Entrez le pourcentage de stabilité : "))
    
    print("\n\n***************************** RESOLUTION RING STAR ********************************\n\n")

    #CONSTRUCTION DU GRAPHE
    #Il faut vérifier le nombre de cycle possible pour le graphe complet
    #Il faut contrôler le noeud initial<taille graphe
    #Contrôler la probabilité d'ellitisme>0 et <1
    #Il faut contrôler les différentes variables

    graphe = Algorithme_MOGA(tailleGraphe, tailleCycle, noeudInitial, nbreGeneration, probEllitisme, nomFichier ,pourcentage_stabilite)
    
    compteur_arret = 100
    graphe.ConstructionGraphe()
    #On met le chrono en marche
    temps_init = tps.time()

    graphe.initialisationPopulation()
    ###################################################
    while True:
        for i in range(nbreByIteration):
            graphe.lecture_Sauvegarde(False)
            graphe.selectionIndividu()
            graphe.Croisement()
            graphe.Mutation()
            graphe.ConfrontationCycle()
            if i != nbreByIteration - 1 :
                graphe.sauvegarde_generation()
        
        """La MOGA converge lorsque le pourcentage maximal autorisé de Pareto ou le
        pourcentage de stabilité de la convergence est atteint."""
        #On vérifie la convergence

        if graphe.ValidationConvergence() : #optimisation convergée
            graphe.AffichePopulationFinal()
            print("\nArrêt par convergence !!!\n")
            graphe.saveFinalSolution()
            break
        else : #optimisation non convergée
            """Si l'optimisation n'a pas convergé, elle est validée pour le respect des critères d'arrêt.
            On vérifie le critère d'arrêt.
            Lorsque le critère Nombre maximal d'itérations est rempli, le processus est arrêté sans
            atteindre la convergence."""
            if compteur_arret == 0 :
                graphe.AffichePopulationFinal()
                print("\nArrêt par critère d'arrêt !!!\n")
                graphe.saveFinalSolution()
                break
            else : #Critères d'arrêt non remplis
                compteur_arret -= 1
    
    #On arrêt le chrono.
    temps_final = tps.time() - temps_init
    print("Le temps écoulé : {} s \n".format(round(temps_final)))
    
    print("\n\n****************************************************************************\n\n")
    