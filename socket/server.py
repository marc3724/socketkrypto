import socket
import threading
from kryption import CryptoHandler, base64_decode, base64_encode

keyword = b"IT-Sikkerhed_PBA"
nonce = b"ZErhvervsakademi"

crypto_handler = CryptoHandler(keyword, nonce)

def handle_client(client_socket, addr):
    try:
        while True:
            encryptedMessage = client_socket.recv(1024)
            print(f"base64 encrypted message: {encryptedMessage}")
            request = crypto_handler.decrypt_message(base64_decode(encryptedMessage))
            # receive, decrypt and print client messages
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break
            print(f"Received from {addr}: {request}")

            # convert and send accept response to the client
            response = "accepted"
            encrypted_response = crypto_handler.encrypt_message(response)
            client_socket.send(base64_encode(encrypted_response))

    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")

def run_server():
    server_ip = "127.0.0.1"  # server hostname or IP address
    port = 8000  # server port number
    # create a socket object
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to the host and port
        server.bind((server_ip, port))
        # listen for incoming connections
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while True:
            # accept a client connection
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            # start a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()

run_server()


