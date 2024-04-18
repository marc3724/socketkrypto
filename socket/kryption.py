from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


class CryptoHandler:
    def __init__(self, keyword, nonce):
        self.keyword = keyword
        self.nonce = nonce

    def encrypt_message(self, message):
        cipher = AES.new(self.keyword, AES.MODE_CBC, self.nonce)
        padded_message = pad(message.encode('utf-8'), AES.block_size)
        encrypted_message = cipher.encrypt(padded_message)
        print(f"aes encryption message = {encrypted_message}")
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        cipher = AES.new(self.keyword, AES.MODE_CBC, self.nonce)
        decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size)
        return decrypted_message.decode('utf-8')


def base64_encode(data):
    return base64.b64encode(data)


def base64_decode(data):
    return base64.b64decode(data)


