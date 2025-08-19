import socket

HOST = '192.168.0.4'
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Server starting...")
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    with conn:
        while True:
            message = input("Send: ")
            conn.sendall(message.encode('utf-8'))
            recieved = conn.recv(1024)
            print(f"Recieved: {recieved.decode('utf-8')}")
