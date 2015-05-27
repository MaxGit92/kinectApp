# Reconnaissance et génération de mouvements avec une Kinect 

## Notice

### Matériel
- Une Kinect de la xbox 360 (je ne possède pas celle de la xbox one pour tester si cela fonctionne)
- Un ordinateur sous système d’exploitation Windows 7/8/8.1

### Logiciels
#### Pour la Kinect
- Kinect for windows SDK v1.8 (windows 7) https://www.microsoft.com/en-us/download/details.aspx?id=40278
OU
Kinect for windows SDK v2.0 (windows 8 / 8.1) https://www.microsoft.com/en-us/download/details.aspx?id=44561
- OpenNI 2.2 SDK for windows http://openni.ru/openni-sdk/index.html
- PrimeSense Sensor KinectMod http://developkinect.com/resource/sdk-middleware-driver/openni-primesense-package-installers
- Les drivers Kinect. Ils s’installent automatiquement lors du premier branchement de la Kinect sur l’ordinateur.

#### Pour le code
- Visual studio 2013 http://www.microsoft.com/france/visual-studio/evenements/visual-studio2013.aspx
OU
Pour une installation et une utilisation plus rapide Visual studio C# 2010 http://www.01net.com/telecharger/windows/Programmation/creation/fiches/120220.html
- Une version récente de Python (exemple : 2.7.9.0) https://code.google.com/p/pythonxy/wiki/Downloads
- HMMlearn de sklearn https://github.com/hmmlearn/hmmlearn
Ce dernier logiciel requière d’avoir pip pour l’installer (vous pouvez télécharger pip sur lien suivant si vous ne l’avez pas : https://pypi.python.org/pypi/pip

### Récupération des mouvements avec la Kinect
#### Lancement du programme d'enregistrement de mouvements

Une fois que tous les logiciels précédents sont installés, nous pouvons débuter la collecte des données. Pour lancer le programme, effectuez les instructions suivantes :
- Connectez la Kinect à l'ordinateur.
- Ouvrez Visual studio.
- Cliquez sur "FILE"->"Open"->"Project/Solution".
- Sélectionnez le fichier "SkeletonBasics-WPF" et ouvrez le.
- Affichez le fichier "MainWindow.xaml.cs" s'il ne s'afficher pas automatiquement.
- Modifiez les deux paramètres "nameFile" et "path" (situés en début de fichier). Le programme enregistrera le mouvement sous le nom de "nameFile.txt" (ne pas rajouter l'extention .txt) à l'endroit du path.
- Il ne reste plus qu'à exécuter le code (appuyez sur la touche f5).

Une fois le programme exécuté, il va afficher une fenêtre noire qui représente ce que voit la Kinect. Si la Kinect est bien installée, vous pouvez vous placer face à elle jusqu'à ce qu'elle vous détecte et effectuer le mouvement que vous souhaitez. Pour terminer l'exécution il suffit de fermer la fenêtre. A la fin de l'exécution, le programme enregistre le fichier à l'endroit que vous lui avez indiqué.

#### Aspect machine learning
Pour que les données capturées servent dans l’apprentissage et la génération de mouvement il est recommandé de créer deux dossiers. Un dossier où seront stockées les données d’apprentissages, celles que vous voulez faire apprendre au programme, et un deuxième où seront stockées les données de tests, celle que vous voulez analyser lors de la reconnaissance de mouvement.
Il doit y avoir beaucoup de mouvements pour que l’apprentissage soit intéressant, de ce fait pour faciliter la lecture des données nous utilisons la convention suivante : Tous les mouvements, même s’ils sont de clusters différents que ça soit en test ou en apprentissage, sont stockés dans un même dossier, on les nommera ensuite par le nom de leur classe suivit de leur numéro d’arriver dans le cluster.
Exemple : Nous voulons créer un cluster contenant des sauts et un autre contenant des marches. On commence par enregistrer un fichier nommé « saut1 » puis un second « saut2 » et ainsi de suite. De même, on enregistre un fichier « marche1 » puis un autre « marche2 » etc. Le tout étant sauvegardé dans le même dossier (que ça soit le dossier de test ou d'apprentissage).
Si vous ne voulez pas suivre cette convention, il suffit de modifier ou de recréer la fonction de lecture des fichiers dans le fichier « classSkeleton.py » ainsi que les fonctions de calcul des scores qui considèrent que les modèles d'apprentissage et les données de test ont la même étiquette (même nom de cluster pour comparer si le résultat obtenu est juste).

### Utilisation de l'application
L'application se décompose en 3 fichiers :
- classSkeleton.py : le fichier principal contenant les classes et des fonctions pour l'apprentissage.
- generationFunc.py : regroupe les méthodes pour générer des mouvements à partir des modèles appris.
- anime.py : permet de visualiser un mouvement enregistré.

La classe principale est listeModeles() située dans le fichier classSkeleton.py. Elle permet de créer des objets qui construisent les modèles d'apprentissage sur les données de mouvements. Les deux attributs de cette classe sont tabModels et tabTests, deux tables de hachage contenant respectivement sur chaque ligne les modèles appris et les données de tests (mouvements) des différents clusters. Le premier élément d’une ligne est une chaîne de caractères qui correspond au nom du mouvement. Cet élément permettra à la fonction de hachage d’ajouter en queue un modèle (resp. un test) si des variables pré-existent déjà, ou bien de créer une nouvelle ligne et donc un nouveau cluster. Deux modèles d'un même cluster peuvent se différentier par rapport aux paramètres d'apprentissage notamment le nombre d'états cachés qu'ils possèdent.

#### Importer les fichiers
Il suffit d'écrire les lignes de code suivantes :
	from classSkeleton import *
from generationFunc import *
from anim import *

#### Apprentissage et reconnaissance
Il faut d'abord commencer par initialiser certaines variables de la méthode d'apprentissage. "nameModels" est un tableau contenant les noms des clusters que l'on souhaite apprendre. Comme expliqué dans la partie "Aspect machine learning", il faut que ces noms correspondent au nom des fichiers de l'emplacement spécifié. Enfin, le paramètre "t" de la fonction définit le traitement des données. Il peut prendre trois valeurs : "absolu" (on ne change pas les coordonnées), "relatif" (les coordonnées sont transformées en vecteurs vitesse) et "barycentre" (les coordonnées sont centrées sur le squelette). exemple :
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

#### Génération
De manière équivalente on définit les paramètres des méthodes de génération. A noter que la génération relative nécessite une première image que l'on peut récupérer via la moyenne d'un état du modèle centré. La méthode "main(path)" sert à afficher un mouvement. Exemple :
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
