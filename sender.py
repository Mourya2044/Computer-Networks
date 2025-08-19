import socket

HOST = '127.0.0.1'
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        recieved = s.recv(1024)
        print(f"Recieved: {recieved.decode('utf-8')}")
        message = input("Send: ")
        s.sendall(message.encode('utf-8'))