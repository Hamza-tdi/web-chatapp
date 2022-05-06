import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from person import Person


# Constant variables
HOST = 'localhost'
PORT = 5500
BUFSIZE = 512
MAX_CONNECTIONS = 10
ADDR = (HOST, PORT)


# Global variables
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
persons = []


def broadcast(msg, name):
    """
    send messages to clients
    :params
    msg: bytes
    name: str
    :return None
    """
    for person in persons:
        client = person.client
        client.send(msg)


def client_communication(person):
    """
    handle client communication
    :params person: Person
    """
    client = person.client
    addr = person.addr

    name = client.recv(BUFSIZE).decode("utf8")
    person.set_name(name)
    msg = bytes(f'{name}:{addr} has joined the chat', 'utf8')
    broadcast(msg, '')

    while True:
        try:
            msg = client.recv(BUFSIZE)
            if msg == bytes("{quit}", "utf8"):
                client.close()
                persons.remove(person)
                broadcast(bytes(f'{name} has left the chat ...', "utf8"), '')
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else:
                msg = bytes(f'{name}: {msg.decode("utf8")}', 'utf8')
                broadcast(msg, name)
                print(f"{name}: ", msg.decode("utf8"))
        except Exception as e:
            client.close()
            print(f'[Exception] {e}')
            break


def wait_for_connections():
    run = True
    while run:
        try:
            client, addr = SERVER.accept()
            person = Person(addr, client)
            persons.append(person)
            print(f'[CONNECTION] {addr} connected to the server at {time.time()}')
            Thread(target=client_communication, args=(person,)).start()
        except Exception as e:
            print(f'[FAILURE] {e}')


if __name__ == '__main__':
    SERVER.listen(MAX_CONNECTIONS)
    print('waiting')
    ACCEPT_THREADS = Thread(target=wait_for_connections)
    ACCEPT_THREADS.start()
    ACCEPT_THREADS.join()
