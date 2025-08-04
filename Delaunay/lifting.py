import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ConvexHull import Incremental3D, Plot
import numpy as np
import matplotlib.pyplot as plt
import math


def TriangulationPlot(x:list,y:list,triangles:list):
    plt.figure(figsize=(6, 6))
    #plt.scatter(x, y, color='blue')    
    for triangle in triangles:
        xs,ys=zip(*triangle)
        plt.plot(xs,ys)
    plt.title("Delaunay Triangulation")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.axis('equal')
    plt.grid(True)
    plt.show()

def DelaunayTriangulation(x:list,y:list,hull:list):
    triangles=[]
    #In this function , I break up each face of the hull, and i convert the coordinates of each face from tuple to np.ndarray.
    for face in hull:
        v0=np.array(face.vertices[0])
        v1=np.array(face.vertices[1])
        v2=np.array(face.vertices[2])
        #Here, we compute the cross product between 
        normal=np.cross(v2-v0,v1-v0)
        #If the z-component is negative, then a Delaunay Triangle has been found.
        if normal[2]<0:
            triangle_2d=[(v[0],v[1]) for v in face.vertices]
            #In the line below , i enclose the triangle by appending the first vertex to the result.
            triangle_2d.append(triangle_2d[0])
            triangles.append(triangle_2d)

    return triangles
    
        



if __name__ =="__main__":
    print("Delaunay Triangulation")
    print("This program prints the Delaunay Triangulation of a set of points by creating at first their Delaunay Triangulation.")
    s=int(input("Please, give me the number of points used in Delaunay Triangulation : "))
    L = np.random.uniform(-200, 200, (s, 3))
    points=[(x,y,z) for x,y,z in L]    
    x = np.array([pt[0] for pt in points])
    y = np.array([pt[1] for pt in points])
    z = np.array([pt[0]**2 + pt[1]**2 for pt in points])
    hull=Incremental3D(points)
    Triangulation=DelaunayTriangulation(x,y,hull)
    TriangulationPlot(x,y,Triangulation)