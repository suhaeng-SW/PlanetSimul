from 최무율 import *
from 이원준 import *
from 김민수 import *

print('\n'*10)
print('=========================================')
print('케플러 법칙을 적용한 행성 궤도 계산기')
print('1204, 1215, 1220')
print('=========================================\n')

M,planet_info = input_values()
plt.figure(figsize=(8,8))
plt.scatter([0],[0],label='Star')

for name,planet in planet_info.items():
    a,b = cal_oval(M,planet)
    orbital_period(a,M,planet)
    drawing_graph(a,b,planet,name)
    cal_speed_av(planet,a,b)
plt.axis('equal')
plt.legend()
plt.show()

print_final(planet_info)
input('\n계속하려면 아무 키나 입력하세요.')
print('\n'*10)

while True:
    order = input_manual()
    if order == 0: break
    elif order == 1:
        planet_adding = input_values(first=False,planet_info=planet_info)
        a,b = cal_oval(M,planet_info[planet_adding])
        orbital_period(a,M,planet_info[planet_adding])
        cal_speed_av(planet_info[planet_adding],a,b)
    elif order == 2:
        remove_planet(planet_info)
    elif order == 3:
        sort_and_print(M,planet_info)
    elif order == 4:
        plt.figure(figsize=(8,8))
        plt.scatter([0],[0],label='Star')
        for name,planet in planet_info.items():
            a,b = cal_oval(M,planet)
            drawing_graph(a,b,planet,name)
            plt.axis('equal')
            plt.legend()
            plt.show()

print('\n프로그램을 종료합니다. >:3')