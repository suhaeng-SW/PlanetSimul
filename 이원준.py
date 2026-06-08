import matplotlib.pyplot as plt
import numpy as np
import math

def orbital_period(Longer_Radius,Main_Mass,Planet):
    G = 0.99893960704 #AU, yr, Mo기준
    Period = 2*math.pi * (Longer_Radius**3 /G/Main_Mass)**0.5
    Planet['period']=Period

def cal_ecc(Planet, Longer_Radius):
    Distance = Planet['peri_dist']
    Eccentricity = 1 - Distance/Longer_Radius
    if Eccentricity >0 and Eccentricity<1:
        Planet['eccentricity']=Eccentricity
    else:
        print('Error: Wrong input')
    return Eccentricity

def drawing_graph(Shorter_Radius, Longer_Radius, peri_x, peri_y):
    c = np.sqrt(Longer_Radius**2 - Shorter_Radius**2) #초점
    r = np.sqrt(peri_x**2 + peri_y**2)
    ux = peri_x/r
    uy = peri_y/r

    center_x = 0 - c*ux
    center_y = 0 - c*uy

    theta = np.arctan2(peri_y,peri_x)
    t = np.linspace(0, 2*np.pi, 1000)

    x = Longer_Radius*np.cos(t)
    y = Shorter_Radius*np.sin(t)

    rotate_x = x*np.cos(theta)-y*np.sin(theta) + center_x
    rotate_y = x*np.sin(theta)+y*np.cos(theta) + center_y

    plt.figure(figsize=(8,8))
    plt.plot(rotate_x,rotate_y)
    plt.scatter([0], [0], label='항성')
    plt.scatter([peri_x], [peri_y], label="근일점")
    plt.axis('equal')
    plt.legend()
    plt.show()


