from mesh import *

Mesh1 = Mesh(1,1,0.25,0.1,0.1)
#Mesh1.add_cavity('circle',(0.5,0.7),0.1,50)
Mesh1.generate()
Mesh1.plot()