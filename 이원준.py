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
    Planet['eccentricity']=Eccentricity
    return Eccentricity

