import numpy as np
import sympy as sp


def xi(x,node1,node2):
    return (2*x-node1[0]-node2[0])/(node2[0]-node1[0])

def eta(y, node1,node2):
    return (2*y-node1[1]-node2[1])/(node2[1]-node1[1])

def area(node1,node2,node3):
    node1 = np.array(node1)
    node2 = np.array(node2)
    node3 = np.array(node3)
    a = np.matrix([[1, node1[0],node1[1]],[1, node2[0],node2[1]],[1, node3[0],node3[1]]])
    return 0.5*np.linalg.det(a)

def L(mesh,element,index,x,y):
    i = np.array(mesh.nodes[int(mesh.delaunay.points[element][index])])
    j = np.array(mesh.nodes[int(mesh.delaunay.points[element][(index+1)%3])])
    k = np.array(mesh.nodes[int(mesh.delaunay.points[element][(index+2)%3])])

    a = j[0]*k[1]-k[0]*j[1]
    b = j[1]-k[1]
    c = k[0]-j[0]
    return 1/2/area(i,j,k)*(a+b*x+c*y)


def B(mesh, element):
    b = np.matrix([[-1,1,0],[-1,0,1]])
    return b

def J(mesh,element):
    i = np.array(mesh.nodes[int(mesh.delaunay.points[element][0])])
    j = np.array(mesh.nodes[int(mesh.delaunay.points[element][1])])
    k = np.array(mesh.nodes[int(mesh.delaunay.points[element][2])])
    xy = np.array([[i[0],i[1]],[j[0],j[1]],[k[0],k[1]]])
    return np.matrix(np.matmul(B(mesh,element),xy))


def J_inv(mesh,element):
    return np.linalg.inv(J(mesh,element))
