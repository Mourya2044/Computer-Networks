
import injecterror

polynomials = {
    "CRC-8": "100000111",
    "CRC-10": "11000000011",
    "CRC-16": "11000000000000101",
    "CRC-32": "100000100110000010001110110110111",
}

polynomial = ""

def xor_division(dividend:str, divisor:str)->str:
    n = len(divisor)
    pick = n
    temp = dividend[:pick]
    
    while pick < len(dividend):
        if temp[0] == '1':
            temp = format(int(temp, 2)^int(divisor, 2), '0' + str(n) + 'b')
        temp = temp[1:]+dividend[pick]
        pick += 1
        
    if temp[0] == '1':
        temp = format(int(temp, 2)^int(divisor, 2), '0' + str(n) + 'b')
        
    return temp[1:]

def generate_crc(data):
    global polynomial
    if polynomial in polynomials:
        polynomial = polynomials[polynomial]

    dividend = data + '0'*(len(polynomial)-1)
    
    rem = xor_division(dividend, polynomial)
    
    data_to_send = data+rem
    return data_to_send

def verify_crc(data:str)->bool:
    global polynomial
    if polynomial in polynomials:
        polynomial = polynomials[polynomial]
        
    dividend = data
    
    rem = xor_division(dividend, polynomial)
    return int(rem, 2)==0

if __name__ == "__main__":
    binary_string = '1111000011110000000011101111'
    polynomial = "CRC-16"
    print(binary_string)
    data_to_send = generate_crc(binary_string)
    print(data_to_send)
    recieved_data = data_to_send
    # recieved_data = injecterror.injecterror(data_to_send, errcnt=2)
    print(recieved_data)
    print(verify_crc(recieved_data))
