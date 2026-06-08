# 입력 및 입력값 자료 저장
def star_input():
    try:
        res = input('\n중심 항성의 질량(M☉), 추가하실 공전 행성의 개수를\n공백으로 구분하여 차례로 입력하세요\n>_ ').split()
        mass,N = float(res[0]), int(res[1])

        if mass <= 0 or N <= 0:
            raise ValueError('항성의 질량 및 행성의 개수는 0보다 커야 합니다.')

        return mass,N    
    except (ValueError, IndexError) as e:
        print(f'\n입력 형식이 잘못되었습니다! 다시 입력해주세요 :( \n{e}')
        return star_input()

def input_values():
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
def cal_oval(M,planet):
    from 이원준 import cal_ecc
    
    G = 6.6743*10**-11
    AU__m = 1.496*10**11
    km__m = 1000
    Msolar__kg = 1.989*10**30

    r0_m = planet['peri_dist'] * AU__m
    v0_m = planet['peri_speed'] * km__m
    L_radius = (2/r0_m - v0_m**2/(G*(M*Msolar__kg)))**-1 / AU__m

    e = cal_ecc(planet,L_radius)
    S_radius = L_radius*(1-e*e)**0.5

    return L_radius,S_radius


# 매뉴얼 입력
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
    

# 현재 궤도시스템 정보 출력
def sort_and_print(star_mass,planet_info):
    print('\n-------------------------------')
    print('매뉴얼 > 4. 현재 궤도시스템 정보 출력 \n')
    print('1. 이름 기준 정렬')
    print('2. 근일점 거리 기준 정렬')
    print('3. 평균 공전 속력 기준 정렬')
    print('4. 공전 주기 기준 정렬')
    print('5. 이심률 기준 정렬')
    print('0. 이전으로 돌아가기')
    print('-------------------------------')

    try:
        order = input('정렬 기준을 숫자로 입력하세요\n>_ ')
        order = int(order)
    except ValueError as e:
        print(f'\n입력 형식이 잘못되었습니다! 다시 입력해주세요 :( \n{e}')
        return sort_and_print(star_mass,planet_info)

    print(f'\n항성 질량: {star_mass} M☉ | 구성 행성 수: {len(planet_info)}')

    if order == 1:
        for planet,data in sorted(planet_info.items(), key=lambda x : x[0]):
            print(f"[{planet:^5}] 근일점 거리: {data['peri_dist']:.2f} AU | "
                  f"평균 공전속력: {data['speed_av']:.2f} km/s | "
                  f"이심률: {data['eccentricity']:.4f} | "
                  f"주기: {data['period']:.2f} 년")
    elif order == 2:
        for planet,data in sorted(planet_info.items(), key=lambda x : x[1]['peri_dist']):
            print(f"[{planet:^5}] 근일점 거리: {data['peri_dist']:.2f} AU | "
                  f"평균 공전속력: {data['speed_av']:.2f} km/s | "
                  f"이심률: {data['eccentricity']:.4f} | "
                  f"주기: {data['period']:.2f} 년")
    elif order == 3:
        for planet,data in sorted(planet_info.items(), key=lambda x : x[1]['speed_av']):
            print(f"[{planet:^5}] 근일점 거리: {data['peri_dist']:.2f} AU | "
                  f"평균 공전속력: {data['speed_av']:.2f} km/s | "
                  f"이심률: {data['eccentricity']:.4f} | "
                  f"주기: {data['period']:.2f} 년")
    elif order == 4:
        for planet,data in sorted(planet_info.items(), key=lambda x : x[1]['period']):
            print(f"[{planet:^5}] 근일점 거리: {data['peri_dist']:.2f} AU | "
                  f"평균 공전속력: {data['speed_av']:.2f} km/s | "
                  f"이심률: {data['eccentricity']:.4f} | "
                  f"주기: {data['period']:.2f} 년")
    elif order == 5:
        for planet,data in sorted(planet_info.items(), key=lambda x : x[1]['eccentricity']):
            print(f"[{planet:^5}] 근일점 거리: {data['peri_dist']:.2f} AU | "
                  f"평균 공전속력: {data['speed_av']:.2f} km/s | "
                  f"이심률: {data['eccentricity']:.4f} | "
                  f"주기: {data['period']:.2f} 년")
    elif order != 0: return sort_and_print(star_mass,planet_info)