binary_string = '111100001111000000001111000011110000'
# decimal_value = int(binary_string, 2)
# print(decimal_value)
# binary_string = format(decimal_value, 'b')
print(binary_string)

chunk = 16
bit_size = 4

def generate_checksum(data: str) -> str:
    n = len(data)
    if(n%chunk != 0):
        data = '0'*(chunk - n%chunk) + data
        n = len(data)
    
    words = [data[i:i+chunk] for i in range(0, n, chunk)]
    
    checksum_strings = []
    
    for word in words:
        numbers = [int(word[i:i+bit_size], 2) for i in range(0, chunk, bit_size)]
        checksum = sum(numbers)
        checksum_string = format(checksum, 'b')
        
        while len(checksum_string)>bit_size:
            checksum_string = '0'*(bit_size - len(checksum_string)%bit_size) + checksum_string
            numbers = [int(checksum_string[i:i+bit_size], 2) for i in range(0, len(checksum_string), bit_size)]
            checksum = sum(numbers)
            checksum_string = format(checksum, 'b')
        checksum_string_complemented = ''.join(['0' if i == '1' else '1' for i in checksum_string])
        checksum_strings.append(word+checksum_string_complemented)
    
    data_to_send = ''.join(checksum_strings)
    return data_to_send

def verify_checksum(data):
    n = len(data)
    word_size = chunk + bit_size
    if(n%word_size != 0):
        data = '0'*(word_size - n%word_size) + data
        n = len(data)
    
    words = [data[i:i+word_size] for i in range(0, n, word_size)]
    
    for word in words:
        numbers = [int(word[i:i+bit_size], 2) for i in range(0, word_size, bit_size)]
        # print(numbers)
        checksum = sum(numbers)
        checksum_string = format(checksum, 'b')
        
        while len(checksum_string)>bit_size:
            checksum_string = '0'*(bit_size - len(checksum_string)%bit_size) + checksum_string
            # print(checksum_string)
            numbers = [int(checksum_string[i:i+bit_size], 2) for i in range(0, len(checksum_string), bit_size)]
            checksum = sum(numbers)
            checksum_string = format(checksum, 'b')
        
        checksum_string_complemented = ''.join(['0' if i == '1' else '1' for i in checksum_string])
        # print(checksum_string_complemented)
        if checksum_string_complemented != '0'*bit_size:
            return False
    
    return True
            
            

import injecterror
        
        

data_to_send = generate_checksum(binary_string)
print(data_to_send)
# recieved_data = injecterror.injecterror('111100001111000000001111000011110000')
recieved_data = '111100001111000000001111000011110000'
isValid = verify_checksum(recieved_data)
print(isValid)