# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 18:51:20 2015

@author: Manence
"""

import numpy as np
import re
from hmmlearn.hmm import GaussianHMM


###############################################    
###############################################
##########DECLARATION DES CLASSES##############
###############################################
###############################################

#NoeudJoint et GrapheSquelette serviront à normaliser le squelette lors de la génération de mouvements

class NoeudJoint():
    '''
    attribut :
    JointsSuiv = liste des jointures qui suivent directement (de bas en haut) la jointure actuelle, exemple : pour le elbowRight, son jointsSuiv possède wristleRight
    noeud = la jointure actuelle
    '''
    def __init__(self, noeud):
        self.jointsSuiv = []
        self.noeud = noeud # un noeud est un triplé x y z
    def addSuiv(self, noeudSuiv):
        self.jointsSuiv.append(noeudSuiv)
    def setNoeud(self, noeud):
        self.noeud = noeud
        
class GrapheSquelette():
    '''
    attribut :
    squelette = le squelette du mouvement, créé par la fonction createSquelette
    '''
    def __init__(self):
        self.squelette = []
    def addMember(self, member):
        self.squelette.append(member)
    def genererImage(self):
        '''
        retourne une image à partir d'un objet GrapheSquelette
        '''
        return np.array([self.squelette[11].noeud, self.squelette[10].noeud,self.squelette[1].noeud,
                        self.squelette[0].noeud,self.squelette[3].noeud,self.squelette[5].noeud,
                        self.squelette[7].noeud,self.squelette[9].noeud,self.squelette[2].noeud,
                        self.squelette[4].noeud,self.squelette[6].noeud,self.squelette[8].noeud,
                        self.squelette[13].noeud,self.squelette[15].noeud,self.squelette[17].noeud,
                        self.squelette[19].noeud,self.squelette[12].noeud,self.squelette[14].noeud,
                        self.squelette[16].noeud,self.squelette[18].noeud]).ravel()
    def createSkeleton(self, image):
        '''
        forme le squlette d'une image à la manière d'un graphe orienté partant de la tête jusqu'aux pieds
        
        paramètres:
        image : une position d'un mouvement = un vecteur de 60 coordonnées
        '''
        hipCenter = NoeudJoint(np.array([image[0], image[1], image[2]]))
        spine = NoeudJoint(np.array([image[3], image[4], image[5]]))
        shoulderCenter = NoeudJoint(np.array([image[6], image[7], image[8]]))
        head = NoeudJoint(np.array([image[9], image[10], image[11]]))
        shoulderLeft = NoeudJoint(np.array([image[12], image[13], image[14]]))
        elbowLeft = NoeudJoint(np.array([image[15], image[16], image[17]]))
        wristleLeft = NoeudJoint(np.array([image[18], image[19], image[20]]))
        handLeft = NoeudJoint(np.array([image[21], image[22], image[23]]))
        shoulderRight = NoeudJoint(np.array([image[24], image[25], image[26]]))
        elbowRight = NoeudJoint(np.array([image[27], image[28], image[29]]))
        wristleRight = NoeudJoint(np.array([image[30], image[31], image[32]]))
        handRight = NoeudJoint(np.array([image[33], image[34], image[35]]))
        hipLeft = NoeudJoint(np.array([image[36], image[37], image[38]]))
        kneeLeft = NoeudJoint(np.array([image[39], image[40], image[41]]))
        ankleLeft = NoeudJoint(np.array([image[42], image[43], image[44]]))
        footLeft = NoeudJoint(np.array([image[45], image[46], image[47]]))
        hipRight = NoeudJoint(np.array([image[48], image[49], image[50]]))
        kneeRight = NoeudJoint(np.array([image[51], image[52], image[53]]))
        ankleRight = NoeudJoint(np.array([image[54], image[55], image[56]]))
        footRight = NoeudJoint(np.array([image[57], image[58], image[59]]))
        head.addSuiv(shoulderCenter)
        shoulderCenter.addSuiv(shoulderRight)
        shoulderCenter.addSuiv(shoulderLeft)
        shoulderRight.addSuiv(elbowRight)
        shoulderLeft.addSuiv(elbowLeft)
        elbowRight.addSuiv(wristleRight)
        elbowLeft.addSuiv(wristleLeft)
        wristleRight.addSuiv(handRight)
        wristleLeft.addSuiv(handLeft)
        shoulderCenter.addSuiv(spine)
        spine.addSuiv(hipCenter)
        hipCenter.addSuiv(hipRight)
        hipCenter.addSuiv(hipLeft)
        hipRight.addSuiv(kneeRight)
        hipLeft.addSuiv(kneeLeft)
        kneeRight.addSuiv(ankleRight)
        kneeLeft.addSuiv(ankleLeft)
        ankleRight.addSuiv(footRight)
        ankleLeft.addSuiv(footLeft)
        self.addMember(head) #0
        self.addMember(shoulderCenter) #1  
        self.addMember(shoulderRight) #2    
        self.addMember(shoulderLeft) #3    
        self.addMember(elbowRight) #4
        self.addMember(elbowLeft) #5
        self.addMember(wristleRight) #6
        self.addMember(wristleLeft) #7
        self.addMember(handRight) #8
        self.addMember(handLeft) #9
        self.addMember(spine) #10
        self.addMember(hipCenter) #11
        self.addMember(hipRight) #12
        self.addMember(hipLeft) #13
        self.addMember(kneeRight) #14
        self.addMember(kneeLeft) #15
        self.addMember(ankleRight) #16
        self.addMember(ankleLeft) #17
        self.addMember(footRight) #18
        self.addMember(footLeft) #19

###############################################    
###############################################
#####FONCTIONS DE LECTURE DE FICHIERS##########
###############################################
###############################################

def read_file( filename, path):
    '''
    lecture d'un fichier où sont stockés les mouvements
    
    paramètres :
    filename = nom du fichier à lire
    path = endroit où est situé le fichier
    
    sortie :
    motion_data = Un mouvement = tableau de vecteurs de 60 coordonnées
    '''
    fic = open(path+"/"+filename+".txt", "r")    
    motion_data = []
    data = np.zeros(60)
    line=" "
    i=4
    j=0
    while(line != ''):
        line = fic.readline()
        try:
            x, y, z, w = line.split()
        except ValueError:
            continue
        data[i-(4+j)] = float(re.sub(r",", r".", x))
        data[i-(3+j)] = float(re.sub(r",", r".", y))
        data[i-(2+j)] = float(re.sub(r",", r".", z))
        #data[i-1] = float(re.sub(r",", r".", w))
        if(i%80 == 0):
            motion_data.append(data)
            data = np.zeros(60)
            i = 0
            j=-1
        i+=4
        j+=1
    fic.close()
    motion_data = np.array(motion_data)
    return motion_data
    
#lit tous les fichiers d'une meme classe. Ils sont enregistré de cette manière : saut1, saut2... sautn
def read_all_files(filename, nbfiles, path):
    '''
    lit tous les fichiers d'une meme classe. Ils doivent être enregistrés de cette manière : mouv1, mouv2... mouvn
    
    paramètres :
    filename = nom du fichier à lire
    nbfiles = nombre de fichiers à lire pour un cluster
    path = endroit opù est situé le fichier
    
    sortie :
    all_motion_data = tableau à trois dimension représentant un cluster possèdant des mouvements possèdant lui même des positions
    '''
    all_motion_data = []
    for i in range (1,nbfiles+1):
        try:
            all_motion_data.append(read_file(filename+str(i), path))
        except:
            break
    all_motion_data = np.array(all_motion_data)
    return all_motion_data



class listeModeles():
    '''
    listeModeles est la classe principale qui possède une liste de modèles hmm et une liste de tests
    
    attribut :
    tabModels = table de hachage des modèles. Le premier élément d'une ligne est le nom d'un cluster, les éléments d'après sont des modèles qui ont été appris sur ce cluster
    tabTests = table de hachage des modèles. Le premier élément d'une ligne est le nom du test
    '''    
    def __init__(self):
        self.tabModels = []
        self.tabTests = []
    def addModel(self, nom, data, nbEtats, n_iter, startprob_prior=None, transmat_prior=None):
        '''
        ajoute un model à tabModels
        
        paramètres :
        nom = nom du modèle
        data = tableau à trois dimension représentant un cluster possèdant des mouvements possèdant lui même des positions        
        nbEtats = nombre d'états cachés pour chaque modèle
        n_iter = nombre d'itérations pour l'algorithme de Baum-Welch
        startprob_prior = la matrice initiale à priori
        transmat_prior = la matrice de transition à priori des états
        '''
        model = GaussianHMM(nbEtats, covariance_type="diag", n_iter=n_iter, startprob_prior=startprob_prior, transmat_prior=transmat_prior)      
        model.fit(data)
        verif_set_transMat(model)
        taille = len(self.tabModels)
        if(taille == 0):
            self.tabModels.append([nom])
            self.tabModels[0].append(model)
            return
        for i in range(taille):        
            if(self.tabModels[i][0] == nom):
                self.tabModels[i].append(model)
                return
        self.tabModels.append([nom])
        self.tabModels[-1].append(model)
    def addTest(self, nom, data):
        '''
        ajoute un test à tabTests
        
        paramètres :
        nom = nom du test
        data = tableau à deux dimensions représentant un mouvements possèdant des positions        
        '''
        taille = len(self.tabTests)
        if(taille == 0):
            self.tabTests.append([nom])
            self.tabTests[0].append(data)
            return
        for i in range(taille):        
            if(self.tabTests[i][0] == nom):
                self.tabTests[i].append(data)
                return
        self.tabTests.append([nom])
        self.tabTests[-1].append(data)
    def genererModels(self, path, names, nbfiles=200, nbEtats=10, n_iter=300, t="absolu", startprob_prior=None, transmat_prior=None, f_read = read_all_files):
        '''
        lit et crée un tableau de données pour génèrer automatiquement autant de modèle qu'il y en a dans "names"
        
        paramètres :
        path = chemin où se trouvent les données
        names = les noms des clusters à lire dans le dossier
        nbfiles = nombre de fichiers à lire pour un cluster
        nbEtats = nombre d'états cachés pour chaque modèle
        n_iter = nombre d'itérations pour l'algorithme de Baum-Welch
        startprob_prior = la matrice initiale à priori
        transmat_prior = la matrice de transition à priori des états
        t = type de données. t peut etre soit absoulu (brut) soit relatif(variation de vitesse) soit barycentre (centré au niveau du barycentre du squelette)
        f_read = fonction de lecture de fichier
        '''
        for f in names:
            data = f_read(f, nbfiles, path)
            if(t == "relatif"):
                data = to_relative_all(data)
            if(t == "barycentre"):
                data = centrer_plan_squelette_all(data)
            self.addModel(f, data, nbEtats, n_iter, startprob_prior, transmat_prior)
    def genererTests(self, path, names, nbfiles=200, t="absolu", f_read = read_all_files):
        '''
        lit et crée un tableau de données pour génèrer automatiquement autant de tests qu'il y en a dans "names"
        
        paramètres :
        path = chemin où se trouve les données
        names = les noms des clusters à lire dans le dossier
        nbfiles = nombre de fichiers à lire pour un cluster
        t = type de données. t peut etre soit absoulu (brut) soit relatif(variation de vitesse) soit barycentre (centré au niveau du barycentre du squelette)
        f_read = fonction de lecture de fichier
        '''
        for f in names:
            data = f_read(f, nbfiles, path)
            if(t == "relatif"):
                data = to_relative_all(data)
            if(t == "barycentre"):
                data = centrer_plan_squelette_all(data)
            for i in range(len(data)):
                self.addTest(f, data[i])
    def getModel(self, name):
        '''
        récupère un modèle de tabModels
        
        paramètre
        name = nom du modèle à récupérer (une chaine de charactères)
        '''
        aux = np.array(self.tabModels)
        return aux[np.where(aux[:,0] == name)].ravel()
    def getTest(self, name):
        '''
        récupère un test de tabTests
        
        paramètre
        name = nom du test à récupérer (une chaine de charactères)
        '''
        for i in range(len(self.tabTests)):
            if(self.tabTests[i][0] == name):
                return self.tabTests[i]
        return []
    #
    def removeModel(self, name, numModel=0):
        '''
        supprime un modèle
        
        si numModel=0 tous les modèles de name seront supprimés, sinon juste celui à l'indice numModel
        name = nom du modèle à supprimer (une chaine de charactères)
        numModel = l'indice du modèle à supprimer
        '''
        for i in range(len(self.tabModels)):
            if(name == self.tabModels[i][0]):
                if(numModel == 0):
                    self.tabModels.pop(i)
                    return
                else:
                    self.tabModels[i].pop(numModel)
                    return                    
    def removeTest(self, name, numTest=0):
        '''
        supprime un test
        
        si numModel=0 tous les tests de name seront supprimés, sinon juste celui à l'indice numModel
        name = nom du test à supprimer (une chaine de charactères)
        numTest = l'indice du test à supprimer
        '''
        for i in range(len(self.tabTests)):
            if(name == self.tabTests[i][0]):
                if(numTest == 0):
                    self.tabTests.pop(i)
                    return
                else:
                    self.tabTests[i].pop(numTest)
                    return
    def prediction(self, test):
        '''
        prédit la valeur d'un test d'après tous les modèles de tabModels
        
        paramètres:
        test = un mouvement
        
        sortie :
        tabScores = le tableau des scores des modèles
        le modèle qui a obtenu le meilleur score
        le nom du cluster prédit
        '''
        tabScores = []
        best = -np.inf
        bestInd = 0
        bestMod = 0
        for i in range(len(self.tabModels)):
            tabScoreMod = [] # tableau des scores par modèle (exemple: pour saut, course etc)
            for j in range(1, len(self.tabModels[i])):
                mod = self.tabModels[i][j]
                tabScoreMod.append(mod.score(test))
            tabScoreMod = np.array(tabScoreMod)
            if(np.max(tabScoreMod) > best):
                best = np.max(tabScoreMod)
                bestMod = np.argmax(tabScoreMod)
                bestInd = i
            tabScores.append(tabScoreMod)
        return np.array(tabScores), self.tabModels[bestInd][bestMod+1], self.tabModels[bestInd][0]
    def predictionUnModele(self, test, numModele):
        '''
        prédit la valeur d'un test d'après un type modèle (modèles créés avec les mêmes paramètres) de tabModels
        
        paramètres:
        test = un mouvement
        numModèle = numéro du modèle pour chaque cluster
        
        sortie :
        tabScores = le tableau des scores des modèles
        le nom du cluster prédit
        '''
        tabScores = []
        best = -np.inf
        bestInd = 0
        for i in range(len(self.tabModels)):
            mod = self.tabModels[i][numModele]
            score = mod.score(test)
            if(score > best):
                best = score
                bestInd = i
            tabScores.append(score)
        return np.array(tabScores), self.tabModels[bestInd][0]
    def score(self):
        '''
        donne le score pour un objet listeModeles en utilisant tous ses tests et tous ses modèles
        
        sortie :
        score = le pourcentage de taux de bonnes classifications
        tabScore = montre le de fois qu'un modèle a été choisi correctement.
        '''
        score = 0
        tabScores = np.zeros((len(self.tabModels), len(self.tabModels[0])-1))
        total = 0
        for i in range(len(self.tabTests)):
            resAttendu = self.tabTests[i][0]
            for j in xrange(1, len(self.tabTests[i])):
                resTab, resMod, res = self.prediction(self.tabTests[i][j])
                if(res == resAttendu):
                    score+=1
                    if(resTab.shape[1] > 1):
                        t1 = resTab.argmax(1)
                        t2 = resTab.max(1).argmax()
                        tabScores[t2][t1[t2]]+=1
                    else:
                        t1 = resTab.argmax()
                        tabScores[t1][0]+=1
                total+=1
        score = (score/(1.0*total))*100
        return score, tabScores
    #donne le score des tests de l'objet en fonction des modèles créés avec les mêmes paramètres
    def scoreUnModele(self, numModele):
        '''
        donne le score pour un objet listeModeles en utilisant tous ses tests et un seul type de modèles ( modèles créés avec les mêmes paramètres)

        paramètres :        
        numModèle = numéro du modèle pour chaque cluster        
        
        sortie :
        score = le pourcentage de taux de bonnes classifications
        '''
        score = 0
        total = 0
        for i in range(len(self.tabTests)):
            resAttendu = self.tabTests[i][0]
            for j in xrange(1, len(self.tabTests[i])):
                resTab, res = self.predictionUnModele(self.tabTests[i][j], numModele)
                if(res == resAttendu):
                    score+=1
                total+=1
        score = (score/(1.0*total))*100
        return score



###############################################    
###############################################
#######FONCTIONS POUR GERER LES MODELES########
###############################################
###############################################

def createMatStartTransPrior(nbEtats, pett): #pett = proba etat trans au temps t
    '''    
    creer trans_mat_prior et start_prob_prior
    '''    
    sp = np.zeros(nbEtats)
    sp[0] = 1
    tp = np.zeros((nbEtats, nbEtats))
    j=0
    for i in range(nbEtats):
        tp[i,j] = pett
        tp[i,(j+1)%nbEtats] = 1-pett
        j+=1
    return sp, tp

def verif_set_transMat(model):
    '''
    modifie la transmat si pas de proba de transmission assez élevée
    utile surtout pour la génération de mouvement
    '''
    j = 0
    nbEtats = model.n_components
    aux = np.zeros((nbEtats, nbEtats))
    for i in range(nbEtats):
        if(i==nbEtats-1):
            if(model.transmat_[i,0] < 0.01):
                aux[i,0] = 0.01
                aux[i,j] = 0.99
                continue
        if (model.transmat_[i,j] > .99):
            aux[i,j] = 0.99
            aux[i,(j+1)%nbEtats] = 0.01
        else:
            aux[i,:] = model.transmat_[i,:]
        j+=1
    model._set_transmat(aux)
    
###############################################    
###############################################
#####FONCTIONS POUR LES DONNEES RELATIVES######
###############################################
###############################################
    
#change les données absolues en donnée relative
def to_relative(motion_data):
    '''
    change les données absolues en données relatives
    
    paramètres :
    motion_data = Un mouvement = tableau de vecteurs de 60 coordonnées
    
    sortie :
    relatives : même type que motion_data
    '''
    relatives = np.zeros((len(motion_data)-1, len(motion_data[0])))
    for t in range(len(relatives)):
        relatives[t] = np.subtract(motion_data[t+1], motion_data[t])
    return relatives

def to_relative_all(all_motion_data):
    '''
    change les toutes les données absolues en données relatives
    
    paramètres :
    all_motion_data = tableau à trois dimension représentant un cluster possèdant des mouvements possèdant lui même des positions
    
    sortie :
    all_relatives : même type que all_motion_data    
    '''
    all_relatives = []
    for i in range(len(all_motion_data)):
        all_relatives.append(to_relative(all_motion_data[i]))
    return all_relatives
    
###############################################    
###############################################
#####FONCTIONS POUR LES DONNEES CENTREES#######
###############################################
###############################################

def centrer_plan_squelette(motion_data):
    '''
    Centre les coordonnées au niveau du barycentre du squelette
    
    paramètres :
    motion_data = Un mouvement = tableau de vecteurs de 60 coordonnées
    
    sortie : même type que motion_data
    '''
    res = []
    dataRes = desaligner_data(motion_data)
    for i in range(len(dataRes)):
        res.append(dataRes[i] - dataRes[i].mean(0))
    return aligner_data(np.array(res))
    
def centrer_plan_squelette_all(all_motion_data):
    '''
    Centre les coordonnées au niveau du barycentre du squelette
    
    paramètres :
    all_motion_data = tableau à trois dimension représentant un cluster possèdant des mouvements possèdant lui même des positions
    
    sortie : même type que all_motion_data
    '''
    all_centrees = []
    for i in range(len(all_motion_data)):
        all_centrees.append(centrer_plan_squelette(all_motion_data[i]))
    return np.array(all_centrees)

###############################################    
###############################################
#########FONCTIONS TRIER LES DONNEES###########
###############################################
###############################################

def desaligner_data(motion_data):
    '''
    change le format des mouvement en format colone (taille (20,3))
    '''
    res = []
    for i in range(len(motion_data)):
        mouv = np.zeros((20, 3))
        for j in xrange(0, len(motion_data[i]), 3):
            mouv[j/3][0] = motion_data[i][j]
            mouv[j/3][1] = motion_data[i][j+1]
            mouv[j/3][2] = motion_data[i][j+2]
        res.append(mouv)
    return np.array(res)

#fonction qui remet format alligné (60, )
def aligner_data(motion_data):
    '''
    remet format alligné (60, )
    '''
    res = []
    for i in range(len(motion_data)):
        mouv = np.ravel(motion_data[i])
        res.append(mouv)
    return np.array(res)