import socket
import sys
import checksum
import crc
import injecterror
import random

HOST = '127.0.0.1'
PORT = 3000

def main():
    if len(sys.argv) < 3:
        print("Usage: python sender.py <file_path> <method> [crc_polynomial]")
        return

    file_path = sys.argv[1]
    method = sys.argv[2]

    try:
        with open(file_path, 'r') as f:
            data = f.read().strip()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return

    codeword = ""
    if method == "checksum":
        codeword = checksum.generate_checksum(data)
    elif method == "crc":
        if len(sys.argv) < 4:
            print("Usage: python sender.py <file_path> crc <crc_polynomial>")
            return
        crc.polynomial = sys.argv[3]
        codeword = crc.generate_crc(data)
    else:
        print(f"Error: Unknown method '{method}'")
        return

    error = random.randint(0, 1)
    if(error == 1):
        codeword = injecterror.injecterror(codeword)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(f"{method}:{crc.polynomial if method == 'crc' else ''}:{codeword}".encode('utf-8'))
        print(f"Sent: {codeword}")

if __name__ == "__main__":
    main()
