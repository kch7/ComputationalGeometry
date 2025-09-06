import numpy as np
import itertools
import matplotlib.pyplot as plt
import sys


#I initiate a class called point , so as to use it in the node of the KD-Tree.
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x:.2f}, {self.y:.2f})"


class KDNode:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

    def __repr__(self):
        return f"KDNode({self.point})"
    
    #The length of each node equals to 2, because each point consists of two coordinates.
    def __len__(self):
        return 2

#This function builds a KD-Tree recursively. The depth is used to determine the axis for splitting the points.
#The axis is determined by the depth modulo k, where k is the number of dimensions (2 in this case).
#The points are sorted based on the current axis, and the median point is chosen as the root of the subtree.
#The left and right subtrees are built recursively with the remaining points.
def KDTree(points: list, bounds: list, depth=0, ax=None):
    if not points:
        return None

    k = 2
    axis = depth % k
    sorted_points = sorted(points, key=lambda p: (p.x, p.y)[axis])
    median_index = len(sorted_points) // 2
    node = KDNode(sorted_points[median_index]) 
    Plot(node, depth, bounds, ax)
    if axis == 0:
        node.left = KDTree(sorted_points[:median_index], [bounds[0], node.point.x, bounds[2], bounds[3]], depth+1, ax)
        node.right = KDTree(sorted_points[median_index+1:], [node.point.x, bounds[1], bounds[2], bounds[3]], depth+1, ax)
    else:
        node.left = KDTree(sorted_points[:median_index], [bounds[0], bounds[1], bounds[2], node.point.y], depth+1, ax)
        node.right = KDTree(sorted_points[median_index+1:], [bounds[0], bounds[1], node.point.y, bounds[3]], depth+1, ax)

    return node


#With this function, the KD-Tree is plotted
def Plot(node: KDNode, depth: int, bounds: list, ax):
    if node is None:
        return

    x_min, x_max, y_min, y_max = bounds
    x, y = node.point.x, node.point.y
    axis = depth % 2

    # Draw the splitting line
    if axis == 0:  # vertical
        ax.plot([x, x], [y_min, y_max], 'r--')
    else:  # horizontal
        ax.plot([x_min, x_max], [y, y], 'g--')
    ax.plot(x, y, 'ko')
    plt.pause(0.5)




def RangeSearch(node:KDNode,bounds:list,depth,results):
    if node is None:
        return []
    
    x_min, x_max, y_min, y_max = bounds
    x=node.point.x
    y=node.point.y
    axis = depth % 2

    if x_min <= x <= x_max and y_min <= y <= y_max:
        if results is None:
            results = []
        results.append(node.point)

    if axis == 0:  # Vertical line
        if x_min <= x:
            RangeSearch(node.left, bounds, depth + 1, results)
        if x_max >= x:
            RangeSearch(node.right, bounds, depth + 1, results)
    else:
        if y_min <= y:
            RangeSearch(node.left, bounds, depth + 1, results)
        if y_max >= y:
            RangeSearch(node.right, bounds, depth + 1, results)    
    
    return results


#In this function, i sort the points in ascending order by their x-coordinate.
def PlotStepByStep(points:list,x_min:int,x_max:int,y_min:int,y_max:int,s:list):
    sorted_points=sorted(s,key=lambda point:point.x)
    pointslist=[]
    fig=plt.figure()
    inside = sorted(s, key=lambda p: p.x)
    outside = [p for p in points if p not in s]
    a=[point.x for point in outside]
    b=[point.y for point in outside]
    
    plt.scatter(a,b,marker='x',color='black')
    rect = plt.Rectangle((x_min, y_min), x_max-x_min, y_max-y_min, edgecolor='blue', facecolor='none', linestyle='--')
    plt.gca().add_patch(rect)
    for point in sorted_points:
        plt.scatter(a,b,marker='x',color='black')
        rect = plt.Rectangle((x_min, y_min), x_max-x_min, y_max-y_min, edgecolor='blue', facecolor='none', linestyle='--')
        plt.gca().add_patch(rect)
        pointslist.append((point.x,point.y))
        xs,ys=zip(*pointslist)
        plt.plot(xs, ys, 'ro')
        plt.pause(0.5)
    
    plt.savefig("final_plotstep.png", dpi=300, bbox_inches='tight')
    plt.close()


def Create(L:list,bounds:list):
    print("Points:", L)
    fig, ax = plt.subplots()
    ax.set_xlim(bounds[0], bounds[1])
    ax.set_ylim(bounds[2], bounds[3])
    kd_tree=KDTree(L, bounds,0,ax)
    plt.pause(2)
    plt.savefig("final_kd_tree.png", bbox_inches='tight')
    plt.close(fig)
    ax.clear()  # Clear the plot for the final result
    return kd_tree
    
def WriteResults(results:list):
    with open("results.txt", "w") as f:
        f.write(str(len(results))+str(" points were found \n"))
        for point in results:
            f.write(f"{point}\n")
        f.close()


if __name__ == "__main__":
    print("Welcome to the KD-Tree and Range Search Program!")
    print("This program allows you to create a KD-Tree from random points and perform a range search.")
    print("You will be prompted to enter the range of coordinates for the points and the number of points.")
    print("Then, you will specify the range for the x-axis and y-axis for the range search.")    
#Here you insert the range of the coordinates of the points and the number of points. Both x,y are properly sanitized.
    x=abs(int(input("Give me number x (The range of points): ")))
    y=abs(int(input("Give me number y (The number of points): ")))
    print("The range of the points is : ",(-x,x))
#Here you insert the ranges of the query search for the x-axis and the y-axis.
    x_min=int(input("Give me number x_min (The minimum x-value): "))
    x_max=int(input("Give me number x_max (The maximum x-value): "))
    y_min=int(input("Give me number y_min (The minimum y-value): "))
    y_max=int(input("Give me number y_max (The maximum y-value): "))
    L = [Point(np.random.uniform(-x,x), np.random.uniform(-x,x)) for _ in range((y))]
#The points are printed for further comprehension.
    kd_tree=Create(L,[-x,x,-x,x])
    results=[]
    s=RangeSearch(kd_tree,[x_min,x_max,y_min,y_max],0,results)
#A result in the range query search has been found.
    if s:
        WriteResults(s)
        PlotStepByStep(L,x_min,x_max,y_min,y_max,s)
    else:
        print("Range Search is unsuccessful")
