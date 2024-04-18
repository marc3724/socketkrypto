import socket
from dan_kryption import CryptoHandler, base64_encode, base64_decode

keyword = b"IT-Sikkerhed_PBA"
nonce = b"ZErhvervsakademi"

crypto_handler = CryptoHandler(keyword, nonce)

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print('Connected to server')

    while True:
        message = input("Write your message (Write 'quit' to exit): ")
        if message.lower() == 'quit':
            break

        encrypted_message = crypto_handler.encrypt_message(message)
        client_socket.sendall(base64_encode(encrypted_message))

        received_data = client_socket.recv(1024)

        if not received_data:
            print("Server did not respond.")
            continue

        decrypted_data = crypto_handler.decrypt_message(base64_decode(received_data))
        print("Server response:", decrypted_data)
