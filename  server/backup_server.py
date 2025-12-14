import socket
import os

BACKUP_DIR = "server_backups"

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

server = socket.socket()
server.bind(("0.0.0.0", 8888))
server.listen(5) #количетсво клиентов в очереди

print("Сервер запущен.")

while True:
    conn, addr = server.accept()
    print("Подключение: ", addr)
    try:
        #получаем имя файла для сравнения
        cmd_len = int.from_bytes(conn.recv(4), "big")
        cmd_bytes = conn.recv(cmd_len)
        command = cmd_bytes.decode("utf-8")

        if command == "LIST":
            # Отправляем список всех бэкапов через запятую
            files = [f for f in os.listdir(BACKUP_DIR) if f.endswith(".bin")]
            response = ",".join(files).encode("utf-8")
            conn.send(len(response).to_bytes(4, "big"))
            conn.send(response)

        elif command.startswith("GET "):
            filename = command[4:]
            filepath = os.path.join(BACKUP_DIR, filename)
            if os.path.exists(filepath):
                data = open(filepath, "rb").read()
                conn.send(len(data).to_bytes(8, "big"))
                conn.sendall(data)
            else:
                conn.send((0).to_bytes(8, "big"))

        elif command == "BACKUP":
            # получаем имя файла
            filename_size = int.from_bytes(conn.recv(4), "big")
            filename_bytes = conn.recv(filename_size)
            filename = filename_bytes.decode("utf-8")

            # получаем данные
            data_size = int.from_bytes(conn.recv(8), "big")
            data = b""

            while len(data) < data_size:
                packet = conn.recv(4096)
                if not packet:
                    break
                data += packet

            save_path = os.path.join(BACKUP_DIR, filename)
            with open(save_path, "wb") as f:
                f.write(data)
            conn.send(b"OK")
            print(f"Бэкап сохранён: {filename}")

        else:
            print("Неизвестная команда:", command)
            conn.send(b"ERROR")

    except Exception as e:
        print("Ошибка:", e)

        try:
            conn.send(b"ERROR")
        except:
            pass

    finally:
        conn.close()