"""
A TCP server for receiving and verifying messages using checksum or CRC error detection.
This script listens for incoming connections on a specified host and port.
It receives messages from a client, each message containing the error detection method,
polynomial (for CRC), error flag, and codeword, separated by colons.
Messages are processed line by line. The server verifies each message using the specified
error detection method (checksum or CRC) and counts the number of correctly detected errors.
Modules required:
    - socket: For network communication.
    - checksum: For checksum verification.
    - crc: For CRC verification.
Attributes:
    HOST (str): The IP address to bind the server.
    PORT (int): The port number to bind the server.
Workflow:
    1. Bind and listen on HOST:PORT.
    2. Accept a client connection.
    3. Receive data in chunks, buffering until a newline is found.
    4. For each message:
        - Parse method, polynomial, error flag, and codeword.
        - Verify codeword using the specified method.
        - Track correct detections.
    5. Print summary of correct detections after transfer is complete.
"""
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
        message_count = 0
        correct_detection_count = 0

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

                try:
                    method, polynomial, error, codeword = message.split(":", 3)
                    message_count += 1
                except ValueError:
                    print(f"Invalid message format: {message}")
                    continue

                is_valid = False
                if method == "checksum":
                    is_valid = checksum.verify_checksum(codeword)
                elif method == "crc":
                    is_valid = crc.verify_crc(codeword, polynomial)
                else:
                    print(f"Unknown method: {method}")
                    continue
                
                if is_valid == bool(error):
                    correct_detection_count += 1
                    
        print(f"Correct detection: {correct_detection_count}/{message_count}")           
            
