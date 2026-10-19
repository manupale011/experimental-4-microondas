import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#parametros ajustados del patron de emision
a         =    10.891465
theta_0   =     1.526437
h         =  1875.903448
offset_c  =     3.654275

def I_a_40cm(theta):
    I=h*np.exp(-(theta-theta_0)**2/(2*a**2))
    return I

