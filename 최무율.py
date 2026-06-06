# 입력 및 입력값 자료 저장
def star_input():
    try:
        res = input('\n중심 항성의 질량(kg), 추가하실 공전 행성의 개수를\n공백으로 구분하여 차례로 입력하세요\n>_ ').split()
        mass,N = float(res[0]), int(res[1])

        if mass <= 0 or N <= 0:
            raise ValueError('항성의 질량 및 행성의 개수는 0보다 커야 합니다.')

        return mass,N
    
    except (ValueError, IndexError) as e:
        print(f'\n입력 형식이 잘못되었습니다! 다시 입력해주세요 :( \n{e}')
        return star_input()

def input_values():
    global planet_info

    star_mass,N = star_input()
    planet_info = {}

    for _ in range(N):
        while True:
            try:
                name,x0,y0,v0 = input('\n공전 행성의 \n이름,근일점 x좌표(AU),근일점 y좌표(AU),근일점 속력(km/s)\n을 공백으로 구분하여 차례로 입력하세요\n(중심 항성의 좌표는 (0,0)입니다.)\n>_ ').split()
                x0,y0,v0 = map(float,(x0,y0,v0))

                if (x0 == 0 and y0 == 0) or v0 <= 0:
                    raise ValueError('근일점 위치는 항성의 위치 (0,0)이 될 수 없으며, 행성의 속력은 0보다 커야 합니다.')
                
                planet_info[name] = {'peri_pos':[x0,y0],
                                     'peri_dist':(x0*x0+y0*y0)**0.5,
                                     'peri_speed':v0}

                break

            except ValueError as e:
                print(f'\n입력 형식이 잘못되었습니다! 다시 입력해주세요 :( \n{e}')

    return star_mass, planet_info


# 그래프 계산
def cal_oval(G,M,planet):
    #from 이원준 import cal_ecc
    
    AU__m = 1.5*10**11
    km__m = 1000

    r0_m = planet['peri_dist'] * AU__m
    v0_m = planet['peri_speed'] * km__m
    L_radius = (2/r0_m - v0_m**2/(G*M))**-1 / AU__m

    e = cal_ecc(planet,L_radius)
    S_radius = L_radius*(1-e*e)**0.5

    return L_radius,S_radius


# 매뉴얼 출력 및 기능 수행
def input_manual():
    print('\n-------------------------------')
    print('매뉴얼 \n')
    print('1. 중심항성 질량 수정')
    print('2. 공전행성 정보 수정 및 추가')
    print('3. 공전행성 정보 삭제')
    print('4. 현재 궤도시스템 정보 출력')
    print('0. 프로그램 종료')
    print('-------------------------------')
    
    try:
        order = input('사용할 기능의 숫자를 입력하세요\n>_ ')
        order = int(order)
        return order
    except ValueError as e:
        print(f'\n입력 형식이 잘못되었습니다! 다시 입력해주세요 :( \n{e}')
        return input_manual()
    
def sort_and_print(star_mass,planet_info):
    print(f'\n항성 질량 : {star_mass}kg, 구성 행성 수 : {len(planet_info)}')
    for planet in sorted(planet_info.items(), key=lambda x : x[0]):
        print(*planet)