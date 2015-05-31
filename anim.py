import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import time
from classSkeleton import *

def read_file2(fn):
    with open(fn,'rb') as f:
        res=[]
        cur = []
        for l in f:
            line = l.replace(",",".").split(" ")
            if len(line)<2:
                if len(cur)>0:
                    res.append(cur)
                cur = []
            else:
                cur+=[float(x) for x in line]
    return np.array(res)

points_list=["Hip center","Spine","Shoulder center","Head","Shoulder left","Elbow left",\
            "Wristle left","Hand left","Shoulder right","Elbow right","Wristle right",\
            "Hand right","Hip left","Knee left","Ankle left","Foot left","Hip right",\
            "Knee right","Ankle right","Foot right"]

dic_points=dict(zip(points_list,range(len(points_list))))
connections=[
                ["Hip center","Hip right"],["Hip center","Hip left"],\
                ["Hip right","Knee right"], ["Hip left", "Knee left"],\
                ["Knee right","Ankle right"],["Knee left","Ankle left"],\
                ["Ankle right","Foot right"],["Ankle left","Foot left"],\
                ["Hip center", "Spine"],["Spine","Shoulder center"],["Shoulder center","Head"],\
                ["Shoulder center","Shoulder right"],["Shoulder center","Shoulder left"],\
                ["Shoulder right","Elbow right"],["Shoulder left","Elbow left"],\
                ["Elbow right","Wristle right"],["Elbow left","Wristle left"],\
                ["Wristle right","Hand right"],["Wristle left","Hand left"]\
            ]


def get_xyzq(name,tab):
    return tab[dic_points[name]*4:dic_points[name]*4+4]

def get_lines(i,tab):
    resx,resy,resz=[],[],[]
    for c in connections:
        x1,y1,z1,q1 = get_xyzq(c[0],tab[i,:])
        x2,y2,z2,q2 = get_xyzq(c[1],tab[i,:])
        resx.append([x1,x2])
        resy.append([z1,z2])
        resz.append([y1,y2])
    return resx,resy,resz

def get_points(i,tab):
    resx,resy,resz=[],[],[]
    for c in points_list:
        x1,y1,z1,q1 = get_xyzq(c,tab[i,:])
        resx.append(x1)
        resy.append(z1)
        resz.append(y1)
    return resx,resy,resz

def update(i, tab, points, lines) :
    xp,yp,zp=get_points(i,tab)
    xl,yl,zl =get_lines(i,tab)
    for line,x,y,z in zip(lines,xl,yl,zl) :
        line.set_data(x,y)
        line.set_3d_properties(z)
    for pt,x,y,z in zip(points,xp,yp,zp):
        pt.set_data(x,y)
        pt.set_3d_properties(z)

def desaligner_data2(motion_data):
    '''
    change le format des mouvement en format colone (taille (20,4))
    '''
    res = []
    for i in range(len(motion_data)):
        mouv = np.zeros((20, 4))
        for j in xrange(0, len(motion_data[i]), 4):
            mouv[j/4][0] = motion_data[i][j]
            mouv[j/4][1] = motion_data[i][j+1]
            mouv[j/4][2] = motion_data[i][j+2]
            mouv[j/4][3] = motion_data[i][j+3]
        res.append(mouv)
    return np.array(res)
    
plt.ion()

fps=75.

def main(fn):
    plt.ion()    
    tab=read_file2(fn)
    tabAux = desaligner_data2(tab)
    fig = plt.figure()
    ax = p3.Axes3D(fig)
    
    ax.set_xlim(tabAux[:,:,0].min(),tabAux[:,:,0].max())
    ax.set_ylim(tabAux[:,:,2].min(),tabAux[:,:,2].max())
    ax.set_zlim(tabAux[:,:,1].min(),tabAux[:,:,1].max())

    plt.show()
    #x,y,z=get_points(i,tab)
    x,y,z=get_points(0,tab)
    #ax.view_init(125, -60)
    
    points=[ax.plot(x,z,y,'o')[0] for i in range(len(x))]
    x,y,z=get_lines(0,tab)
    lines =[ax.plot(x[i],z[i],y[i],)[0] for i in range(len(x))]
    '''
    for i in range(1,tab.shape[0]):
        tab[i,:]=tab[i-1,:]+np.random.random(tab.shape[1])/100.
    '''
    #line_ani = animation.FuncAnimation(fig, update, 25, fargs=(tab,points, lines),interval=50, blit=False)
    for i in range(tab.shape[0]):
        update(i,tab,points,lines)
        plt.draw()
        time.sleep(1./fps)

fn=("C:/Users/Manence/Desktop/pldac/data/mouvementsGeneres/newMove.txt")