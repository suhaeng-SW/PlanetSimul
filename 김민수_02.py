def cal_speed_av(planet, L_radius, S_radius):
    import math
    if planet.get('eccentricity', float('inf')) != float('inf'):
        circumference = 2 * math.pi * L_radius
        speed_av = circumference / planet['period']
        planet['speed_av'] = speed_av
    else:
        planet['speed_av'] = float('inf')

def print_final(planet_info):
    print("\n= 전체 궤도 시스템 정보 =")
    
    for name, planet in planet_info.items():
        
        peri_dist = planet['peri_dist']       # 근일점 거리
        peri_speed = planet['peri_speed']     # 근일점 속력
        eccentricity = planet['eccentricity'] # 이심률
        period = planet['period']             # 공전 주기
        speed_av = planet['speed_av']         # 평균 공전 속력
        
        print(f"[{name}] 행성")
        print(f" - 근일점 거리: {peri_dist:.2f} AU")
        print(f" - 근일점 속력: {peri_speed:.2f} km/s")
        print(f" - 이심률: {eccentricity:.4f}")
        print(f" - 공전 주기: {period:.2f} yr")
        print(f" - 평균 속력: {speed_av:.2f} AU/yr")
        print("-")
