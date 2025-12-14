import socket

server = socket.socket()
server.bind(("0.0.0.0", 8888))
server.listen(1) #количетсво клиентов в очереди

print("Сервер запущен.")

while True:
    conn, addr = server.accept()
    print("Подключение: ", addr)

    data = conn.recv(10000000) #принимает 10мб
    with open("backup.bin", "wb") as f:
        f.write(data)

    conn.send(b"OK")
    conn.close()