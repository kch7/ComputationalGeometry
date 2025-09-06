import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random as rd
import itertools

#This function indicates if a point called d is visible from a face consisting of a,b,c
#d is visible iff the determinant is bigger than 0
def TetVolume(a,b,c,d):
    pts = [p[-3:] for p in (a, b, c, d)]   # keep only x,y,z
    mat = np.hstack((np.ones((4, 1)), np.array(pts, dtype=float)))
    return np.linalg.det(mat)
    

#This class is created for better manipulation of each face . 
class Face:
    def __init__(self,a,b,c):
        self.vertices=[a,b,c]

    def visible(self,p):
        return TetVolume(self.vertices[0],self.vertices[1],self.vertices[2],p)>0


#This plotting function has actually two modes . When mode is set to false , it plots the 3d convex hull of the incremental algorithm
#If mode is set to true, then the function plots the hull necessary for Delaunay Triangulation. In this case, z equals with x^2+y^2 for each pair of points (x,y)
def Plot(x:np.ndarray,y:np.ndarray,z:np.ndarray,hull:list,s,mode=False):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
# Scatter plot
    scatter = ax.scatter(x, y, z, c=z, cmap='viridis', marker='o')
# Vertical dashed lines
    if mode==False:
        for i in range(s):
            ax.plot([x[i], x[i]], [y[i], y[i]], [z[i], z[i]], color='blue', linestyle='--', linewidth=0.75)
    elif mode==True:
        for i in range(s):
            ax.plot([x[i], x[i]], [y[i], y[i]], [0, z[i]], color='blue', linestyle='--', linewidth=0.75)

# Convex hull faces
    poly3d = [[v for v in face.vertices] for face in hull]
    hull_collection = Poly3DCollection(poly3d, alpha=0.3, facecolor='red', edgecolor='k')
    ax.add_collection3d(hull_collection)

# Labels and titles
    fig.colorbar(scatter, ax=ax, label='Colormap for Hull Points')
    ax.set_title('Incremental 3D Convex Hull')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Z-axis')
    ax.legend(['Convex Hull'])
    plt.tight_layout()
    if(mode==False):
        savepath="./results/convex_hull_incremental_3d.png"
        plt.savefig(savepath)
    plt.show()

def border_edges(visible_faces, all_faces):
    edges=[]
    #With this computation, we define that other_faces is the list containing all faces except for the visible ones.
    other_faces=[f for f in all_faces if f not in visible_faces]
    for face in visible_faces:
        for i in range(3):
            e1=(face.vertices[i], face.vertices[(i + 1) % 3])
            shared=False
            for other_face in other_faces:
                for j in range(3):
                    e2=(other_face.vertices[j], other_face.vertices[(j+1)%3])
                    if set(e1) == set(e2):
                        shared = True
            
            if shared:
                edges.append(e1)        

    return edges

#With this function, I ensure that the orientation of the faces is consistent.
#If i find an appropriate tetrahedron, then i pass it up to the function below
#The function computes the centroid of the tetrahedron and checks if each face is visible from it
#If a face is visible, then i swap two of its vertices to change its orientation
def Normalize(a,b,c,d,faces:list):
    fixed=[]
    centroid=np.mean(np.array([a,b,c,d]),axis=0)
    for face in faces:
        if face.visible(centroid):
            face.vertices[1], face.vertices[2] = face.vertices[2], face.vertices[1]
        fixed.append(face)
    return fixed


def InitialTetrahedron(L) -> list:
    for combs in itertools.combinations(L, 4):
        a, b, c, d = combs
        if abs(TetVolume(a, b, c, d)) > 1e-6:
            faces = [Face(a, b, c), Face(a, c, d), Face(a, d, b), Face(b, d, c)]
            
            fixed=Normalize(a,b,c,d,faces)
            return fixed
    # If no valid tetrahedron is found, raise an error.
    # This should not happen with a sufficient number of points.
    raise ValueError("The points are coplanar.")


def Incremental3D(points:list)->list:
    if len(points) < 4:
        raise ValueError("At least 4 points are required to form a tetrahedron.")
    #For faster execution , I create the initial face by using only 8 points out of all . 
    hull = InitialTetrahedron(points[:8])
    #I have initialized a set to keep track of the used points in the hull.
    #This is done to avoid adding the same point multiple times.
    #The tuple is used to make the points hashable.
    #This is necessary because the points are in 3D space and we need to check visibility.
    used = set(tuple(p) for f in hull for p in f.vertices)

    for p in points:
        if tuple(p) not in used:
            visible_faces = [f for f in hull if f.visible(p)]
            if visible_faces:
                #horizon_edges are the adjacent edges between the visible_faces
                horizon_edges = border_edges(visible_faces, hull)
                #After detecting the horizon edges, i create new faces using the point p and the edges of the horizon.
                new_faces = [Face(edge[0], edge[1], p) for edge in horizon_edges]
                #Here i discard the visible faces i have found and i add the newly created ones
                hull = [f for f in hull if f not in visible_faces] + new_faces
                #After creating the new faces, I update the used set with the vertices of the new faces.
                #This ensures that the next point will not be added again if it is already part of the hull.
                used.update(tuple(v) for f in new_faces for v in f.vertices)

    return hull



if __name__ == "__main__":
    print("Incremental 3D Convex Hull")
    print("This program computes the convex hull of a set of points in 3D space using an incremental algorithm.")
    print("It will generate random points and display the convex hull in a 3D plot.")
    s=int(input("Give me the number of points for the Incremental 3D Convex Hull: "))
    num=abs(int(input("Give me the range of coordinates of the points: ")))
# Generate s random points in 3D space
    L = np.random.uniform(-num, num, (s, 3))
    points=[(x,y,z) for x,y,z in L]
    x = np.array([pt[0] for pt in points])
    y = np.array([pt[1] for pt in points])
    z = np.array([pt[2] for pt in points])
    hull=Incremental3D(points)
    #In Plot function, mode is set to False so that the 3d convex hull is plotted.
    Plot(x,y,z,hull,s,False)
    


    

