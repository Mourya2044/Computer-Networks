chunk = 16
bit_size = 4

def generate_checksum(data: str) -> str:
    n = len(data)
    if n % chunk != 0:
        data = '0'*(chunk - n % chunk) + data
        n = len(data)

    words = [data[i:i+chunk] for i in range(0, n, chunk)]
    checksum_strings = []

    for word in words:
        numbers = [int(word[i:i+bit_size], 2) for i in range(0, chunk, bit_size)]
        checksum = sum(numbers)

        while checksum >= (1 << bit_size):
            # fold carries
            checksum = (checksum >> bit_size) + (checksum & ((1 << bit_size)-1))

        checksum_string = format(checksum, '0{}b'.format(bit_size))
        # complement
        checksum_string_complemented = ''.join('0' if b == '1' else '1' for b in checksum_string)
        checksum_strings.append(word + checksum_string_complemented)

    return ''.join(checksum_strings)


def verify_checksum(data: str) -> bool:
    n = len(data)
    word_size = chunk + bit_size
    if n % word_size != 0:
        data = '0'*(word_size - n % word_size) + data
        n = len(data)

    words = [data[i:i+word_size] for i in range(0, n, word_size)]

    for word in words:
        numbers = [int(word[i:i+bit_size], 2) for i in range(0, word_size, bit_size)]
        checksum = sum(numbers)

        while checksum >= (1 << bit_size):
            checksum = (checksum >> bit_size) + (checksum & ((1 << bit_size)-1))

        if checksum != (1 << bit_size) - 1:  # must be all 1s
            return False

    return True
            

if __name__ == "__main__":        
    import injecterror
    binary_string = '111100001111000000001111000011110000'
    # decimal_value = int(binary_string, 2)
    # print(decimal_value)
    # binary_string = format(decimal_value, 'b')
    print(binary_string)
            
            

    data_to_send = generate_checksum(binary_string)
    print(data_to_send)
    recieved_data = data_to_send
    recieved_data = injecterror.injecterror(data_to_send, errcnt=2)
    print(recieved_data)
    isValid = verify_checksum(recieved_data)
    print(isValid)