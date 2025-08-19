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

    chunk_size = 16  # characters per chunk
    polynomial = ""

    if method == "crc":
        if len(sys.argv) < 4:
            print("Usage: python sender.py <file_path> crc <crc_polynomial>")
            return
        polynomial = sys.argv[3]
        crc.polynomial = polynomial  # set global polynomial

    try:
        with open(file_path, 'r') as f, socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"Connected to {HOST}:{PORT}")

            while True:
                data = f.read(chunk_size)
                if not data:
                    break

                if method == "checksum":
                    codeword = checksum.generate_checksum(data)
                elif method == "crc":
                    codeword = crc.generate_crc(data)
                else:
                    print(f"Error: Unknown method '{method}'")
                    return

                # Inject error with 20% probability
                if random.random() < 0.2:
                    codeword = injecterror.injecterror(codeword)

                message = f"{method}:{polynomial}:{codeword}\n"
                s.sendall(message.encode("utf-8"))
                print(f"Sent: {codeword}")

        print("File transfer complete.")

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return

if __name__ == "__main__":
    main()
