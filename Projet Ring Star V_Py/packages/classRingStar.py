#*-*coding : utf-8 -*
###############################################################################
""" LES IMPORTATIONS """
from numpy import zeros
from random import randint, choice
from os import getcwd, mkdir, path
from pickle import dump, load
#from matplotlib.pyplot import plot, fill_between, grid, title, xlabel, ylabel, legend, xlim, ylim, show, savefig
##############################################################################
"""DECLARATION DE LA CLASS"""
class Algorithme_MOGA():

    ############# CONSTRUCTEUR #####################
    def __init__( self, nbreNoeud, tailleC, noeudInit, nbreGene, probEllitisme, nomFic , pourcentage):
        
        self.nombre_noeud = nbreNoeud
        self.taille_cycle = tailleC
        self.noeud_initial = noeudInit
        self.nombre_cycle_in_generation = nbreGene

        self.probabilite_mutation = 0.5
        self.probabilite_ellitisme = probEllitisme 
        self.pourcentage_stabilite = pourcentage

        self.nombre_cycle_mutation = int(round(self.nombre_cycle_in_generation * self.probabilite_mutation,0))
        self.nombre_cycle_ellistisme= int(round(self.nombre_cycle_in_generation * self.probabilite_ellitisme,0))
        self.nomFichier = nomFic    

        self.graphe_initial = zeros((self.nombre_noeud , self.nombre_noeud ), dtype='i')
        self.graphe_generation = []
        self.graphe_generation_old = []

        self.dossier_travail = getcwd()
        self.dossierFile = self.dossier_travail + str('/File/')
        self.dossierOut = self.dossier_travail + str('/Out/')
        self.dossierSave = self.dossier_travail + str('/save/')
        self.dossierView = self.dossier_travail + str('/view/')
    

    ####################################################################################################
    ############################ CONSTRUCTION DU GRAPHE ################################################
    
    def ConstructionGraphe(self):
        """Cette fonction nous permet de construire notre graphe
        à partir d'un fichier contenu dans le dossier File""" 
        
        if path.exists(self.dossierFile + self.nomFichier):
            fic = open(self.dossierFile + self.nomFichier, 'r')
            Mat = []
            for ligne in fic:
                Mat.append(ligne)
            fic.close()
            i=0 
            j=0
            for line in Mat:
                Z = []
                Z =  line.split()
                for val in Z:
                    self.graphe_initial[i,j] = int(val)
                    j = j + 1
                i = i + 1
                j = 0
        else:
            print("Verifier si le fichier existe !!!!")
    
    def AfficheGraphe(self):
        """Fonction permettant d'afficher la matrice"""
        for i in range(len(self.graphe_initial)):
            for j in range(len(self.graphe_initial)):
                print(self.graphe_initial[i,j], end=" ")
            print("\n")
    
    ############################ COUT ANNEAU : 'ring cost' #############################################

    def C( self, i, j ):   
        return self.graphe_initial[i-1,j-1]
    
    def CoutAnneau(self, cycle):
        long = 0
        j = 0
        for i in cycle[:-1]:
            j += 1
            long += self.C(i, cycle[j])
        return long

    ############################ COUT AFFECTATION : 'Assignment cost' #################################

    def D( self, cycle, Vi ):
        #Liste des noeuds non visités et leurs coût associés
        NoeudNVisites = []
        CoutNVisite = []
        for j in range(1,len(self.graphe_initial)+1):
            if not j in cycle:
                NoeudNVisites.append(j)
                CoutNVisite.append(self.C(Vi, j)) 
        
        return [NoeudNVisites[CoutNVisite.index(min(CoutNVisite))], min(CoutNVisite)]

    def CoutAffectation(self, cycle):
        Noeud = []
        Somme_cout = 0
        for i in range(len(cycle)-1):
            Noeud.append(self.D(cycle, cycle[i])[0])
            Somme_cout += self.D(cycle, cycle[i])[1]

        return Somme_cout

    ################################## GESTION POPULATION ##############################################
    
    def fonctionTri(self, population):
        """
            Fonction permettant de trier les individus en fonction de la fonction objectif coût anneau. Tri par ordre croissant.
            La méthode Tri bulle.
            Cette méthode se base sur le cout anneau et le cout d'affectation pour effetuer le tri.
            Si ces deux couts sont minimuns alors ce cycle domine sinon il reste intact dans l'ordre.
        """
        trier2 = bool()
        for i in range(0, len(population)-1):
            trier2 = True
            for j in range(0 , len(population)-1-i):  
                if self.CoutAffectation(population[j]) >= self.CoutAffectation(population[j+1]) :
                    population[j], population[j+1] = population[j+1], population[j]
                    trier2 = False
            if(trier2):
                break
        
        trier1 = bool()
        for i in range(0, len(population)-1):
            trier1 = True
            for j in range(0 , len(population)-1-i):  
                if self.CoutAnneau(population[j]) >= self.CoutAnneau(population[j+1]) :
                    population[j], population[j+1] = population[j+1], population[j]
                    trier1 = False
            if(trier1):
                break

    def NbreCyclePossibleGraphe(self):
        """Cette fonction permet de déterminer le nombre de cycle possible
        pour un graphe non orienté complet."""
        nombre = self.nombre_noeud
        nombre_cycle = 1
        for i in range(self.taille_cycle-1):
            nombre_cycle = nombre_cycle * (nombre - 1)
            nombre -= 1
        return nombre_cycle
    
    def GenerationCycle(self):
        
        cycle = [self.noeud_initial] #On initialise le cycle avec l'entête
        compteur = 0
        nombre_possibilite = self.NbreCyclePossibleGraphe()
        while(True):
            compteur += 1
            while(True):
                sommet = randint(1,len(self.graphe_initial)) #On tire une valeur aléatoire 
                if not sommet in cycle:
                    if len(cycle) == self.taille_cycle :
                        break
                    else:
                        cycle.append(sommet)

            cycle = cycle + [self.noeud_initial]
            if not cycle in self.graphe_generation_old:
                self.graphe_generation_old.append(cycle)   
                break
            else:
                cycle = [self.noeud_initial]

            if compteur == nombre_possibilite :
                break
  
    def initialisationPopulation(self):

        for i in range(self.nombre_cycle_in_generation):
            self.GenerationCycle()

        try:
            mkdir(self.dossierSave)
        except:
            pass
        #On trie notre population
        self.fonctionTri(self.graphe_generation_old)

        with open(self.dossierSave + str('sauvegarde.ring'), 'wb') as sauvegarde:
            dump(self.graphe_generation_old, sauvegarde)

        self.graphe_generation_old = []
        self.graphe_generation = []
        
    def AffichePopulation(self):
        for item in self.graphe_generation_old:
            print("{} --> ( c = {} , d = {} )".format(item,
            self.CoutAnneau(item),
            self.CoutAffectation(item)))
    
    def AffichePopulationFinal(self):
        self.fonctionTri(self.graphe_generation)
        for item in self.graphe_generation:
            print("{} --> ( c = {} , d = {} )".format(item,
            self.CoutAnneau(item),
            self.CoutAffectation(item)))
    
    ########################## FONCTION MUTATION, SELECTION, CROISEMENT  ###############################
    
    def sauvegarde_generation (self):
        """
            Fonction permettant la sauvegarde en fichier binaire de toutes les populations.
        """
        with open(self.dossierSave + str('sauvegarde.ring'), 'rb') as lecture:
            population_stockee = load(lecture)
        
        self.fonctionTri(self.graphe_generation)
        population = self.graphe_generation + population_stockee 
        
        with open(self.dossierSave + str('sauvegarde.ring'), 'wb') as sauvegarde:
            dump(population, sauvegarde)
            
        self.graphe_generation = []
        self.graphe_generation_old = []
        
    def lecture_Sauvegarde(self,end=False):
        population_generation_stockee = load(open(self.dossierSave + str('sauvegarde.ring'), 'rb'))
        if end == True:
            self.graphe_generation = []
            cpt = 0
            i = 0
            while cpt < self.nombre_cycle_in_generation:
                if not population_generation_stockee[i] in self.graphe_generation :
                    self.graphe_generation.append(population_generation_stockee[i])
                    cpt += 1
                i += 1
        else:
            for i in range(self.nombre_cycle_in_generation):
                self.graphe_generation_old.append(population_generation_stockee[i])
    
    def Mutation (self) :
        """
            Fonction permettant de créer des individus mutés de manière aléatoire 
            dans la nouvelle génération.
        """
        for cycle in self.graphe_generation:
            for elt in range(1,len(cycle)-1):
                proba = randint(0, 100)/100.00
                if proba <= self.probabilite_mutation:
                    ind = -1
                    while True:
                        ind = randint(1, len(self.graphe_initial))
                        if not ind in cycle:
                            break
                    cycle[elt] = ind
 
    def Croisement(self):  
        """Croisement uniforme"""
        for cycle in range(self.nombre_cycle_ellistisme):
            id_pere = randint(0, self.nombre_cycle_in_generation-1)
            id_mere = randint(0, self.nombre_cycle_in_generation-1)    
        
            for noeud in range(1,self.taille_cycle-1): #On laisse le noeud initial et le noeud final
                self.graphe_generation[cycle][noeud] = choice([self.graphe_generation_old[id_pere][noeud],self.graphe_generation_old[id_mere][noeud]])
    
    def selectionIndividu (self) :
        """
            Fonction permettant de sélectionner les meilleurs individus de la population total
            pour les intégrer à la génération en cours.
        """
        for cycle_i in range(self.nombre_cycle_ellistisme):
            self.graphe_generation.append(self.graphe_generation_old[cycle_i])
    
    def ConfrontationCycle(self) :
        """
            Fonction permettant de confronter deux cycles aléatoirement et de sélectionner le meilleur 
            pour la génération suivante.
        """
        #On recupère l'historique
        population_generation_stockee = load(open(self.dossierSave + str('sauvegarde.ring'), 'rb'))

        for cycle in range(self.nombre_cycle_ellistisme):
        
            while True:
                cy_1 = randint(0, len(population_generation_stockee)-1)
                cout_An1 = self.CoutAnneau(population_generation_stockee[cy_1])  
                cout_An2 = self.CoutAnneau(self.graphe_generation[cycle])
                
                if cout_An1 < cout_An2:
                    if not population_generation_stockee[cy_1] in self.graphe_generation:
                        self.graphe_generation[cycle] = population_generation_stockee[cy_1]
                        break
                else:
                    break
        
    #####################################################################################################
    
    def ValidationConvergence(self):
        #On recupère notre population finale
        self.lecture_Sauvegarde(True)

        optimisation_validee = True
        valeur = []
        for cycle in self.graphe_generation:
            val = []
            val.append(self.CoutAnneau(cycle))
            val.append(self.CoutAffectation(cycle))
            valeur.append(val)
        #On verifie le pourcentage autorisé
        for i in range(len(valeur)-1):
            for j in range(i+1,len(valeur)):
                pourAnn = (valeur[i][0] * 100) / (valeur[i][0] + valeur[j][0])
                pourAff = (valeur[i][1] * 100) / (valeur[i][1] + valeur[j][1])
                if pourAnn > self.pourcentage_stabilite or pourAff > self.pourcentage_stabilite:
                    optimisation_validee = False
                    break
            if not optimisation_validee:
                break
        return optimisation_validee

    def saveFinalSolution(self):
        try:
            mkdir(self.dossierOut)
        except:
            pass
        
        with open(self.dossierOut + str('population_finale.txt'), 'w') as population_fin:
            for cycle in self.graphe_generation :
                for parametre in cycle :
                    population_fin.write(str(parametre) + '   ')
                population_fin.write("  --> ( "+ str(self.CoutAnneau(cycle)) + " , "+ str(self.CoutAffectation(cycle)) +" )")
                population_fin.write('\n')
        
    """def ConvergenceCourbe(self):

        try:
            mkdir(self.dossierView)
        except:
            pass
        
        coutA = []
        coutAf = []
        coutPann = []
        coutPAff = []
        for cycle in self.graphe_generation :
            coutA.append(self.CoutAnneau(cycle))
            coutAf.append(self.CoutAffectation(cycle))
        for cycle in self.graphe_generation_old :
            coutPann.append(self.CoutAnneau(cycle))
            coutPAff.append(self.CoutAffectation(cycle))
        
        #On trace le graphe
        title("Graphe convergence algorithme ")
        plot(coutA, coutAf, "b", linewidth=0.8, marker="+")
        #plot(coutPann, coutPAff, "g", linewidth=0.8, marker="*")
        xlabel("Coût anneau")
        ylabel("Coût affectation")
        
        grid(True)
        show()
        #savefig(self.dossierView + 'Figure_convergence.pdf')"""
        