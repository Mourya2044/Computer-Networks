"""
sender.py
A Python script to send file data over a TCP socket using either checksum or CRC error detection methods.
Each chunk of the file is processed to generate a codeword (checksum or CRC), with optional error injection.
The codeword and metadata are sent to a receiver server.
Usage:
    python sender.py <file_path> <method> [crc_polynomial]
Arguments:
    file_path         Path to the input file to be sent.
    method            Error detection method: "checksum" or "crc".
    crc_polynomial    (Required if method is "crc") Polynomial to use for CRC calculation.
Modules:
    socket            For network communication.
    sys               For command-line argument handling.
    checksum          Custom module for checksum generation.
    crc               Custom module for CRC generation.
    injecterror       Custom module for error injection.
    random            For probabilistic error injection.
Functions:
    main()            Handles argument parsing, file reading, codeword generation, error injection, and data transmission.
Notes:
    - Data is sent in chunks of 16 characters.
    - With 20% probability, an error is injected into the codeword before sending.
    - The message format sent to the receiver is: "<method>:<polynomial>:<error>:<codeword>\n"
    - Requires a receiver server listening on HOST:PORT.
"""
import socket
import sys
import checksum
import crc
import injecterror
import random

HOST = '127.0.0.1'
PORT = 3000

SRC_ADDR = "00000001"
DEST_ADDR = "00000010"
CODEWORD_SIZE = 64
HEADER_SIZE = 16   # 8 src + 8 dest
PAYLOAD_SIZE = CODEWORD_SIZE - HEADER_SIZE  # 48 bits

def main():
    if len(sys.argv) < 3:
        print("Usage: python sender.py <file_path> <method> [crc_polynomial]")
        return

    file_path = sys.argv[1]
    method = sys.argv[2]

    chunk_size = PAYLOAD_SIZE
    polynomial = ""

    if method == "crc":
        if len(sys.argv) < 4:
            print("Usage: python sender.py <file_path> crc <crc_polynomial>")
            return
        polynomial = sys.argv[3]
        # crc.polynomial = polynomial  # set global polynomial

    try:
        with open(file_path, 'r') as f, socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"Connected to {HOST}:{PORT}")

            while True:
                data = f.read(PAYLOAD_SIZE - HEADER_SIZE)  # leave space for header inside 64 bits
                if not data:
                    break

                # Combine header + payload
                frame_data = SRC_ADDR + DEST_ADDR + data

                # Generate full codeword (header+payload protected)
                if method == "checksum":
                    codeword = checksum.generate_checksum(frame_data)
                elif method == "crc":
                    codeword = crc.generate_crc(frame_data, polynomial)
                else:
                    print(f"Error: Unknown method '{method}'")
                    return

                # Inject error with 20% probability
                error = 0
                if random.random() < 0.2:
                    codeword = injecterror.injecterror(codeword)
                    error = 1

                # Pad or truncate to 64 bits
                # if len(codeword) < CODEWORD_SIZE:
                #     codeword = codeword.ljust(CODEWORD_SIZE, "0")
                # else:
                #     codeword = codeword[:CODEWORD_SIZE]

                # Send
                message = f"{method}:{polynomial}:{error}:{codeword}\n"
                s.sendall(message.encode("utf-8"))
                print(f"Sent frame: {message} (len={len(codeword)})")


        print("File transfer complete.")

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return

if __name__ == "__main__":
    main()
