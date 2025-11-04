import numpy as np
import matplotlib.pyplot as plt
from lifting import DelaunayTriangulation, TriangulationPlot
from BowyerWatson import BowyerWatson, BowyerPlot
import os
import time
import sys
import pandas as pd
sys.path.append('..')
from ConvexHull import Incremental3D


if __name__ =="__main__":
    results=[]
    os.makedirs("delaunay_performance", exist_ok=True)
    print("Performance Comparison between Bowyer-Watson and Lifting Method")
    a=int(input("Please enter the minimum range of coordinates : "))
    b=int(input("Please enter the maximum range of coordinates : "))
    c=int(input("Please enter the minimum number of points : "))
    d=int(input("Please enter the maximum number of points : "))
    f=int(input("Please enter the step size for number of points : "))
    for n in range(c,d+f,f):
        fig,(ax,ax1)=plt.subplots(1,2,figsize=(16,8))
        L= np.random.uniform(a, b, (n, 2))
        L = np.round(L, decimals=10)
        points=[(x,y,x**2+y**2) for x,y in L]
        points = sorted(points, key=lambda p: (p[0], p[1],p[2]))
        x = np.array([pt[0] for pt in points])
        y = np.array([pt[1] for pt in points])
        Points = [(pt[0], pt[1]) for pt in points]
        t0=time.time()
        hull=Incremental3D(points)
        Triangulation=DelaunayTriangulation(x,y,hull)
        t1=time.time()
        TriangulationPlot(ax,Triangulation,points)
        diff_lifting=t1-t0
        t0=time.time()
        BowyerWatsonTriangulation=BowyerWatson(Points)
        BowyerPlot(ax1,BowyerWatsonTriangulation,Points)
        savepath="./delaunay_performance/delaunay_comparison_"+str(n)+".png"
        plt.savefig(savepath)
        t1=time.time()
        diff_bowyer=t1-t0
        results.append([n,diff_lifting,diff_bowyer])

    results=pd.DataFrame(results,columns=["Points","LiftingMethodSeconds","BowyerWatsonSeconds"])
    results.to_csv("delaunay_performance.csv",index=False)
    os.execlp("python3", "python3", "plot.py")