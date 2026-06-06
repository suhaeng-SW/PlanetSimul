
# 입력 및 입력값 자료 저장
def star_input():
    try:
        res = input('중심 항성의 질량(kg), 추가하실 공전 행성의 개수를\n공백으로 구분하여 차례로 입력하세요\n>_ ').split()
        mass,N = float(res[0]), int(res[1])
        if mass <= 0 or N <= 0:
            raise ValueError('항성의 질량 및 행성의 개수는 0보다 커야 합니다.')

        return mass,N
    except (ValueError, IndexError) as e:
        print(f'\n입력 형식이 잘못되었습니다! 다시 입력해주세요. \n{e}\n')
        return star_input()

def input_values():
    star_mass,N = star_input()
    planet_info = {}

    for _ in range(N):
        while True:
            try:
                name,x0,y0,v0 = input('\n공전 행성의 \n이름,근일점 x좌표(AU),근일점 y좌표(AU),근일점 속력(km/s)\n을 공백으로 구분하여 차례로 입력하세요\n>_ ').split()
                planet_info[name] = {'peri_pos':[float(x0),float(y0)],
                                     'peri_dist':(x0+y0)**0.5,
                                     'peri_speed':float(v0)}
                if (x0 == 0 and y0 == 0) or v0 <= 0:
                    raise ValueError('근일점 위치는 항성의 위치 (0,0)이 될 수 없으며, 행성의 속력은 0보다 커야 합니다.')
                break
            except ValueError as e:
                print(f'\n입력 형식이 잘못되었습니다! 다시 입력해주세요. \n{e}\n')

    return star_mass, planet_info
    
input_values()

# 그래프 계산
def cal_oval(G,M,planet):
    r0 = planet['peri_dist']
    v0 = planet['peri_speed']
    e = planet['eccentricity']
    
    L_radius = (2/r0 - v0/G*M)*-1
    S_radius = L_radius*(1-e*e)**0.5

    return L_radius,S_radius

