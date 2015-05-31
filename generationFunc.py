# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 11:04:43 2015

@author: 3100366
"""

from classSkeleton import *

from anim import *


###############################################    
###############################################
#########GNERATION MOUVEMENTS RELATIFS#########
###############################################
###############################################
       
def generate_move_velocity_varition(model, nbIma, firstIm, path, nameMove):
    '''
    génère et enregistre un mouvement en s'appuyant des paramètres du modèle "model" qui est un modèle relatif
    
    paramètres :
    model = un modèle
    nbIma = nombre d'image du mouvement
    firstIm = la première image du mouvement qui sera modifié avec des translation par rapport aux vitesses. Il faut récupérer l'image moyenne d'un modèle absolu ou centré.
    path = le chemin où sera enregistré le nouveau mouvement
    nameMove = le nom du fichier du mouvement
    
    sortie :
    newMouv = le mouvement généré
    '''
    trans = model.transmat_
    start = model.startprob_
    newMouv = []
    startcs = np.cumsum(start)
    etat = np.argmin(np.where((startcs >= np.random.rand()) == True, startcs, 2))
    modifMouv = model.means_[etat]
    newMouv.append(firstIm)
    mouvSuiv = newMouv[len(newMouv)-1] + modifMouv
    mouvSuiv = remake_skeleton(firstIm, mouvSuiv)
    newMouv.append(mouvSuiv)
    for i in range(nbIma-2):
        print etat
        transcs = np.cumsum(trans[etat,:])
        alea = np.random.rand()
        etat = np.argmin(np.where((transcs >= alea) == True, transcs, 2))
        #modifMouv = model._generate_sample_from_state(etat)
        modifMouv = model.means_[etat]
        mouvSuiv = newMouv[len(newMouv)-1] + modifMouv
        mouvSuiv = remake_skeleton(firstIm, mouvSuiv)
        newMouv.append(mouvSuiv)
    register_move(newMouv, nameMove, path)
    return np.array(newMouv)
    
def generate_move_velocity_varition2(model, nbIma, firstIm, changement, path, nameMove):
    '''
    génère et enregistre un mouvement en s'appuyant des paramètres du modèle "model" qui est un modèle relatif, en forcant le changement si le HMM reste trop longtemps dans le même état
    
    paramètres :
    model = un modèle
    nbIma = nombre d'image du mouvement
    firstIm = la première image du mouvement qui sera modifié avec des translation par rapport aux vitesses. Il faut récupérer l'image moyenne d'un modèle absolu ou centré.
    changement = nombre defois où l'on peut rester dans le même état avant de devoir changer.    
    path = le chemin où sera enregistré le nouveau mouvement
    nameMove = le nom du fichier du mouvement
    
    sortie :
    newMouv = le mouvement généré
    '''
    trans = model.transmat_
    start = model.startprob_
    cpt = 0
    newMouv = []
    startcs = np.cumsum(start)
    etat = np.argmin(np.where((startcs >= np.random.rand()) == True, startcs, 2))
    modifMouv = model.means_[etat]
    newMouv.append(firstIm)
    mouvSuiv = newMouv[len(newMouv)-1] + modifMouv
    mouvSuiv = remake_skeleton(firstIm, mouvSuiv)
    newMouv.append(mouvSuiv)
    etatAncien = etat
    for i in range(nbIma-2):
        print etat
        transcs = np.cumsum(trans[etat,:])
        alea = np.random.rand()
        etat = np.argmin(np.where((transcs >= alea) == True, transcs, 2))
        if(cpt == changement):
            cpt = 0
            while(etat == etatAncien):
                transcs = np.cumsum(trans[etat,:])
                alea = np.random.rand()
                etat = np.argmin(np.where((transcs >= alea) == True, transcs, 2))
        if(etat == etatAncien): cpt+=1
        else: etatAncien = etat
        #modifMouv = model._generate_sample_from_state(etat)
        modifMouv = model.means_[etat]
        mouvSuiv = newMouv[len(newMouv)-1] + modifMouv
        mouvSuiv = remake_skeleton(firstIm, mouvSuiv)
        newMouv.append(mouvSuiv)
    register_move(newMouv, nameMove, path)
    return np.array(newMouv)
    
#Pas de changement d'état dans cette fonction. Permet d'analyser le comportement d'un état
def generate_move_velocity_varition_un_etat(model, nbIma, firstIm, etat, path, nameMove):
    '''
    génère et enregistre un mouvement en restant dans le même état et en s'appuyant des paramètres du modèle "model" qui est un modèle relatif
    
    paramètres :
    model = un modèle
    nbIma = nombre d'image du mouvement
    firstIm = la première image du mouvement qui sera modifié avec des translation par rapport aux vitesses. Il faut récupérer l'image moyenne d'un modèle absolu ou centré.
    etat = l'état dans lequel on reste
    path = le chemin où sera enregistré le nouveau mouvement
    nameMove = le nom du fichier du mouvement
    
    sortie :
    newMouv = le mouvement généré
    '''
    newMouv = []
    modifMouv = model.means_[etat]
    newMouv.append(firstIm)
    mouvSuiv = newMouv[len(newMouv)-1] + modifMouv
    mouvSuiv = remake_skeleton(firstIm, mouvSuiv)
    newMouv.append(mouvSuiv)
    for i in range(nbIma-2):
        #modifMouv = model._generate_sample_from_state(etat)
        modifMouv = model.means_[etat]
        mouvSuiv = newMouv[len(newMouv)-1] + modifMouv
        mouvSuiv = remake_skeleton(firstIm, mouvSuiv)
        newMouv.append(mouvSuiv)
    register_move(newMouv, nameMove, path)
    return np.array(newMouv)


###############################################    
###############################################
####GNERATION MOUVEMENTS ABSOLUS ET CENTRES####
###############################################
###############################################

def generate_move_translation(model, nbTrans, fps, path, nameMove):
    '''
    génère et enregistre un mouvement en s'appuyant des paramètres du modèle "model" qui est un modèle centré ou absolu
    
    paramètres :
    model = un modèle
    nbTrans = nombre de translations du mouvement
    fps = la vitesse de translation d'une image à l'autre
    path = le chemin où sera enregistré le nouveau mouvement
    nameMove = le nom du fichier du mouvement
    
    sortie :
    newMouv = le mouvement généré
    '''
    trans = model.transmat_
    start = model.startprob_
    newMouv = []
    startcs = np.cumsum(start)
    etat = np.argmin(np.where((startcs >= np.random.rand()) == True, startcs, 2))
    etatAncien = etat
    newMouv.append(model.means_[etat])
    cpt = 0
    while(cpt <= nbTrans):
        transcs = np.cumsum(trans[etat,:])
        alea = np.random.rand()
        etat = np.argmin(np.where((transcs >= alea) == True, transcs, 2))
        if(etat != etatAncien):
            print etat
            cpt+=1
            translation = translation_skeleton(np.array([newMouv[-1], model.means_[etat]]), fps)
            for i in range(len(translation)):
                newMouv.append(translation[i])
            etatAncien = etat
    register_move(newMouv, nameMove, path)
    return np.array(newMouv)

###############################################    
###############################################
####FONCTIONS USUELLES SUR LES MOuVEMENTS######
###############################################
###############################################

def translation_skeleton(mat, fps):
    '''
    génère un mouvement en reliant les positions dans mat
    
    paramètres :
    mat = la matrice qui contient des positions qu'il faut relier par translation
    fps = la vitesse de translation d'une image à l'autre
    
    sortie :
    allMouv = le mouvement généré
    '''
    matBis = desaligner_data(mat)
    m = np.zeros((20,3))
    mouv = np.copy(m)
    allMouv = []
    lineax = []
    lineay = []
    lineaz = []
    for i in range(len(matBis)-1):
        for j in range(len(matBis[i])):
            lineax.append(np.linspace(matBis[i][j][0], matBis[i+1][j][0], fps))
            lineay.append(np.linspace(matBis[i][j][1], matBis[i+1][j][1], fps))
            lineaz.append(np.linspace(matBis[i][j][2], matBis[i+1][j][2], fps))
        for k in range(fps):
            for l in range(len(lineax)):
                mouv[l][0] = lineax[l][k]
                mouv[l][1] = lineay[l][k]
                mouv[l][2] = lineaz[l][k]
            allMouv.append(mouv)
            mouv = np.copy(m)
        lineax = []
        lineay = []
        lineaz = []
    allMouv = aligner_data(allMouv)
    return allMouv

def remake_skeleton(imageDepart, nouvelleImage):
    '''
    fonction pour garder un squelette semblable au premier squelette tout au long d'un mouvement (évite le déformation)
    
    paramètres :
    imageDepart = l'image qui a le squelette qu'il faut conserver à la prochaine image
    nouvelleImage = l'image qui aura le nouveau squelette.
    
    sortie :
    nouvelleImage renormalisée
    '''
    squeletteOriginal = GrapheSquelette()
    squeletteOriginal.createSkeleton(imageDepart)
    squeletteNouveau = GrapheSquelette()
    squeletteNouveau.createSkeleton(nouvelleImage)
    for i in range(len(squeletteNouveau.squelette)):
        jointO = squeletteOriginal.squelette[i]
        jointN = squeletteNouveau.squelette[i]
        if(len(jointN.jointsSuiv) > 0):
            for j in range(len(jointN.jointsSuiv)):
                tailleMembreO = np.linalg.norm(jointO.noeud - jointO.jointsSuiv[j].noeud)
                tailleMembreN = np.linalg.norm(jointN.noeud - jointN.jointsSuiv[j].noeud)
                rapport = tailleMembreO / tailleMembreN
                auxNoeudN = jointN.noeud # auxNoeudN doit permettre au noeud i de ne pas etre modifier seul les voisins descendants le seront
                squeletteNouveau.squelette[i].setNoeud(jointN.noeud*rapport)
                squeletteNouveau.squelette[i].jointsSuiv[j].setNoeud(jointN.jointsSuiv[j].noeud*rapport)
                #On remet à jour le noeud i :
                translation = auxNoeudN - squeletteNouveau.squelette[i].noeud
                squeletteNouveau.squelette[i].setNoeud(squeletteNouveau.squelette[i].noeud + translation)
                #On remet aussi a jour le noeud descendant pour garder la norme :
                squeletteNouveau.squelette[i].jointsSuiv[j].setNoeud(squeletteNouveau.squelette[i].jointsSuiv[j].noeud + translation)
    return squeletteNouveau.genererImage()

def register_move(newMouv, nomFic, path):
    '''
    prend un tableau de mouvement de taille (,60) et enregistre le mouvement
    
    paramètres:
    newMouv = le mouvement à enregistrer
    nomFic = le nom du fichier enregistré
    path = l'endroit où on enregistre nomFic
    '''  
    if(nomFic[-4:] != ".txt"):
        nomFic+=".txt"
    monFichier = open(path+"/"+nomFic, "w")
    
    for i in range(len(newMouv)):
        monFichier.writelines(str(i)+"\n")
        for j in xrange(0, len(newMouv[i]), 3):
            monFichier.writelines(str(newMouv[i][j])+" "+str(newMouv[i][j+1])+" "+str(newMouv[i][j+2])+ " " +str(1)+"\n")
    monFichier.close()

