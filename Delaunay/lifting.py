import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ConvexHull import Incremental3D, Plot
import numpy as np
import matplotlib.pyplot as plt
import math


def TriangulationPlot(ax,triangles:list,points:list):
    for triangle in triangles:
        xs, ys = zip(*triangle)
        ax.plot(xs, ys)
    xf,yf,zf=zip(*points)
    ax.scatter(xf,yf,c='red',s=15)
    ax.set_title("Delaunay Triangulation")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.axis('equal')
    ax.grid(True)

def DelaunayTriangulation(x:list,y:list,hull:list):
    triangles=[]
    #In this function , I break up each face of the hull, and i convert the coordinates of each face from tuple to np.ndarray.
    for face in hull:
        v0=np.array(face.vertices[0],dtype=float)
        v1=np.array(face.vertices[1],dtype=float)
        v2=np.array(face.vertices[2],dtype=float)
        #Here, we compute the cross product between the differences of the vertices.
        normal = np.cross(v1 - v0, v2 - v0)
        #If the z-component is negative, then a Delaunay Triangle has been found.
        if normal[2]<0:
            triangle_2d=[(v[0],v[1]) for v in face.vertices]
            #In the line below , i enclose the triangle by appending the first vertex to the result.
            triangle_2d.append(triangle_2d[0])
            triangles.append(triangle_2d)

    return triangles
    
    
if __name__ =="__main__":
    print("Delaunay Triangulation")
    print("This program prints the Delaunay Triangulation of a set of points by creating at first their 3D-Convex Hull.")
    s=int(input("Please, give me the number of points used in Delaunay Triangulation : "))
    L = np.random.uniform(-250, 250, (s, 2))
    points=[(x,y,x**2+y**2) for x,y in L]
    x = np.array([pt[0] for pt in points])
    y = np.array([pt[1] for pt in points])
    fig,ax=plt.subplots(figsize=(12,8))
    hull=Incremental3D(points)
    Triangulation=DelaunayTriangulation(x,y,hull)
    TriangulationPlot(ax, Triangulation,points)       # Plot Delaunay Triangulation
    plt.tight_layout()
    plt.show()