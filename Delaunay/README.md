# Delaunay Triangulation

Regarding the Delaunay Triangulation via lifting, at first i computed the 3D-Convex Hull by using the Incremental Algorithm and by raising the points to the parabola z=x^2+y^2. As a result, the form of the points was the following: (x,y,x^2+y^2).
After computing the 3D-Convex Hull,i created a function called Delaunay Triangulation. In this specific function, i divide each face of the hull, into its components(its vertices) and then i compute the cross product of those two matrices : <pre>(np.cross(v2-v0,v1-v0))</pre>.
If the third component of the product is less than 0, then i create each triangle and append it to a list called triangles. The list called triangles includes all triangles of the Delaunay Triangulation.
In main, at first i compute the 3D-Convex Hull, so that i get the hull, and then i call the function "Triangulation".


# Useful Info 

In order to avoid dependency issues, inside Delaunay directory, i have created a blank file called __init__.py.
Also, in the libraries of lifting.py, i have added this specific line: <pre>sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))</pre> , so as to ensure that lifting.py is able to use the functions required for the computation of the convex hull.


