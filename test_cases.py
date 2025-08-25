import checksum
import crc
import injecterror

binary_string = ["0100100001100101011011000110110001101111", "11110000111100001111", "0000000000000000", "1111111111111111", ""]
polynomials = {
    "CRC-8":  "100000111",
    "CRC-10": "11000000011",
    "CRC-16": "11000000000000101",
    "CRC-32": "100000100110000010001110110110111",
}

for word in binary_string:
    codeword_checksum = checksum.generate_checksum(word)
    print("[Checksum] codeword: ", codeword_checksum)

    correct_data = checksum.verify_checksum(codeword_checksum)
    print("[Checksum] correct data recieved: ", correct_data)

for key in polynomials:
    print()
    for word in binary_string:
        codeword_crc = crc.generate_crc(word, key)
        print(f"[CRC][{key}] codeword: ", codeword_crc)

        correct_data = crc.verify_crc(codeword_crc, key)
        print(f"[CRC][{key}] correct data recieved: ", correct_data)

