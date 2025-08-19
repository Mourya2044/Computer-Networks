import random

def injecterror(data: str, errcnt:int = 1) -> str:
    n = len(data)
    data_list = list(data)
    for _ in range(errcnt):
        index = random.randint(0, n-1)
        if data_list[index] == '1':
            data_list[index] = '0'
        else:
            data_list[index] = '1'
    return ''.join(data_list)