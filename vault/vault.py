import json

from .entry import Entry
from crypto.crypto_engine import CryptoEngine

class Vault:
    def __init__(self, crypto: CryptoEngine,filename = "vault.enc"):
        self.crypto = crypto
        self.filename = filename
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def save(self):
        data = []
        for e in self.entries:
            data.append(e.__dict__)     #добавляем как словарь

        json_str = json.dumps(data, ensure_ascii=False, indent=4).encode("utf-8")
        encrypted = self.crypto.encrypt(json_str)

        with open(self.filename, "wb") as f:
            f.write(encrypted)

    def load(self):
        with open(self.filename, "rb") as f:
            encrypted = f.read()

            decrypted_json = self.crypto.decrypt(encrypted).decode("utf-8")
            data = json.loads(decrypted_json)
            self.entries = [Entry(**d) for d in data]