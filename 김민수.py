def cal_oval(M, planet):
    G = 6.6743 * 10**-11
    AU__m = 1.496 * 10**11
    km__m = 1000
    Msolar__kg = 1.989 * 10**30

    r0_m = planet['peri_dist'] * AU__m
    v0_m = planet['peri_speed'] * km__m
    
    L_radius = (2 / r0_m - v0_m**2 / (G * (M * Msolar__kg)))**-1 / AU__m

    e = cal_ecc(planet, L_radius)
    
    if 0 < e < 1:
        S_radius = L_radius * (1 - e*e)**0.5
    else:
        S_radius = 0
        
    return L_radius, S_radius

def update_planet_derived_values(star_mass, planet_info):
    for name, data in list(planet_info.items()):
        try:
            L_radius, S_radius = cal_oval(star_mass, data)
            data['semi_major_axis'] = L_radius
            data['semi_minor_axis'] = S_radius
            
            orbital_period(L_radius, star_mass, data)
            
            if data['period'] > 0:
                a = L_radius
                T_yr = data['period']
                data['speed_av'] = (2 * math.pi * a / T_yr) * 4.74372
            else:
                data['speed_av'] = 0.0
                
        except ZeroDivisionError:
            print(f"\n[알림] {name} 행성은 공전 궤도를 유지할 수 없어 분석에서 제외됩니다.")
            planet_info.pop(name)

def sort_and_print(star_mass, planet_info):
    if not planet_info:
        print("\n[안내] 현재 시스템에 등록된 행성이 없습니다. 먼저 행성을 추가해주세요.")
        return

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
        return sort_and_print(star_mass, planet_info)

    if order == 0:
        return

    update_planet_derived_values(star_mass, planet_info)

    print("\n" + "="*75)
    print(f"★ 현재 궤도 시스템 정보 요약 (중심 항성 질량: {star_mass:.4f} M☉) ★")
    print(f"등록된 총 행성 수: {len(planet_info)}개")
    print("="*75)

    sort_keys = {
        1: lambda x: x[0],
        2: lambda x: x[1]['peri_dist'],
        3: lambda x: x[1].get('speed_av', 0.0),
        4: lambda x: x[1].get('period', 0.0),
        5: lambda x: x[1].get('eccentricity', 0.0)
    }

    if order in sort_keys:
        sorted_list = sorted(planet_info.items(), key=sort_keys[order])
        for planet, data in sorted_list:
            print(f"▶ 행성명: [{planet}]")
            print(f"  - 근일점 좌표: ({data['peri_pos'][0]:.3f}, {data['peri_pos'][1]:.3f}) AU")
            print(f"  - 근일점 거리: {data['peri_dist']:.4f} AU")
            print(f"  - 근일점 속력: {data['peri_speed']:.2f} km/s")
            print(f"  - 평균 공전속력: {data.get('speed_av', 0.0):.2f} km/s")
            print(f"  - 공전 주기:   {data.get('period', 0.0):.4f} 년 (yr)")
            print(f"  - 궤도 장반경 (긴반지름): {data.get('semi_major_axis', 0.0):.4f} AU")
            print(f"  - 궤도 단반경 (짧은반지름): {data.get('semi_minor_axis', 0.0):.4f} AU")
            print(f"  - 궤도 이심률: {data.get('eccentricity', 0.0):.4f}")
            print("-" * 75)
    else:
        return sort_and_print(star_mass, planet_info)
