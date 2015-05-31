from Tkinter import *
import tkFileDialog

class MainView:
    
    def askdir(self):
        self.dirname = tkFileDialog.askdirectory()
        self.l1=Label(self.root, text=self.dirname).grid(row=1, column=1, sticky=W)
    def __init__(self,root,delegate):
        self.root=root

        self.l1=Label(root, text="Selectionner le dossier  ").grid(row=0, column=0, sticky=E)
        self.ButtonDir=Button(root, text='dossier', command=self.askdir)
        self.ButtonDir.grid(row=0,column=1,sticky=W)
        #self.path=Entry(root, width=40)#.grid(row=0,column=1,sticky=W)
        #self.path.insert(0, "C:/Users")
        #self.path.grid(row=0,column=1,sticky=W)
        #self.l1b=Label(root, text="                      ").grid(row=0, column=2, sticky=E)
        #self.path.pack(side=LEFT, padx=5,pady=10)
        #self.path.insert("insert","Entrez le path",0)
  	
        self.l2=Label(root, text="                Saisir les noms des modeles  ").grid(row=2, column=0, sticky=E)
        self.nModele=Entry(root,width=40)#.grid(row=1, column=1,sticky=W)
        self.nModele.insert(0, "marche")
        self.nModele.grid(row=2, column=1,sticky=W)        
        #self.nModele.pack(padx=5,pady=10)
        #self.nModele.insert(0, "Saisir les noms des modeles")
        
        self.l3=Label(root, text="Saisir le nombre d'etats  ").grid(row=3, column=0, sticky=E)
        self.netat=Entry(root, width = 4)#.grid(row=2,column=1,sticky=W)
        self.netat.insert(0, "10")
        self.netat.grid(row=3,column=1,sticky=W)
        #self.netat.pack(side=BOTTOM, padx=5,pady=10)
        #self.netat.insert(0, "Saisir nombre d'etats")
  	
        self.l4=Label(root, text="Saisir le nombre d'iterations  ").grid(row=4, column=0, sticky=E)
        self.niter=Entry(root , width = 4)#.grid(row=3, column=1,sticky=W)
        self.niter.insert(0, "300")
        self.niter.grid(row=4, column=1,sticky=W)
        #self.niter.pack(padx=5,pady=10)
        #self.niter.insert(0, "Saisir le nombre d'iterations")
        
        self.l5=Label(root, text="Saisir le nombre de fichiers  ").grid(row=5, column=0, sticky=E)
        self.nfile=Entry(root , width = 4)#.grid(row=3, column=1,sticky=W)
        self.nfile.insert(0, "200")
        self.nfile.grid(row=5, column=1,sticky=W)
        
        self.l5b=Label(root, text="Saisir le type de modele  ").grid(row=6, column=0, sticky=E)        
        
        self.radioVal=IntVar()
        self.absolu=Radiobutton(root,text="absolu",variable=self.radioVal,value=1)#.grid(row=5, column=0)
        self.absolu.select()
        self.absolu.grid(row=6, column=1, sticky=W)
        #self.absolu.pack(side=LEFT, padx=5,pady=10)
  	
        self.relatif=Radiobutton(root,text="relatif",variable=self.radioVal,value=2).grid(row=6, column=1)
        #self.relatif.pack(side=LEFT, padx=5,pady=10)
  	
        self.barycentre=Radiobutton(root,text="centre",variable=self.radioVal,value=3).grid(row=6, column=1, sticky=E)
        #self.barycentre.pack(side=LEFT, padx=5,pady=10)
        
        self.Bapprentissage=Button(root,text="apprentissage",command=delegate.apprentissage).grid(row=7, column=0, sticky=E)
        #self.Bapprentissage.pack()
        self.Bscore=Button(root,text="score",command=delegate.score).grid(row=7, column=1, sticky=W)
        #self.Bscore.pack()
        
        
        self.l6=Label(self.root, text=" ").grid(row=8, column=0)
        
        self.l7=Label(root, text="Entrez le nom du fichier a sauvegarder ").grid(row=9, column=0, sticky=E)
        self.nomFic=Entry(root, width=20)#.grid(row=0,column=1,sticky=W)
        self.nomFic.insert(0, "name")
        self.nomFic.grid(row=9,column=1,sticky=W)
        
        self.l7=Label(root, text="Entrez le nom du mouvement a generer ").grid(row=10, column=0, sticky=E)
        self.nomMouv=Entry(root, width=20)#.grid(row=0,column=1,sticky=W)
        self.nomMouv.insert(0, "marche")
        self.nomMouv.grid(row=10,column=1,sticky=W)
        
        self.l7=Label(root, text="Entrez le bombres d'images du mouvement ").grid(row=11, column=0, sticky=E)
        self.nbIma=Entry(root, width=20)#.grid(row=0,column=1,sticky=W)
        self.nbIma.insert(0, "200")
        self.nbIma.grid(row=11,column=1,sticky=W)
        
        self.Bgeneration=Button(root,text="generation",command=delegate.generation).grid(row=12, column=0, sticky=E)
        #self.Bgeneration.pack()
        
    def show(self):
        self.root.mainloop()
