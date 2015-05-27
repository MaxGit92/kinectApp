# Reconnaissance et g�n�ration de mouvements avec une Kinect 

## Notice

### Mat�riel
- Une Kinect de la xbox 360 (je ne poss�de pas celle de la xbox one pour tester si cela fonctionne)
- Un ordinateur sous syst�me d�exploitation Windows 7/8/8.1

### Logiciels
#### Pour la Kinect
- Kinect for windows SDK v1.8 (windows 7) https://www.microsoft.com/en-us/download/details.aspx?id=40278
OU
Kinect for windows SDK v2.0 (windows 8 / 8.1) https://www.microsoft.com/en-us/download/details.aspx?id=44561
- OpenNI 2.2 SDK for windows http://openni.ru/openni-sdk/index.html
- PrimeSense Sensor KinectMod http://developkinect.com/resource/sdk-middleware-driver/openni-primesense-package-installers
- Les drivers Kinect. Ils s�installent automatiquement lors du premier branchement de la Kinect sur l�ordinateur.

#### Pour le code
- Visual studio 2013 http://www.microsoft.com/france/visual-studio/evenements/visual-studio2013.aspx
OU
Pour une installation et une utilisation plus rapide Visual studio C# 2010 http://www.01net.com/telecharger/windows/Programmation/creation/fiches/120220.html
- Une version r�cente de Python (exemple : 2.7.9.0) https://code.google.com/p/pythonxy/wiki/Downloads
- HMMlearn de sklearn https://github.com/hmmlearn/hmmlearn
Ce dernier logiciel requi�re d�avoir pip pour l�installer (vous pouvez t�l�charger pip sur lien suivant si vous ne l�avez pas : https://pypi.python.org/pypi/pip

### R�cup�ration des mouvements avec la Kinect
#### Lancement du programme d'enregistrement de mouvements

Une fois que tous les logiciels pr�c�dents sont install�s, nous pouvons d�buter la collecte des donn�es. Pour lancer le programme, effectuez les instructions suivantes :
- Connectez la Kinect � l'ordinateur.
- Ouvrez Visual studio.
- Cliquez sur "FILE"->"Open"->"Project/Solution".
- S�lectionnez le fichier "SkeletonBasics-WPF" et ouvrez le.
- Affichez le fichier "MainWindow.xaml.cs" s'il ne s'afficher pas automatiquement.
- Modifiez les deux param�tres "nameFile" et "path" (situ�s en d�but de fichier). Le programme enregistrera le mouvement sous le nom de "nameFile.txt" (ne pas rajouter l'extention .txt) � l'endroit du path.
- Il ne reste plus qu'� ex�cuter le code (appuyez sur la touche f5).

Une fois le programme ex�cut�, il va afficher une fen�tre noire qui repr�sente ce que voit la Kinect. Si la Kinect est bien install�e, vous pouvez vous placer face � elle jusqu'� ce qu'elle vous d�tecte et effectuer le mouvement que vous souhaitez. Pour terminer l'ex�cution il suffit de fermer la fen�tre. A la fin de l'ex�cution, le programme enregistre le fichier � l'endroit que vous lui avez indiqu�.

#### Aspect machine learning
Pour que les donn�es captur�es servent dans l�apprentissage et la g�n�ration de mouvement il est recommand� de cr�er deux dossiers. Un dossier o� seront stock�es les donn�es d�apprentissages, celles que vous voulez faire apprendre au programme, et un deuxi�me o� seront stock�es les donn�es de tests, celle que vous voulez analyser lors de la reconnaissance de mouvement.
Il doit y avoir beaucoup de mouvements pour que l�apprentissage soit int�ressant, de ce fait pour faciliter la lecture des donn�es nous utilisons la convention suivante : Tous les mouvements, m�me s�ils sont de clusters diff�rents que �a soit en test ou en apprentissage, sont stock�s dans un m�me dossier, on les nommera ensuite par le nom de leur classe suivit de leur num�ro d�arriver dans le cluster.
Exemple : Nous voulons cr�er un cluster contenant des sauts et un autre contenant des marches. On commence par enregistrer un fichier nomm� � saut1 � puis un second � saut2 � et ainsi de suite. De m�me, on enregistre un fichier � marche1 � puis un autre � marche2 � etc. Le tout �tant sauvegard� dans le m�me dossier (que �a soit le dossier de test ou d'apprentissage).
Si vous ne voulez pas suivre cette convention, il suffit de modifier ou de recr�er la fonction de lecture des fichiers dans le fichier � classSkeleton.py � ainsi que les fonctions de calcul des scores qui consid�rent que les mod�les d'apprentissage et les donn�es de test ont la m�me �tiquette (m�me nom de cluster pour comparer si le r�sultat obtenu est juste).

### Utilisation de l'application
L'application se d�compose en 3 fichiers :
- classSkeleton.py : le fichier principal contenant les classes et des fonctions pour l'apprentissage.
- generationFunc.py : regroupe les m�thodes pour g�n�rer des mouvements � partir des mod�les appris.
- anime.py : permet de visualiser un mouvement enregistr�.

La classe principale est listeModeles() situ�e dans le fichier classSkeleton.py. Elle permet de cr�er des objets qui construisent les mod�les d'apprentissage sur les donn�es de mouvements. Les deux attributs de cette classe sont tabModels et tabTests, deux tables de hachage contenant respectivement sur chaque ligne les mod�les appris et les donn�es de tests (mouvements) des diff�rents clusters. Le premier �l�ment d�une ligne est une cha�ne de caract�res qui correspond au nom du mouvement. Cet �l�ment permettra � la fonction de hachage d�ajouter en queue un mod�le (resp. un test) si des variables pr�-existent d�j�, ou bien de cr�er une nouvelle ligne et donc un nouveau cluster. Deux mod�les d'un m�me cluster peuvent se diff�rentier par rapport aux param�tres d'apprentissage notamment le nombre d'�tats cach�s qu'ils poss�dent.

#### Importer les fichiers
Il suffit d'�crire les lignes de code suivantes :
	from classSkeleton import *
from generationFunc import *
from anim import *

#### Apprentissage et reconnaissance
Il faut d'abord commencer par initialiser certaines variables de la m�thode d'apprentissage. "nameModels" est un tableau contenant les noms des clusters que l'on souhaite apprendre. Comme expliqu� dans la partie "Aspect machine learning", il faut que ces noms correspondent au nom des fichiers de l'emplacement sp�cifi�. Enfin, le param�tre "t" de la fonction d�finit le traitement des donn�es. Il peut prendre trois valeurs : "absolu" (on ne change pas les coordonn�es), "relatif" (les coordonn�es sont transform�es en vecteurs vitesse) et "barycentre" (les coordonn�es sont centr�es sur le squelette). exemple :
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

#### G�n�ration
De mani�re �quivalente on d�finit les param�tres des m�thodes de g�n�ration. A noter que la g�n�ration relative n�cessite une premi�re image que l'on peut r�cup�rer via la moyenne d'un �tat du mod�le centr�. La m�thode "main(path)" sert � afficher un mouvement. Exemple :
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
