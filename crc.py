binary_string = '111100001111000000001111000011110000'
print(binary_string)

def generate_crc(data):
    polynomial = '1101'  # Example polynomial
    data = data + '000'  # Append zeros for CRC
    while '1' in data[:len(data) - len(polynomial) + 1]:
        pos = data.index('1')
        data = data[:pos] + ''.join(
            '0' if d == p else '1'
            for d, p in zip(data[pos:pos + len(polynomial)], polynomial)
        ) + data[pos + len(polynomial):]
    return data

print(generate_crc(binary_string))