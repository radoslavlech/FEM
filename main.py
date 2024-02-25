from mesh import *
from functions import *
from sympy import *
import numpy as np

Mesh1 = Mesh(1,1,0.25,0.1,0.1)
#Mesh1.add_cavity('circle',(0.5,0.7),0.1,50)
Mesh1.generate()
Mesh1.plot()
#element1 node1 coordinates
#print(Mesh1.nodes[int(Mesh1.delaunay.points[1][1])])


D = np.matrix('1.4 0; 0 1.4')
r,s = symbols('r s')
h=1

for element in range(len(Mesh1.mesh)):
    K_local = np.zeros((3,3))

    c =np.matmul(np.matmul((np.matmul(J_inv(Mesh1,element),B(Mesh1,element))).transpose(),D),(np.matmul(J_inv(Mesh1,element),B(Mesh1,element))))*h*np.linalg.det(J(Mesh1,element))
    for i in range(3):
        for j in range(3):
            K_local[i,j] = integrate(integrate(c[i,j],(r,0,1-s)),(s,0,1))
    print(K_local)




