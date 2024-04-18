import socket
import threading

from dan_kryption import CryptoHandler, base64_decode, base64_encode

keyword = b"IT-Sikkerhed_PBA"
nonce = b"ZErhvervsakademi"

HOST = '0.0.0.0'
PORT = 12345

crypto_handler = CryptoHandler(keyword, nonce)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print('Waiting for a connection')
    connection, client_address = server_socket.accept()
    print('Accepted connection from', client_address)

    with connection:
        while True:
            data = connection.recv(1024)
            if not data:
                break

            decrypted_data = crypto_handler.decrypt_message(base64_decode(data))
            print("Received (encrypted):", data)
            print("Decrypted data:", decrypted_data)

            # Echo back the decrypted message to the client
            encrypted_response = crypto_handler.encrypt_message(decrypted_data)
            connection.sendall(base64_encode(encrypted_response))
