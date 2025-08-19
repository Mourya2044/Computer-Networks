polynomial = "1001"

def xor_division(dividend:str, divisor:str)->str:
    n = len(divisor)
    pick = n
    temp = dividend[:pick]
    
    while pick < len(dividend):
        if temp[0] == '1':
            temp = format(int(temp, 2)^int(divisor, 2), '0{}b'.format(n))
        temp = temp[1:]+dividend[pick]
        pick += 1
        
    if temp[0] == '1':
        temp = format(int(temp, 2)^int(divisor, 2), '0{}b'.format(n))
        
    return temp[1:]

def generate_crc(data):
    dividend = data + '0'*(len(polynomial)-1)
    
    rem = xor_division(dividend, polynomial)
    
    data_to_send = data+rem
    return data_to_send

def verify_crc(data:str)->bool:
    dividend = data
    
    rem = xor_division(dividend, polynomial)
    return int(rem, 2)==0

if __name__ == "__main__":
    import injecterror
    binary_string = '1111000011110000000011101111'
    print(binary_string)
    data_to_send = generate_crc(binary_string)
    print(data_to_send)
    recieved_data = data_to_send
    recieved_data = injecterror.injecterror(data_to_send, errcnt=2)
    print(recieved_data)
    print(verify_crc(recieved_data))