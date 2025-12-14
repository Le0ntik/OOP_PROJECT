from vault.vault import Vault
from vault.entry import Entry
from crypto.crypto_engine import CryptoEngine
from client.backup_client import send_backup, choose_backup_server, download_backup

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
    cmd = input("Команда (Записать/Вывести/Бэкап/Восстановить/Выйти): ").strip().lower()

    if cmd == "записать":
        title = input("Название сервиса: ")
        username = input("Логин: ")
        password = input("Пароль: ")
        note = input("Заметка: ")
        vault.add_entry(Entry(title, username, password, note))
        vault.save()
        print("Запись сохранена.")

    elif cmd == "вывести":
        if not vault.entries:
            print("База пустая.")
        for e in vault.entries:
            print(f"{e.title}: {e.username}")

    elif cmd == "бэкап":
        try:
            backup_name = send_backup(vault.filename)
            print(f"Бэкап успешно завершен: {backup_name}")

        except Exception as e:
            print("Ошибка при отправке бэкапа на сервер:", e)

    elif cmd == "восстановить":
        backup_name = choose_backup_server()
        if backup_name:
            if download_backup(backup_name):
                vault.load()

    elif cmd == "выйти":
        break

    print("\t")
