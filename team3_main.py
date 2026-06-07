from 최무율 import *
from 이원준 import *
#from 김민수 import *

M,I = input_values()
for planet in I.values():
    a,b = cal_oval(M,planet)
while True:
    order = input_manual()
    if order == 0: break
    elif order == 4: sort_and_print(M,I)
