The 3D-Convex Hull was implemented with the use of the incremental algorithm.
I modified the classic incremental algorithm, by using at most 8 points of my dataset 
in order to retrieve the initial tetrahedron. Then, i created a function called Normalize, 
useful for the proper orientation of the faces. After implementing these substantial steps, 
i shuffled the points. All the other part is the known 3d incremental algorithm.

Further info for this algorithm can be found at : https://tildesites.bowdoin.edu/~ltoma/teaching/cs3250-CompGeom/spring17/Lectures/cg-hull3d.pdf 
