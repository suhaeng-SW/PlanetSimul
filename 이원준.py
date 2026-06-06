import matplotlib.pyplot as plt
import numpy as np
import math

def orbital_period(Longer_Radius,Main_Mass):
    G = 6.6743*10**-11
    period = 2*math.pi * (Longer_Radius**3 / Main_Mass)**0.5
    return period

def cal_ecc(Peri_Distance, Longer_Radius):
    Eccentricity = 1 - Peri_Distance/Longer_Radius
    return Eccentricity

