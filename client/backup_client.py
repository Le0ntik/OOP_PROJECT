import socket
from datetime import datetime


def generate_backup_name():
    timestamp = datetime.now().strftime("%H-%M-%S_%d-%m-%Y")
    return f"backup_{timestamp}.bin"


def send_backup(filename):
    backup_name = generate_backup_name()

    with open(filename, "rb") as f:
        data = f.read()

    s = socket.socket()
    s.connect(("127.0.0.1", 8888))

    cmd = "BACKUP".encode("utf-8")
    s.send(len(cmd).to_bytes(4, "big"))
    s.send(cmd)

    # отправляем имя файла
    filename_bytes = backup_name.encode("utf-8")
    s.send(len(filename_bytes).to_bytes(4, "big"))
    s.send(filename_bytes)

    # отправляем размер данных
    s.send(len(data).to_bytes(8, "big"))
    s.sendall(data)

    response = s.recv(1024)
    s.close()

    if response == b"OK":
        print(f"Бэкап успешно отправлен на сервер: {backup_name}")
    else:
        print("Ошибка отправки бэкапа на сервер.")

    return backup_name


def list_server_backups():
    #Получаем список всех бэкапов на сервере
    s = socket.socket()
    s.connect(("127.0.0.1", 8888))

    cmd = "LIST".encode("utf-8")
    s.send(len(cmd).to_bytes(4, "big"))
    s.send(cmd)

    resp_len = int.from_bytes(s.recv(4), "big")
    resp = s.recv(resp_len).decode("utf-8")
    s.close()

    if not resp:
        return []
    return resp.split(",")

def choose_backup_server():
    #Выбор бэкапа с сервера
    backups = list_server_backups()
    if not backups:
        print("Бэкапы на сервере не найдены.")
        return None

    print("\nДоступные бэкапы на сервере:")
    for i, b in enumerate(backups, 1):
        print(f"{i}. {b}")

    choice = input("Введите номер бэкапа: ").strip()
    if not choice.isdigit():
        return None
    index = int(choice) - 1
    if index < 0 or index >= len(backups):
        return None

    return backups[index]


def download_backup(backup_name):
    s = socket.socket()
    s.connect(("127.0.0.1", 8888))

    cmd = f"GET {backup_name}".encode("utf-8")
    s.send(len(cmd).to_bytes(4, "big"))
    s.send(cmd)

    # получаем размер файла
    data_size = int.from_bytes(s.recv(8), "big")
    if data_size == 0:
        print("Файл не найден на сервере.")
        s.close()
        return False

    # сразу читаем весь файл
    data = s.recv(data_size)
    s.close()

    with open("vault.enc", "wb") as f:
        f.write(data)

    print(f"Бэкап {backup_name} загружен и восстановлен.")
    return True
