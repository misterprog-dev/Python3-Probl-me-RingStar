# Python3-Probl-me-RingStar
Résolution du problème RingStar avec la Méthode MOGA (MULTI-OBJECTIVE GENETIC  ALGORITHM)


*********************
   DIAKITE SOUMAILA
*********************

NB : Avant toute manipulation , il faudrait installer la librairie numpy

********************** La composition du logiciel************************************************

Notre Logiciel a été structuré de la manière modulaire suivante :
o	Un dossier File qui contient le jeu de donnée
o	Un dossier packages qui contient la classe permettant la réalisation du projet
o	Un dossier save qui contient notre fichier de sauvegarde de l’évolution de la population
o	Un dossier out qui contient la solution finale retenue
o	Un dossier view visualiser la courbe d’évolution

********************** ********************** ********************** ********************** *****
classRingStar

On a les méthodes suivantes :

Contructiongraphe : Qui permet de lire le fichier contenu dans File et remplir le graphe.

GenerationCycle : Qui permet de générer un cycle.

InitialisationPopulation : Qui permet d’initialisation la population.

CoutAnneau : Qui permet de calculer le cout anneau du cycle.

CoutAffectation : Qui permet de calculer le cout d’affectation du cycle.

fonctionTri : Qui permet de trier notre population.

sauvegarde_generation : Qui permet de sauvegarder la population en cours d’évolution.

Mutation : Qui effectue la mutation.Cette fonction permettant de créer des individus mutés de manière aléatoire dans la nouvelle génération.

Croisement : Qui effectue le croisement.

selectionIndividu : Qui permet de sélectionner les meilleurs individus de la population total pour les intégrer à la génération en cours.

ConfrontationCycle : Fonction permettant de confronter deux cycles aléatoirement et de sélectionner le meilleur pour la génération suivante.

ValidationConvergence : Fonction permettant de vérifier la convergence de l’algorithme.


************************************************************************************************

Comment lancer le logiciel ?
   
	
	-On lance le main.py
	-Vous Entrez le nom du fichier
	-Vous Entrez la taille du graphe
	-Vous Entrez la taille du cycle
	-Vous Entrez le noeud initial
	-Vous Entrez le nombre de génération
	-Vous Entrez Nombre d'échantillons par itération
	-Vous Entrez la probabilité d'éllitisme
	-Vous Entrez le pourcentage de stabilité
	-Vous appuyer Enter pour terminer les entrées de données.

Après toutes ces opérations, on observe les résultats.


