from 최무율 import *
from 이원준 import *
#from 김민수 import *

M,planet_info = input_values()
for planet in planet_info.values():
    a,b = cal_oval(M,planet)
    orbital_period(a,M,planet)
    drawing_graph(b,a,planet)
    planet['speed_av']=-1

while True:
    order = input_manual()
    if order == 0: break
    elif order == 1:
        planet_adding = input_values(first=False,planet_info=planet_info)
        a,b = cal_oval(M,planet_info[planet_adding])
        orbital_period(a,M,planet_info[planet_adding])
        planet_info[planet_adding]['speed_av']=-1
    elif order == 2:
        remove_planet(planet_info)
    elif order == 3:
        sort_and_print(M,planet_info)

print('\n프로그램을 종료합니다.')