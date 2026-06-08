def average_orbital_speed(Longer_Radius, Planet):
    Speed = (2 * math.pi * Longer_Radius / Planet['period']) * 4.74372
    Planet['speed_av'] = Speed

def update_planet_derived_values(star_mass, planet_dictionary):
    G = 6.6743 * 10**-11
    AU__m = 1.496 * 10**11
    km__m = 1000
    Msolar__kg = 1.989 * 10**30

    for planet_name, planet in list(planet_dictionary.items()):
        try:
            planet['star_mass'] = star_mass

            r0_m = planet['peri_dist'] * AU__m
            v0_m = planet['peri_speed'] * km__m
            star_mass_kg = star_mass * Msolar__kg
            
            longer_radius = (2 / r0_m - v0_m**2 / (G * star_mass_kg))**-1 / AU__m
            planet['longer_radius'] = longer_radius

            eccentricity = cal_ecc(planet, longer_radius)

            if 0 < eccentricity < 1:
                shorter_radius = longer_radius * (1 - eccentricity * eccentricity)**0.5
            else:
                shorter_radius = 0.0
            planet['shorter_radius'] = shorter_radius

            orbital_period(longer_radius, star_mass, planet)
            average_orbital_speed(longer_radius, planet)

        except ZeroDivisionError:
            print(f"\n[알림] {planet_name} 행성은 공전 궤도를 유지할 수 없어 분석에서 제외됩니다.")
            planet_dictionary.pop(planet_name)

def star_input():
    try:
        res = input('\n중심 항성의 질량(M☉), 추가하실 공전 행성의 개수를\n공백으로 구분하여 차례로 입력하세요\n>_ ').split()
        mass, N = float(res[0]), int(res[1])

        if mass <= 0 or N <= 0:
            raise ValueError('항성의 질량 및 행성의 개수는 0보다 커야 합니다.')

        return mass, N    
    except (ValueError, IndexError) as e:
        print(f'\n입력 형식이 잘못되었습니다! 다시 입력해주세요 :( \n{e}')
        return star_input()

def input_values():
    star_mass, N = star_input()
    planet_info = {}

    for i in range(N):
        while True:
            try:
                name, x0, y0, v0 = input(f'\n[{i+1}/{N}] 공전 행성의 \n이름, 근일점 x좌표(AU), 근일점 y좌표(AU), 근일점 속력(km/s)\n을 공백으로 구분하여 차례로 입력하세요\n(중심 항성의 좌표는 (0,0)입니다.)\n>_ ').split()
                x0, y0, v0 = map(float, (x0, y0, v0))

                if (x0 == 0 and y0 == 0) or v0 <= 0:
                    raise ValueError('근일점 위치는 항성의 위치 (0,0)이 될 수 없으며, 행성의 속력은 0보다 커야 합니다.')
                
                planet_info[name] = {
                    'peri_pos': [x0, y0],
                    'peri_dist': (x0*x0 + y0*y0)**0.5,
                    'peri_speed': v0
                }
                break
            except (ValueError, IndexError) as e:
                print(f'\n입력 형식이 잘못되었습니다! 다시 입력해주세요 :( \n{e}')

    return star_mass, planet_info

def input_manual():
    print('\n-------------------------------')
    print('매뉴얼 \n')
    print('1. 중심항성 질량 수정')
    print('2. 공전행성 정보 수정 및 추가')
    print('3. 공전행성 정보 삭제')
    print('4. 현재 궤도시스템 정보 출력 및 정렬')
    print('5. 현재 궤도 그래프 그리기 (시각화)')
    print('0. 프로그램 종료')
    print('-------------------------------')
    
    try:
        order = input('사용할 기능의 숫자를 입력하세요\n>_ ')
        order = int(order)
        return order
    except ValueError as e:
        print(f'\n입력 형식이 잘못되었습니다! 다시 입력해주세요 :( \n{e}')
        return input_manual()

