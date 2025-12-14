from vault.vault import Vault
from vault.entry import Entry
from crypto.crypto_engine import CryptoEngine
from client.backup_client import send_backup

try:
    key = open("master.key", "rb").read()
    print("Ключ загружен.")
except:
    key = CryptoEngine.generate_key()
    open("master.key", "wb").write(key)
    print("Создан новый ключ и сохранён в master.key")

crypto = CryptoEngine(key)

vault = Vault(crypto)
try:
    vault.load()
    print("База данных загружена.")
except:
    print("Создаем новую базу ...")

while True:
    cmd = input("Команда (Записать/Вывести/Бэкап/Выйти): ")

    if cmd == "Записать":
        title = input("Название сервиса: ")
        username = input("Логин: ")
        password = input("Пароль: ")
        note = input("Заметка: ")
        vault.add_entry(Entry(title, username, password, note))
        vault.save()
        print("Запись сохранена.")

    elif cmd == "Вывести":
        if not vault.entries:
            print("База пустая.")
        for e in vault.entries:
            print(f"{e.title}: {e.username}")


    elif cmd == "Бэкап":
        response = send_backup(vault.filename)
        if response is not None:
            print("Бэкап успешно завершен:", response.decode())
        else:
            print("Бэкап не был выполнен.")


    elif cmd == "Выйти":
        break

    print("\t")



