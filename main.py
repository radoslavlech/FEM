from mesh import *
from functions import *
from sympy import *

Mesh1 = Mesh(1,1,0.25,0.1,0.1)
#Mesh1.add_cavity('circle',(0.5,0.7),0.1,50)
Mesh1.generate()
Mesh1.plot()
#element1 node1 coordinates
#print(Mesh1.nodes[int(Mesh1.delaunay.points[1][1])])


D = np.matrix('1.4 0; 0 1.4')


