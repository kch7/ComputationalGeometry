# Delaunay Triangulation

Regarding the Delaunay Triangulation via lifting, at first i computed the 3D-Convex Hull by using the Incremental Algorithm and by raising the points to the parabola z=x^2+y^2. As a result, the form of the points was the following: (x,y,x^2+y^2).
After computing the 3D-Convex Hull,i created a function called Delaunay Triangulation. In this specific function, i divided each face of the hull, into its components(its vertices) and then i computed the cross product of those two matrices : <pre>(np.cross(v2-v0,v1-v0)).</pre>
If the third component of the product was less than 0, then i would create each triangle and append it to a list called triangles. The list called triangles included all triangles of the Delaunay Triangulation.
In main, at first i computed the 3D-Convex Hull, so that i would get the hull, and then i called the function "Triangulation".

Now, i have added another method of creating a Delaunay Triangulation. This method is called Bowyer-Watson. In order to implement this method, we have to compute at first a super-triangle. A super-triangle is called the triangle that encloses all given two-dimensional points. Then the algorithm i follow for the implementation is derived from Wikipedia. 



# Useful Info 

In order to avoid dependency issues, inside Delaunay directory, i have created a blank file called __init__.py.
Also, in the libraries of lifting.py, i have added this specific line: <pre>sys.path.append('..')</pre> , so as to ensure that lifting.py is able to use the functions required for the computation of the convex hull.




