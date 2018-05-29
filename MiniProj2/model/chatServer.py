"""
 Implements a simple socket server

"""

import socket
import threading
from model.Hall import Hall
from model.manager import *

class ChatServer:
    def __init__(self):
        self.port = 8000
        self.host = '0.0.0.0'
        self.hall=Hall()
        self.manager=Manager()
        self.close=False

    #method to handle the credentials from client
    def checkCredentials(self,client_connection):
        while True:
            credentials = client_connection.recv(1024).decode()
            info=credentials.split(':')[1]
            username = info.split('-')[0]
            username = username.replace('\n', '')
            pw = info.split('-')[1]
            pw = pw.replace('\n', '')
            if 'Login' in credentials:
                if(self.manager.isUser(username,pw)):
                    user = User(client_connection, username.strip())
                    client_connection.sendall("Correto".encode())
                    break
                else:
                    client_connection.sendall("Credentiais erradas".encode())
            else:
                client_connection.sendall(self.manager.register(username,pw).encode())
        return user

    #method to handle chat messages from client
    def handle_client(self, client_connection):
        user= self.checkCredentials(client_connection)
        self.hall.welcome(user)
        while True:
            try:
                if self.close:
                    break
                    # Print message from client
                msg = client_connection.recv(1024).decode()
                    # print('Received:', msg)
                if '#sair' in msg:
                    self.hall.handleUserMessage(user, msg)
                    break
                else:
                    self.hall.handleUserMessage(user, msg)
            except:
                break
        # Close client connection
        print('Client disconnected...')
        client_connection.close()

    #method to handle message from admin shell
    def handle_admin(self):
        print('Nome de administrador:')
        msg = input('> ')
        admin=msg
        while True:
            msg = input('> ')
            if   "broadcast" in msg:
                self.hall.broadcastToAllRooms(admin,msg.split(msg.split()[0])[1])
            elif "shutdown" in msg:
                self.hall.saveRooms()
                self.hall.closeAll()
                self.close = True
                self.server_socket.close()
                break


    def createSocket(self):
        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(1)
        return server_socket;


    def start(self):
        self.server_socket= self.createSocket()

        threadAdmin = threading.Thread(target=self.handle_admin,
                                       args=())
        threadAdmin.start()
        try:
            while True:
                # Wait for client connections
                client_connection, client_address = self.server_socket.accept()

                threadUser = threading.Thread(target=self.handle_client,
                                          args=(client_connection,))
                threadUser.start()

        except:
            self.hall.saveRooms()
            self.server_socket.close()

