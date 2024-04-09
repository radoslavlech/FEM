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

T = np.zeros((len(Mesh1.mesh),1))  #Temperature at each ELEMENT
x,y = sp.symbols('x y')

print(node(Mesh1,1,0))

#print nodes pf the first element:
n1 = np.array(Mesh1.nodes[int(Mesh1.delaunay.points[1][0])])
n2 = np.array(Mesh1.nodes[int(Mesh1.delaunay.points[1][1])])
n3 = np.array(Mesh1.nodes[int(Mesh1.delaunay.points[1][2])])
print(L(Mesh1,1,0,n1[0],n1[1]))
#L1 at node 1 is 1, which means that it works!!
exit()

for element in range(len(Mesh1.mesh)):
    L_vec = np.array([L(Mesh1,element,0,x,y),L(Mesh1,element,1,x,y),L(Mesh1,element,2,x,y)])
    K_local = np.zeros((3,3))
    q_local = np.zeros((3,1))

    c =np.matmul(np.matmul((np.matmul(J_inv(Mesh1,element),B(Mesh1,element))).transpose(),D),(np.matmul(J_inv(Mesh1,element),B(Mesh1,element))))*h*np.linalg.det(J(Mesh1,element))
    for i in range(3):
        for j in range(3):
            K_local[i,j] = integrate(integrate(c[i,j],(r,0,1-s)),(s,0,1))




