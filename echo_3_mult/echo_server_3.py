import os
import socket
import threading

HOST = "127.0.0.1"
PORT = 50131
event = threading.Event()


def handle_connection(sock, addr, set_event):
    with sock:
        print("Подключение по", addr)
        while True:
            # Recieve
            try:
                data = sock.recv(1024)
            except ConnectionError:
                print("Клиент внезапно отключился в процессе отправки данных на сервер")
                break
            if not data:
                break
            elif data == b'-off':
                set_event.set()
                quit()
            print(f"Получено: {data}, from: {addr}")
            data = data.upper()
            # Send
            print(f"Send: {data} to: {addr}")
            try:
                sock.sendall(data)
            except ConnectionError:
                print(f"Клиент внезапно отключился не могу отправить данные")
                break
        print("Отключение по", addr)


def close_server(wait_event):
    wait_event.wait()
    print("\nСервер выключен")
    os._exit(0)


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind((HOST, PORT))
        serv_sock.listen(1)
        close_thread = threading.Thread(target=close_server, args=(event, ))
        close_thread.start()
        while True:
            print("Ожидаю подключения....")
            sock, addr = serv_sock.accept()
            thread = threading.Thread(target=handle_connection, args=(sock, addr, event))
            print(thread)
            thread.start()
