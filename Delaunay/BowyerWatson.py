import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.tri as mtri
import itertools

def same(p1, p2, eps=1e-9):
    return abs(p1[0]-p2[0]) < eps and abs(p1[1]-p2[1]) < eps

def canonical_triangle(tri, eps=1e-8):
    """Return a triangle as sorted rounded vertices for consistent comparison."""
    verts = sorted([(round(v[0], 8), round(v[1], 8)) for v in tri])
    return tuple(verts)


def BowyerPlot(ax, triangles: list, points: list): 
    xs = [p[0] for p in points] 
    ys = [p[1] for p in points] 
    ax.scatter(xs, ys, color='blue', s=50, label='Points') 
    for tri in triangles: 
        tx = [v[0] for v in tri.vertices] + [tri.vertices[0][0]] 
        ty = [v[1] for v in tri.vertices] + [tri.vertices[0][1]] 
        ax.plot(tx, ty, color='red', linewidth=1.5) 
    ax.set_title("Delaunay Triangulation (Bowyer–Watson)") 
    ax.legend() 
    ax.set_aspect('equal') 
    ax.grid(True)


class Triangle():
    def __init__(self,a,b,c):
        self.vertices=[a,b,c]
        ax, ay = a 
        bx, by = b 
        cx, cy = c
        if (bx - ax)*(cy - ay) - (by - ay)*(cx - ax) < 0:
            self.vertices = [a, c, b]

    def CircumCircle(self,point):
        ax,ay=self.vertices[0]
        bx,by=self.vertices[1]
        cx,cy=self.vertices[2]
        dx,dy=point
        mat = np.array([
            [ax - dx, ay - dy, (ax - dx)**2 + (ay - dy)**2],
            [bx - dx, by - dy, (bx - dx)**2 + (by - dy)**2],
            [cx - dx, cy - dy, (cx - dx)**2 + (cy - dy)**2]
        ])

        det = np.linalg.det(mat)
        return det > 0

def LawsonFlip(triangles):
    changed = True
    while changed:
        changed = False
        # Build edge → triangles map
        edge_to_tri = {}
        for t in triangles:
            verts = t.vertices
            for i in range(3):
                a, b = verts[i], verts[(i + 1) % 3]
                e = tuple(sorted([a, b]))
                edge_to_tri.setdefault(e, []).append(t)

        # Check all edges shared by two triangles
        for edge, tris in list(edge_to_tri.items()):
            if len(tris) != 2:
                continue  # boundary edge
            t1, t2 = tris

            # find opposite vertices (those not on the shared edge)
            opp1 = [v for v in t1.vertices if v not in edge][0]
            opp2 = [v for v in t2.vertices if v not in edge][0]
            a, b = edge

            # Check Delaunay condition using your CircumCircle()
            if t1.CircumCircle(opp2) or t2.CircumCircle(opp1):
                # Flip the shared edge
                triangles.remove(t1)
                triangles.remove(t2)
                new1 = Triangle(opp1, a, opp2)
                new2 = Triangle(opp1, opp2, b)
                triangles.append(new1)
                triangles.append(new2)
                changed = True
                break  # restart search (safe)
    return triangles



def BowyerWatson(points):
    xs=[points[i][0] for i in range(len(points))]
    ys=[points[i][1] for i in range(len(points))]
    min_xs,min_ys=min(xs),min(ys)
    max_xs,max_ys=max(xs),max(ys)   
    range_x=max_xs-min_xs
    range_y=max_ys-min_ys
    max_range = max(range_x, range_y)
    
    # Calculate the center point of the range
    center_x = (min_xs + max_xs) / 2
    center_y = (min_ys + max_ys) / 2
    
    # Calculate the vertices of the super-triangle
    p1 = (center_x - 20 * max_range, center_y - max_range)
    p2 = (center_x, center_y + 20 * max_range)
    p3 = (center_x + 20 * max_range, center_y - max_range)
    superTriangle=Triangle(p1,p2,p3)
    triangles=[superTriangle]
    for point in points:
        badTriangles=[triangle for triangle in triangles if triangle.CircumCircle(point)]
        boundaryEdges=[]
        for triangle in badTriangles:
            for i in range(3):
                a,b=triangle.vertices[i],triangle.vertices[(i+1)%3]
                edge=tuple(sorted([a,b]))
                if edge not in boundaryEdges:
                    boundaryEdges.append(edge)
                else:
                    boundaryEdges.remove(edge)
        for triangle in badTriangles:
            triangles.remove(triangle)
        for edge in boundaryEdges:
            newTriangle=Triangle(edge[0],edge[1],point)
            triangles.append(newTriangle)
    
    def super_vert(tri):
        return any(any(same(v,sv) for sv in superTriangle.vertices) for v in tri.vertices)

    triangles = [t for t in triangles if not super_vert(t)]
    triangles=LawsonFlip(triangles)
    return triangles


if __name__ =="__main__":
    print("Delaunay Triangulation")
    print("This program prints the Delaunay Triangulation of a set of points by applying the Bowyer-Watson algorithm.")
    s=int(input("Please, give me the number of points used in Delaunay Triangulation : "))
    L = np.random.uniform(-250, 250, (s, 2))
    L = np.round(L, decimals=10)
    points=[(x,y) for x,y in L]
    points = sorted(points, key=lambda p: (p[0], p[1]))
    x = np.array([pt[0] for pt in points])
    y = np.array([pt[1] for pt in points])
    BowyerWatsonTriangulation=BowyerWatson(points)
    fig,(ax)=plt.subplots(figsize=(12,8))
    BowyerPlot(ax, BowyerWatsonTriangulation,points)
    plt.tight_layout()
    plt.savefig("triangulation.png")
    plt.show()
