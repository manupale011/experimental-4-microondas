import numpy as np

d=3.8
l=2.85

for i in range(3):
    arg= (i*l)/(2*d)
    ang=np.arcsin(arg)
    print(180*ang/np.pi)