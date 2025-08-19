import socket
import checksum
import crc

HOST = '127.0.0.1'
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(message)
            method, polynomial, codeword = message.split(':', 2)

            is_valid = False
            if method == "checksum":
                is_valid = checksum.verify_checksum(codeword)
            elif method == "crc":
                crc.polynomial = polynomial
                is_valid = crc.verify_crc(codeword)

            if is_valid:
                print(f"Received: {codeword} - Data is valid.")
            else:
                print(f"Received: {codeword} - Data is invalid.")