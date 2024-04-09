import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import math

class Node:
    def __init__(self,coords):
        self.region = None
        self.temperature = 0
        self.coords = np.array(coords)
        self.x = coords[0]
        self.y = coords[1]

class Mesh:
    def __init__(self, width, height, wall_thickness ,insul_thickness,cladding_thickness):
        self.width = width
        self.height = height
        self.wall_thickness = wall_thickness
        self.insul_thickness = insul_thickness
        self.cladding_thickness = cladding_thickness
        self.useless_nodes = []

        self.R = self.cladding_thickness + self.insul_thickness + 0.1*self.width
        self.r = self.insul_thickness + 0.1*self.width
        self.nodes = []
        self.node_coords = []

        self.T_in = 25 #indoors temperature
        self.T_out = 10


        #1.1. Creating Nodes
        x0 = 0
        xe = self.width
        x1 = x0 + self.cladding_thickness
        x2 = x1 + self.insul_thickness
        x3 = x0 + self.R
        x4 = x2 + self.wall_thickness
        y0 = 0
        ye = self.height
        y4 = ye - self.cladding_thickness
        y3 = y4 - self.insul_thickness
        y2 = ye - self.R
        y1 = y3 - self.wall_thickness

        #Discretizing region 1: cladding
        self.n1_1 = 20
        self.n1_2 =7

        for x in np.linspace(x3,xe,num=self.n1_1):
            for y in np.linspace(y4,ye, self.n1_2):
                if [x,y] not in self.nodes :
                    self.node_coords.append([x,y])
                    node = Node([x,y])
                    node.region = 1
                    self.nodes.append(node)


        for y in np.linspace(y0,y2,num=self.n1_1):
            for x in np.linspace(x0,x1, num=self.n1_2):
                if [x,y] not in self.nodes:
                    self.node_coords.append([x,y])
                    node = Node([x,y])
                    node.region = 1
                    self.nodes.append(node)

        for rad in np.linspace(self.r,self.R,self.n1_2):
            for theta in np.linspace(np.pi/2,np.pi,self.n1_2+5):
                x = rad*np.cos(theta)+x3
                y = rad*np.sin(theta)+y2
                if [x,y] not in self.nodes:
                    self.node_coords.append([x,y])
                    node = Node([x,y])
                    node.region = 1
                    self.nodes.append(node)


        #Discretizing region 2: insulation
        self.n2_2 =3

        for x in np.linspace(x3,xe,num=self.n1_1):
            for y in np.linspace(y3,y4, self.n2_2):
                if [x,y] not in self.nodes :
                    self.node_coords.append([x,y])
                    node = Node([x,y])
                    node.region = 2
                    self.nodes.append(node)


        for y in np.linspace(y0,y2,num=self.n1_1):
            for x in np.linspace(x1,x2, num=self.n2_2):
                if [x,y] not in self.nodes:
                    self.node_coords.append([x,y])
                    node = Node([x,y])
                    node.region = 2
                    self.nodes.append(node)

        for rad in np.linspace(y3-y2,self.r,self.n2_2):
            for theta in np.linspace(np.pi/2,np.pi,self.n1_2+5):
                x = rad*np.cos(theta)+x3
                y = rad*np.sin(theta)+y2
                if [x,y] not in self.nodes:
                    self.node_coords.append([x,y])
                    node = Node([x,y])
                    node.region = 2
                    self.nodes.append(node)



        #Discretizing region 3: wall
        self.n2_3 =10

        #horizontal fragment
        for x in np.linspace(x3,xe,num=self.n1_1):
            if x<=x4:
                y1 = -x+width
                for y in np.linspace(y1,y3, self.n2_3):
                    if [x,y] not in self.nodes :
                        self.node_coords.append([x,y])
                        node = Node([x,y])
                        node.region = 3
                        self.nodes.append(node)
            else:
                for y in np.linspace(y1,y3, self.n2_3):
                    if [x,y] not in self.nodes :
                        self.node_coords.append([x,y])
                        node = Node([x,y])
                        node.region = 3
                        self.nodes.append(node)



        for y in np.linspace(y0,y2,num=self.n1_1):
            if y<y1:
                for x in np.linspace(x2,x4, num=self.n2_3):
                    if [x,y] not in self.nodes:
                        self.node_coords.append([x,y])
                        node = Node([x,y])
                        node.region = 3
                        self.nodes.append(node)
            else:
                x4 = -y + height
                for x in np.linspace(x2,x4, num=self.n2_3):
                    if [x,y] not in self.nodes:
                        self.node_coords.append([x,y])
                        node = Node([x,y])
                        node.region = 3
                        self.nodes.append(node)

        #2. Create elements

    def generate(self):
        trg = Delaunay(self.node_coords)
        for x in np.linspace(self.cladding_thickness+self.insul_thickness+self.wall_thickness+0.01*self.width,self.width,2*self.n1_1):
            self.useless_nodes.append([x, self.height-self.cladding_thickness-self.insul_thickness-self.wall_thickness-0.01*self.height])

        for y in np.linspace(0, self.height-self.cladding_thickness-self.insul_thickness-self.wall_thickness-0.01*self.height,2*self.n1_1):
            self.useless_nodes.append([self.cladding_thickness+self.insul_thickness+self.wall_thickness+0.01*self.width, y])

        useless_simplices = trg.find_simplex(self.useless_nodes)
        self.mesh = np.delete(trg.simplices, [simplex for simplex in list(useless_simplices)],0)
        self.delaunay = Delaunay(self.mesh)
        return self.mesh




    def plot_nodes(self):
        Nodes = np.array(self.node_coords)
        fig, ax = plt.subplots()
        plt.plot(Nodes[:,0],Nodes[:,1],'.',color='b')
        ax.set_aspect('equal')
        plt.show()

    def plot(self):
        Nodes = np.array(self.node_coords)
        fig1, ax1 = plt.subplots()
        plt.triplot(Nodes[:,0],Nodes[:,1],self.mesh,color='r')
        plt.plot(Nodes[:,0],Nodes[:,1],'.',color='b')
        ax1.set_aspect('equal')
        plt.show()


    def add_cavity(self,shape,center,d,n_points):
        if shape == 'circle':
            for rad in np.linspace(0,d/2-0.005*self.width,self.n2_2*10):
                for theta in np.linspace(0,2*np.pi,self.n1_2*10):
                    x = rad*np.cos(theta)+center[0]
                    y = rad*np.sin(theta)+center[1]
                    self.useless_nodes.append([x,y])

            for theta in np.linspace(0,2*np.pi,n_points):
                X = d/2*np.cos(theta)+center[0]
                Y = d/2*np.sin(theta)+center[1]
                if [X,Y] not in self.node_coords:
                        self.node_coords.append([X,Y])
            for node in self.node_coords:
                if math.dist(node,center)<d/2:
                    self.node_coords.remove(node)


    def set_precision(self, longitudinal ,transversal,insul,cladding):
        self.n1_1 = longitudinal
        self.n1_2 = cladding
        self.n2_2 = insul
        self.n2_3 = transversal

    def set_temperature(self):
        pass
    def set_material(self, region):
        pass

    def export(self):
        pass


class Material:
    def __init__(self):
        self.D = []
