import socket
import threading
from time import sleep

HOST = "127.0.0.1"
PORT = 13322

def receive_messages(soc):
    while True:
        sleep(0.2)
        data = soc.recv(1024)
        if not data:
            break
        print(data.decode('utf-8'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.connect((HOST, PORT))
    username = input("Bitte geben Sie Ihren Namen ein: ")
    soc.sendall(username.encode())
    receive_thread = threading.Thread(target=receive_messages, args=(soc,))
    receive_thread.start()

    while True:
        sleep(0.2)
        message = input()
        if message.lower() == 'quit':
            soc.close()
            break
        soc.sendall(message.encode())