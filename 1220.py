
# 입력 및 입력값 자료 저장
def star_input():
    try:
        res = input('중심 항성의 질량(kg), 추가하실 공전 행성의 개수를\n공백으로 구분하여 차례로 입력하세요\n>_ ').split()
        mass,N = float(res[0]), int(res[1])
        if mass <= 0 or N <= 0: raise ValueError("항성의 질량 및 행성의 개수는 0보다 커야 합니다.")
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
                name,x0,y0,vx0,vy0 = input('\n공전 행성의 \n이름,초기x좌표,초기y좌표,초기속도 x성분,초기속도 y성분\n을 공백으로 구분하여 차례로 입력하세요\n>_ ').split()
                planet_info[name] = {'init_pos':[float(x0),float(y0)],
                                     'init_velocity':[float(vx0),float(vy0)]}
                break
            except ValueError as e:
                print(f'\n입력 형식이 잘못되었습니다! 다시 입력해주세요. \n{e}\n')

    return star_mass, planet_info
    
input_values()