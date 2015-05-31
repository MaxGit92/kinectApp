from classSkeleton import *
from generationFunc import *
from anim import *

#definition des variables d'apprentissage
pathMouvements = "C:/Users/mouvements"
nbEtats = 10 #nombre d'etats du hmm
nameModels = ["saut", "marche", "course"] #nom des models crees
n_iter = 300 #nombre d'iteration de l'algorithme

#apprentissage des modeles avec les donnees relatives
listeModelesRelatifs = listeModeles()
listeModelesRelatifs.genererModels(pathMouvements+"/train", nameModels, nbEtats=nbEtats, n_iter=n_iter, t="relatif")
listeModelesRelatifs.genererTests(pathMouvements+"/test", nameModels, t="relatif")

#apprentissage des modeles avec les donnees centrees
listeModelesCentres = listeModeles()
listeModelesCentres.genererModels(pathMouvements+"/train", nameModels, nbEtats=nbEtats, n_iter=n_iter, t="barycentre")
listeModelesCentres.genererTests(pathMouvements+"/test", nameModels, t="barycentre")

#calcul des scores de predictions
scoreRel, tabScoreRel = listeModelesRelatifs.score()
scoreCen, tabScoreCen = listeModelesCentres.score()
print "score reletif : " + str(scoreRel) + ", score centre : " + str(scoreCen)

#generation de mouvements
pathMouvementsGeneres = "C:/Users/mouvementsGeneres"
#parametres pour generer le mouvement relatif
modeleRelatifSaut = listeModelesRelatifs.getModel("saut")[1]
nbImaMouv = 200
imageDepart = listeModelesCentres.getModel("saut")[1].means_[0] #la prmiere image pour generer un mouvement relatif
#parametres pour generer le mouvement relatif
modeleCentreCourse = listeModelesCentres.getModel("course")[1]
nbTranslations = 20
fps = 10 # 20 * 10 = 200 mouvements
nameMoveRel = "sautGenere"
nameMoveCen = "courseGenere"

mouvRel = generate_move_velocity_varition(modeleRelatifSaut, nbImaMouv, imageDepart, pathMouvementsGeneres, nameMoveRel)
mouvCen = generate_move_translation(modeleCentreCourse, nbTranslations, fps, pathMouvementsGeneres, nameMoveCen)

main(pathMouvementsGeneres+"/"+nameMoveRel)
main(pathMouvementsGeneres+"/"+nameMoveCen)