def sort_and_print_system(star_mass, planet_info):
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
        return sort_and_print_system(star_mass, planet_info)

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
            print(f"  - 궤도 장반경 (긴반지름): {data.get('longer_radius', 0.0):.4f} AU")
            print(f"  - 궤도 단반경 (짧은반지름): {data.get('shorter_radius', 0.0):.4f} AU")
            print(f"  - 궤도 이심률: {data.get('eccentricity', 0.0):.4f}")
            print("-" * 75)
    else:
        return sort_and_print_system(star_mass, planet_info)

def main():
    print("==================================================")
    print("      태양계 외 행성계 궤도 분석 시뮬레이터       ")
    print("==================================================")
    
    star_mass, planet_info = input_values()
    update_planet_derived_values(star_mass, planet_info)

    while True:
        order = input_manual()

        if order == 1:
            while True:
                try:
                    new_mass = float(input(f'\n현재 중심항성 질량: {star_mass} M☉\n새로운 질량값을 입력하세요 (M☉)\n>_ '))
                    if new_mass <= 0:
                        raise ValueError("질량은 0보다 커야 합니다.")
                    star_mass = new_mass
                    update_planet_derived_values(star_mass, planet_info)
                    print(f"\n[성공] 항성의 질량이 {star_mass} M☉로 수정되었습니다.")
                    break
                except ValueError as e:
                    print(f'\n입력 오류: {e}')

        elif order == 2:
            print("\n--- 행성 정보 수정 및 추가 ---")
            name = input("수정 또는 추가할 행성의 이름을 입력하세요\n>_ ").strip()
            while True:
                try:
                    x0, y0, v0 = input('근일점 x좌표(AU), 근일점 y좌표(AU), 근일점 속력(km/s)을\n공백으로 구분하여 입력하세요\n>_ ').split()
                    x0, y0, v0 = map(float, (x0, y0, v0))

                    if (x0 == 0 and y0 == 0) or v0 <= 0:
                        raise ValueError('좌표가 (0,0)이거나 속력이 0 이하일 수 없습니다.')
                    
                    planet_info[name] = {
                        'peri_pos': [x0, y0],
                        'peri_dist': (x0*x0 + y0*y0)**0.5,
                        'peri_speed': v0
                    }
                    update_planet_derived_values(star_mass, planet_info)
                    print(f"\n[성공] 행성 '{name}'의 정보가 업데이트되었습니다.")
                    break
                except (ValueError, IndexError) as e:
                    print(f'\n입력 형식이 잘못되었습니다! 다시 입력해주세요 :( \n{e}')

        elif order == 3:
            if not planet_info:
                print("\n[안내] 삭제할 행성이 없습니다.")
                continue
            print("\n현재 등록된 행성 목록:", list(planet_info.keys()))
            target = input("삭제할 행성의 이름을 정확히 입력하세요\n>_ ").strip()
            if target in planet_info:
                planet_info.pop(target)
                print(f"\n[성공] '{target}' 행성이 삭제되었습니다.")
            else:
                print(f"\n[실패] '{target}' 행성을 찾을 수 없습니다.")

        elif order == 4:
            sort_and_print_system(star_mass, planet_info)

        elif order == 5:
            if not planet_info:
                print("\n[안내] 시각화할 행성이 없습니다.")
                continue
            print("\n현재 등록된 행성 목록:", list(planet_info.keys()))
            target = input("궤도를 그릴 행성의 이름을 입력하세요 (전체 입력을 원하시면 'all'을 입력하세요)\n>_ ").strip()
            
            if target == 'all':
                for name, data in planet_info.items():
                    drawing_graph(data['shorter_radius'], data['longer_radius'], data['peri_pos'][0], data['peri_pos'][1])
            elif target in planet_info:
                data = planet_info[target]
                drawing_graph(data['shorter_radius'], data['longer_radius'], data['peri_pos'][0], data['peri_pos'][1])
            else:
                print(f"\n[실패] '{target}' 행성을 찾을 수 없습니다.")

        elif order == 0:
            print("\n프로그램을 종료합니다. 이용해 주셔서 감사합니다!")
            break
        else:
            print("\n존재하지 않는 기능 번호입니다. 다시 선택해 주세요.")

if __name__ == "__main__":
    main()
