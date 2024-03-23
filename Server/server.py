import socket
import json
import classes.classes as cl
import threading

HOST = "127.0.0.1"
PORT = 13322

def load_locale(Language : str = "de"):
    """Load locale.json and saves it in global dictonary"""
    try:
        with open("./Server/locale.json", encoding="utf-8") as f:
            load_locale = json.load(f)
            return load_locale[Language]
    except:
        print("locale not found, loading english...")
        with open("./Server/locale.json", encoding="utf-8") as f:
            load_locale = json.load(f)
            return load_locale["en"]

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"{locale['server_start_msg']} {host}:{port}")

    while True:
        client_socket, address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

def handle_client(client_socket, address):

    print(f"{locale['new_client_connection']} {address[0]}:{address[1]}")
    # Create new client object and connect to the group list
    try:
        username = client_socket.recv(1024).decode('utf-8')
        client = None
        for c in cl.clients:
            if(c.address == address):
                c.username = username
                c.socket = client_socket
                c.address = address
                client = c
        if client is None:
            client = cl.Client(username,client_socket, address)
            cl.clients.append(client)
        while True:
            try:
                data = client_socket.recv(1024)
            except:
                break
            if not data:
                remove_client(client)
                break
            if(data.decode(encoding='UTF-8')) == 'IG!veUp':
                remove_client(client)
                return
            handle_client_request(client,data)
    except Exception as e:
        print(e.with_traceback(None))   

def handle_client_request(client: cl.Client, data: bytes):
    """Handle a message from one of the clients and check for Commands"""
    msg = data.decode('utf-8')
    # Check for commands first
    if msg.startswith('/'):
        handle_client_command(client, msg)
    else:
        handle_client_message(client, msg)

def  handle_client_command(client: cl.Client, cmd: str):
    """Handles all known commands"""
    print(f"{locale['handle_client_command_user']} {client.username}, {locale['handle_client_command_address']} {client.address}, {locale['handle_client_command_cmd']} {cmd}")
    command = cmd.split(" ")[0].split("/")[1].strip().lower()
    parameters = cmd.split(" ",2)[1:]
    match (command):
        case 'nick':
            for user in cl.clients:
                if user == client:
                    user.username = parameters[0]
        case _:
            client.socket.sendall(locale['wrong_CMD'].encode())

def handle_client_message(client: cl.Client, msg:str):
    """Handles all Chat Messages"""
    # Broadcast to everyone but the sender
    for user in cl.clients:
        if user != client:
            #if(check_client_alive(user)):
            try:
                user.socket.sendall((client.username + ": " + msg).encode())
            except:
                check_client_alive(user)

def check_client_alive(client: cl.Client) -> bool:
    try:
        char =  client.socket.recv(1,socket.MSG_PEEK)
        if char:
            return True
        else:
            remove_client(client)
            return False
    except Exception as e:
        remove_client(client)
        return False

def remove_client(client: cl.Client):
    """Remove a client from the clients list"""
    try:
        print(f"{locale['client_disconnect1']} {client.username} | {client.address} {locale['client_disconnect2']}")
        cl.clients.remove(client)
        client.socket.close()
    except ValueError:
        pass  # Ignore if not in list (e.g. during shutdown)
    return


if __name__ == "__main__":
    language = input("Please  enter your preferred Language [de/en/es/fr/nl]: ")
    locale = load_locale(language.lower()) #  Load german locale by default
    start_server(HOST, PORT) # Start Server on given host and port and wait for connections
