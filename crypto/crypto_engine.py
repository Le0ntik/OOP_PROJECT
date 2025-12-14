from cryptography.fernet import Fernet

class CryptoEngine:
    def __init__(self, key):
        self.f = Fernet(key)

    def encrypt(self, data: bytes) -> bytes:
        return self.f.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        return self.f.decrypt(data)

    @staticmethod
    def generate_key():
        return Fernet.generate_key()