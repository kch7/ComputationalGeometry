# Voronoi Diagram


I have chosen to implement the Voronoi Diagram by using the method of the tangent planes. At first, i gather n points in RxR.                                        Then, i lift them to RxRxR by applying this simple formula: <pre>(x,y)->(x,y,x**2 + y**2)</pre>
After that, i retrieve the minimum x-coordinate,the minimum y-coordinate,the maximum x-coordinate and the maximum y-coordinate.                                          I decrement the minimum coordinates by 10, and i add up 10 to the maximum ones. Then, i initiate a grid consisting of 90000 values                                  inside the rectangle created by the computed coordinates. The goal of using the grid is finding the tangent plane equation with the maximum                      numerical value at each site of my grid. Then, i compute the dominant points from the comparisons between the Voronoi cell.                                            In order to compute these changes, i use an NumPy array called edges. At first, the array is initialized with the value False.                                           In this array, i save the changes from the comparison of each Voronoi cells with its neighbors (up,down,right and left). When a change is recorded,
the respective value of the cell in the array becomes True.At the end, i plot the Voronoi Diagram 

# Useful sources

https://www.math.pku.edu.cn/teachers/chenzy/Note/vmsc.pdf

https://www.cs.cmu.edu/afs/cs/academic/class/15456-s14/Handouts/cmsc754-lects.pdf


