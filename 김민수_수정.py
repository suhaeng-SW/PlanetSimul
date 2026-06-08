def calculate_orbit_sizes(star_mass, planet_details):
    gravity_constant = 6.6743 * 10**-11
    au_to_meters = 1.496 * 10**11
    km_to_meters = 1000
    solar_mass_to_kg = 1.989 * 10**30

    perihelion_distance_meters = planet_details['peri_dist'] * au_to_meters
    perihelion_speed_meters = planet_details['peri_speed'] * km_to_meters
    star_mass_kg = star_mass * solar_mass_to_kg
    
    longer_radius = (2 / perihelion_distance_meters - perihelion_speed_meters**2 / (gravity_constant * star_mass_kg))**-1 / au_to_meters

    eccentricity = cal_ecc(planet_details, longer_radius)
    
    if 0 < eccentricity < 1:
        shorter_radius = longer_radius * (1 - eccentricity*eccentricity)**0.5
    else:
        shorter_radius = 0
        
    return longer_radius, shorter_radius

def update_all_planet_data(star_mass, planet_dictionary):
    for planet_name, planet_details in list(planet_dictionary.items()):
        try:
            longer_radius, shorter_radius = calculate_orbit_sizes(star_mass, planet_details)
            planet_details['semi_major_axis'] = longer_radius
            planet_details['semi_minor_axis'] = shorter_radius
            
            orbital_period(longer_radius, star_mass, planet_details)
            
            if planet_details['period'] > 0:
                orbital_period_years = planet_details['period']
                planet_details['speed_av'] = (2 * math.pi * longer_radius / orbital_period_years) * 4.74372
            else:
                planet_details['speed_av'] = 0.0
                
        except ZeroDivisionError:
            print(f"\n[알림] {planet_name} 행성은 공전 궤도를 유지할 수 없어 분석에서 제외됩니다.")
            planet_dictionary.pop(planet_name)

def print_sorted_planet_system(star_mass, planet_dictionary):
    if not planet_dictionary:
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
        user_choice = input('정렬 기준을 숫자로 입력하세요\n>_ ')
        user_choice = int(user_choice)
    except ValueError as e:
        print(f'\n입력 형식이 잘못되었습니다! 다시 입력해주세요 :( \n{e}')
        return print_sorted_planet_system(star_mass, planet_dictionary)

    if user_choice == 0:
        return

    update_all_planet_data(star_mass, planet_dictionary)

    print("\n" + "="*75)
    print(f"★ 현재 궤도 시스템 정보 요약 (중심 항성 질량: {star_mass:.4f} M☉) ★")
    print(f"등록된 총 행성 수: {len(planet_dictionary)}개")
    print("="*75)

    sorting_standards = {
        1: lambda x: x[0],
        2: lambda x: x[1]['peri_dist'],
        3: lambda x: x[1].get('speed_av', 0.0),
        4: lambda x: x[1].get('period', 0.0),
        5: lambda x: x[1].get('eccentricity', 0.0)
    }

    if user_choice in sorting_standards:
        sorted_planets = sorted(planet_dictionary.items(), key=sorting_standards[user_choice])
        for planet_name, planet_details in sorted_planets:
            print(f"▶ 행성명: [{planet_name}]")
            print(f"  - 근일점 좌표: ({planet_details['peri_pos'][0]:.3f}, {planet_details['peri_pos'][1]:.3f}) AU")
            print(f"  - 근일점 거리: {planet_details['peri_dist']:.4f} AU")
            print(f"  - 근일점 속력: {planet_details['peri_speed']:.2f} km/s")
            print(f"  - 평균 공전속력: {planet_details.get('speed_av', 0.0):.2f} km/s")
            print(f"  - 공전 주기:   {planet_details.get('period', 0.0):.4f} 년 (yr)")
            print(f"  - 궤도 장반경 (긴반지름): {planet_details.get('semi_major_axis', 0.0):.4f} AU")
            print(f"  - 궤도 단반경 (짧은반지름): {planet_details.get('semi_minor_axis', 0.0):.4f} AU")
            print(f"  - 궤도 이심률: {planet_details.get('eccentricity', 0.0):.4f}")
            print("-" * 75)
    else:
        return print_sorted_planet_system(star_mass, planet_dictionary)
