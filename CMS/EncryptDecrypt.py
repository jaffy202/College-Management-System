import json
import rsa


class EnDecrypt:
    def __init__(self, keys_path):
        self.keys_path = keys_path
        self.public_key, self.private_key = self.load_keys_from_json()

    def load_keys_from_json(self):
        with open(self.keys_path, 'r') as f:
            keys_data = json.load(f)
            public_key_str = keys_data['public_key']
            private_key_str = keys_data['private_key']
        return rsa.PublicKey.load_pkcs1(public_key_str.encode()), rsa.PrivateKey.load_pkcs1(private_key_str.encode())

    def encrypt_data(self, data):
        return rsa.encrypt(data.encode(), self.public_key)

    def decrypt_data(self, data):
        return rsa.decrypt(data, self.private_key).decode()
