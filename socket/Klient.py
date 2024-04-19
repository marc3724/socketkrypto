import socket
from kryption import CryptoHandler, base64_decode, base64_encode

keyword = b"IT-Sikkerhed_PBA"
nonce = b"ZErhvervsakademi"

crypto_handler = CryptoHandler(keyword, nonce)

def run_client(data):
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "192.168.68.100"  # replace with the server's IP address
    server_port = 8000  # replace with the server's port number
    # establish connection with server
    client.connect((server_ip, server_port))
    print("Connected to server")

    try:
        while True:
            # get input message from user and send it to the server
            #msg = input("Enter message: ")
            msg = data
            encrypted_message = crypto_handler.encrypt_message(msg)
            client.send(base64_encode(encrypted_message))

            # receive message from the server
            response = client.recv(1024)
            response = crypto_handler.decrypt_message(base64_decode(response))

            # if server sent us "closed" in the payload, we break out of
            # the loop and close our socket
            if response.lower() == "closed":
                break

            print(f"Received: {response}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # close client socket (connection to the server)
        client.close()
        print("Connection to server closed")


#run_client()


