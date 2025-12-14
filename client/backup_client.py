import socket


def send_backup(filename):
    with open(filename, "rb") as f:
        data = f.read()

    s = socket.socket()
    s.connect(("127.0.0.1", 8888))
    s.sendall(data)
    response = s.recv(1024)
    print("Ответ сервера:", response)
    s.close()
    return response