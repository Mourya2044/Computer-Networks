import socket
import checksum
import crc

HOST = '127.0.0.1'
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        buffer = ""

        while True:
            data = conn.recv(1024)
            if not data:
                print("File transfer complete.")
                break

            buffer += data.decode("utf-8")

            # Process messages separated by newline
            while "\n" in buffer:
                message, buffer = buffer.split("\n", 1)
                if not message.strip():
                    continue

                # print(f"Raw message: {message}")

                try:
                    method, polynomial, codeword = message.split(":", 2)
                except ValueError:
                    print(f"Invalid message format: {message}")
                    continue

                is_valid = False
                if method == "checksum":
                    is_valid = checksum.verify_checksum(codeword)
                elif method == "crc":
                    crc.polynomial = polynomial
                    is_valid = crc.verify_crc(codeword)
                else:
                    print(f"Unknown method: {method}")
                    continue

                if is_valid:
                    print(f"Received: {codeword} ✅ Data is valid.")
                else:
                    print(f"Received: {codeword} ❌ Data is invalid.")
