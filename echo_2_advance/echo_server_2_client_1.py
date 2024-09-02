import socket

HOST = "127.0.0.1"
PORT = 50432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    while True:
        data = input("Напечатайте сообщение для отправки: ")
        if data == "-stop":
            break
        elif data == "":
            print("Запрос должен что то содержать!!")
            continue
        data_bytes = data.encode()
        try:
            sock.sendall(data_bytes)
            data_bytes = sock.recv(1024)
        except (ConnectionResetError, ConnectionAbortedError):
            print("Сервер отключился")
            break
        data = data_bytes.decode()
        print("Received:", data)

