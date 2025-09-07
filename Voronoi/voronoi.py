import numpy as np
import math
import itertools
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random
from matplotlib.colors import ListedColormap

#I create the Voronoi Diagram by using lifted points. I have n pairs of points (x,y) in 2D. I lift them to 3D by using the formula (x,y,x^2+y^2).
#Then, I create the tangent planes for each lifted point. The equation of the tangent plane at point (x0,y0,z0) is given by z = 2*x0*(x-x0) + 2*y0*(y-y0) + z0
#This simplifies to z = 2*x0*x + 2*y0*y - (x0^2 + y0^2)
#I compute the value of each tangent plane at each point of a grid in the xy-plane. The Voronoi region for each point corresponds to the area where
#its tangent plane is the highest among all tangent planes. The edges of the Voronoi diagram are found where the maximum tangent plane changes from one point to another.
# Finally, I plot the Voronoi diagram by coloring the regions and drawing the edges.


def CreateVoronoi(points:list,x,y,z):    
    tangents= np.array([[2*pt[0],2*pt[1],-((pt[0]*pt[0])+(pt[1]*pt[1]))] for pt in points])
    xx,yy=np.meshgrid(np.linspace(min(x)-10,max(x)+10,300),np.linspace(min(y)-10,max(y)+10,300))
    tangvals=np.array([a*xx+b*yy+c for (a,b,c) in tangents])
    maxima=np.argmax(tangvals,axis=0)
    edges=np.zeros_like(maxima,dtype=bool)
    edges[1:, :] |= maxima[1:,:] != maxima[:-1, :]
    edges[:, 1:] |= maxima[:,1:] != maxima[:, :-1]

    return edges,maxima,xx,yy

def PlotVoronoi(ax,edges,maxima,xx,yy,x,y,points:list,s):
    colors = plt.cm.tab20(np.linspace(0, 1, s))
    cmap = ListedColormap(colors)

    ax.imshow(maxima, extent=(min(x)-10, max(x)+10, min(y)-10, max(y)+10),
          cmap=cmap, origin='lower', alpha=0.4)
    ax.contour(xx, yy, edges, levels=[0.2], colors='k', linewidths=1.5)
    ax.scatter(x, y, c='blue', s=20, edgecolors='k')

    for i, (xi, yi) in enumerate(points):
        ax.text(xi+0.05, yi+0.05, f"p{i+1}", fontsize=10, weight='bold',color='black')

    ax.set_aspect('equal')
    ax.set_title("Voronoi Diagram via Tangent Planes", fontsize=12)
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")


if __name__=="__main__":
    print("Voronoi Diagram")
    print("This program prints the Voronoi Diagram of a set of points by lifting at first the given 2D points to 3D.")
    s=int(input("Please, give me the number of points used in Voronoi Diagram : "))
    a=int(input("Please, give me the first value for the coordinate : "))
    b=int(input("Please, give me the second value for the coordinate : "))
    L = np.random.randint(a, b, (s, 2))
    points=[(x,y,x**2+y**2) for x,y in L]   
    xf,yf,zf=zip(*points)
    Points = [(pt[0], pt[1]) for pt in points]
    fig,ax1=plt.subplots(figsize=(8,8))
    edges,maxima,xx,yy=CreateVoronoi(Points,xf,yf,zf)
    PlotVoronoi(ax1,edges,maxima,xx,yy,xf,yf,Points,s)
    plt.tight_layout()
    plt.show()