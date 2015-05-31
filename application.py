from Tkinter import *
from mainView import MainView
from classSkeleton import *
from generationFunc import *
import anim
import re
import tkMessageBox

def main():
    app = Application()
    app.run()

class Application:
    def __init__(self):

        self.root=Tk()
        self.root.title("Untitled")
        self.listeModelesAbsolus=None
        self.listeModelesRelatifs=None
        self.listeModelesCentres=None
        self.modAbsExist=False
        self.modRelExist=False
        self.modCenExist=False
        self.resultApprentissage=None
        self.main_view=MainView(self.root,self)
        
    def apprentissage(self):
        path = re.sub(r'\\', '/', self.main_view.dirname)
        netat=int(self.main_view.netat.get())
        nmodele=re.sub(r'\ \s','',self.main_view.nModele.get()).split(',')
        for i in range(len(nmodele)):
            nmodele[i] = nmodele[i].lstrip()
        niter=int(self.main_view.niter.get())
        nfile=int(self.main_view.nfile.get())
        t=int(self.main_view.radioVal.get())
        if(t == 1):
            self.listeModelesAbsolus=listeModeles()
            self.listeModelesAbsolus.genererModels(path+"/train", nmodele, nbfiles=nfile, nbEtats=netat, n_iter=niter, t="absolu")
            self.listeModelesAbsolus.genererTests(path+"/test", nmodele, nbfiles=nfile, t="absolu")     
            self.modAbsExist=True
        if(t == 2):
            self.listeModelesRelatifs=listeModeles()
            self.listeModelesRelatifs.genererModels(path+"/train", nmodele, nbfiles=nfile, nbEtats=netat, n_iter=niter, t="relatif")
            self.listeModelesRelatifs.genererTests(path+"/test", nmodele, nbfiles=nfile, t="relatif")
            self.modRelExist=True
        if(t == 3):
            self.listeModelesCentres=listeModeles()
            self.listeModelesCentres.genererModels(path+"/train", nmodele, nbfiles=nfile, nbEtats=netat, n_iter=niter, t="barycentre")
            self.listeModelesCentres.genererTests(path+"/test", nmodele, nbfiles=nfile, t="barycentre")
            self.modCenExist=True
        
    def score(self):
        t=int(self.main_view.radioVal.get())
        if(t == 1):
            if(self.modAbsExist):
                scoreAbs, tabScoreAbs = self.listeModelesAbsolus.score()
                self.lT=Label(self.root, text="  Le taux de bonnes classifications est de : " + str((int(scoreAbs)*100)/(1.0*100)) + "%").grid(row=8, column=1, sticky=W)
            else:
                tkMessageBox.showinfo("Information", "Vous n'avez pas encore appris de modele absolu")
        if(t == 2):
            if(self.modRelExist):
                scoreRel, tabScoreRel = self.listeModelesRelatifs.score()
                self.lT=Label(self.root, text="  Le taux de bonnes classifications est de : " + str((int(scoreRel)*100)/(1.0*100)) + "%").grid(row=8, column=1, sticky=W)
            else:
                tkMessageBox.showinfo("Information", "Vous n'avez pas encore appris de modele relatif")
        if(t == 3):
            if(self.modCenExist):
                scoreCen, tabScoreCen = self.listeModelesCentres.score()
                self.lT=Label(self.root, text="  Le taux de bonnes classifications est de : " + str((int(scoreCen)*100)/(1.0*100)) + "%").grid(row=8, column=1, sticky=W)
            else:
                tkMessageBox.showinfo("Information", "Vous n'avez pas encore appris de modele Centre")
        
    def generation(self):
        path = re.sub(r'\\', '/', self.main_view.dirname)
        t=int(self.main_view.radioVal.get())
        nomFic=(self.main_view.nomFic.get()).strip()
        nomMouv=(self.main_view.nomMouv.get()).strip()
        nbIma=int(self.main_view.nbIma.get())
        if(t == 1):
            if(self.modAbsExist):
                fps = 10
                nbTranslations = nbIma/fps
                if(nbTranslations == 0): nbTranslations = 1
                mouv = generate_move_translation(self.listeModelesAbsolus.getModel(nomMouv)[1], nbTranslations, fps, path, nomFic)
                if(nomFic[-4:] != ".txt"):
                    nomFic+=".txt"                
                anim.main(path+"/"+nomFic)
            else:
                tkMessageBox.showinfo("Information", "Vous n'avez pas encore appris de modele absolu")
        if(t == 2):
            if(self.modRelExist == False):
                tkMessageBox.showinfo("Information", "Vous n'avez pas encore appris de modele relatif")
            elif(self.modCenExist == False):
                tkMessageBox.showinfo("Information", "Vous avez besoin de creer le modele centre en plus du modele relatif pour pouvoir generer un mouvement")
            else:
                mouv = generate_move_velocity_varition(self.listeModelesRelatifs.getModel(nomMouv)[1], nbIma, self.listeModelesCentres.getModel(nomMouv)[1].means_[1], path, nomFic)
                if(nomFic[-4:] != ".txt"):
                    nomFic+=".txt"                
                anim.main(path+"/"+nomFic)
        if(t == 3):
            if(self.modCenExist):
                fps = 10
                nbTranslations = nbIma/fps
                if(nbTranslations == 0): nbTranslations = 1
                mouv = generate_move_translation(self.listeModelesCentres.getModel(nomMouv)[1], nbTranslations, fps, path, nomFic)
                if(nomFic[-4:] != ".txt"):
                    nomFic+=".txt"                
                anim.main(path+"/"+nomFic)
            else:
                tkMessageBox.showinfo("Information", "Vous n'avez pas encore appris de modele Centre")
	
    def run(self):
        self.main_view.show()
        
if __name__ =="__main__":
    main()
