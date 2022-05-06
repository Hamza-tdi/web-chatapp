import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from threading import Lock


class Client:
    """
    For communication with server
    """
    HOST = 'localhost'
    PORT = 5500
    BUFSIZE = 512
    MAX_CONNECTIONS = 10
    ADDR = (HOST, PORT)

    def __init__(self, name):
        """
        init object and send name to server
        :params name: str
        """
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = []
        self.lock = Lock()
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(name)

    def receive_messages(self):
        """Handles receiving of messages."""
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZE).decode("utf8")
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print(f'[Exception] {e}')
                break

    def send_message(self, msg):
        """
        send messages to server
        :params msg:str
        :return: None
        """
        self.client_socket.send(bytes(msg, 'utf8'))
        if msg == '{quit}':
            self.client_socket.close()

    def get_messages(self):
        """
        return messages
        """
        messages_copy = self.messages[:]

        # assure memory is safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return messages_copy

