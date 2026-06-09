def orbital_period(Longer_Radius, Main_Mass, Planet):
    Period = (Longer_Radius**3 / Main_Mass)**0.5
    Planet['period'] = Period

def cal_ecc(Planet, Longer_Radius):
    Distance = Planet['peri_dist']
    Eccentricity = 1 - Distance / Longer_Radius
    if 0 < Eccentricity < 1:
        Planet['eccentricity'] = Eccentricity
    else:
        print('Error: wrong input')
        Planet['eccentricity'] = float('inf')
    return Eccentricity

def cal_speed_av(planet, L_radius, S_radius):
    if planet.get('eccentricity', float('inf')) != float('inf'):
        circumference = 2 * math.pi * L_radius
        speed_av = circumference / planet['period']
        planet['speed_av'] = speed_av
    else:
        planet['speed_av'] = float('inf')

def main():
    star_mass = float(input('중심 항성의 질량(M☉)을 입력하세요: '))
    planet_count = int(input('추가할 행성의 개수를 입력하세요: '))
    
    planet_info = {}
    
    G = 6.6743 * 10**-11
    AU_m = 1.496 * 10**11
    km_m = 1000
    Msolar_kg = 1.989 * 10**30

    for i in range(planet_count):
        name = input(f'\n[{i+1}/{planet_count}] 행성 이름을 입력하세요: ')
        x0 = float(input('근일점 x좌표(AU): '))
        y0 = float(input('근일점 y좌표(AU): '))
        v0 = float(input('근일점 속력(km/s): '))

        planet = {
            'star_mass': star_mass,
            'peri_pos': [x0, y0],
            'peri_dist': (x0**2 + y0**2)**0.5,
            'peri_speed': v0
        }
        
        try:
            r0_m = planet['peri_dist'] * AU_m
            v0_m = planet['peri_speed'] * km_m
            M_kg = star_mass * Msolar_kg
            
            longer_radius = (2 / r0_m - v0_m**2 / (G * M_kg))**-1 / AU_m
            planet['longer_radius'] = longer_radius
            
            eccentricity = cal_ecc(planet, longer_radius)
            
            if 0 < eccentricity < 1:
                shorter_radius = longer_radius * (1 - eccentricity**2)**0.5
            else:
                shorter_radius = 0.0
                planet['eccentricity'] = float('inf')
            planet['shorter_radius'] = shorter_radius
            
            orbital_period(longer_radius, star_mass, planet)
            cal_speed_av(planet, longer_radius, shorter_radius)
            
        except ZeroDivisionError:
            planet['longer_radius'] = 0.0
            planet['shorter_radius'] = 0.0
            planet['eccentricity'] = float('inf')
            planet['period'] = float('inf')
            planet['speed_av'] = float('inf')

        planet_info[name] = planet

    print("\n================ 최종 연산 결과 딕셔너리 ================")
    print(planet_info)

if __name__ == "__main__":
    main()
