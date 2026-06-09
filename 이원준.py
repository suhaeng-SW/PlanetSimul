import matplotlib.pyplot as plt
import numpy as np
import math

def orbital_period(Longer_Radius,Main_Mass,Planet):
    if Planet['eccentricity']!=float('inf'):
        Period = (Longer_Radius**3 / Main_Mass)**0.5
        Planet['period']=Period
    else:
        Planet['period']=float('inf')

def cal_ecc(Planet, Longer_Radius):
    Distance = Planet['peri_dist']
    Eccentricity = 1 - Distance/Longer_Radius
    if Eccentricity >= 0 and Eccentricity <= 1:
        Planet['eccentricity']=Eccentricity
    else:
        Planet['eccentricity']=float('inf')
    return Eccentricity

def drawing_graph(Longer_Radius, Shorter_Radius, Planet, name):

    peri_x, peri_y = Planet['peri_pos']
    L = Longer_Radius
    S = Shorter_Radius
    c = np.sqrt(L**2 - S**2)
    r = np.sqrt(peri_x**2 + peri_y**2)
    ux = peri_x / r
    uy = peri_y / r

    center_x = -c * ux
    center_y = -c * uy

    theta = np.arctan2(peri_y, peri_x)
    t = np.linspace(0,2*np.pi,1000)

    x = L*np.cos(t)
    y = S*np.sin(t)

    rotate_x = x*np.cos(theta) - y*np.sin(theta) + center_x
    rotate_y = x*np.sin(theta) + y*np.cos(theta) + center_y

    plt.plot(rotate_x, rotate_y, label=name)
    plt.scatter([peri_x],[peri_y])


