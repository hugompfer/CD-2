"""
 Implements a simple socket client

"""

import socket
import threading
from model import JsonHandler

class ChatClient:
    def __init__(self,host,port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = host

    #method to manage login/register
    def receiveCredentiais(self):
        while True:
            res = self.client_socket.recv(1024).decode()
            if "Correto" in res:
                self.view.goTochat()
                break
            elif 'sucesso' in res:
                self.view.showMessgae("Registo",res)
            else:
                self.view.showMessgae("Erro", res)

    #method to manage chat
    def handle_message(self):
            while True:
                # Read answer
                res = self.client_socket.recv(1024).decode()
                if "Até à proxima" in res or self.view.close:
                    break

                self.handle_options(res)
            self.view.exit()

    #method to start a thread to handle login/register
    def startCheckLogin(self):
        try:
            # Connect to server
            self.client_socket.connect((self.host, self.port))

            thread = threading.Thread(target=self.receiveCredentiais,
                                      args=())
            thread.start()

        except:
            print('Servidor encerrado!')

    # method to start a thread to handle messages from chat
    def start(self):
        try:

            thread = threading.Thread(target=self.handle_message,
                                      args=())
            thread.start()

        except:
            print('Servidor encerrado!')

    #add current view of client
    def addView(self, view):
        self.view = view

    #send message to server
    def send(self,msg):
        self.client_socket.sendall(msg.encode())

    #handle message from server
    def handle_options(self,msg):
        list=JsonHandler.decode(msg)
        for dic in list:
            if '#rooms' in dic['cod']:
                self.view.addToRooms(dic['result'])
            elif '#users' in dic['cod']:
                self.view.addToUser(dic['result'])
            else:
                if ' O utilizador  foi banido.' in dic['result']:
                    self.view.deleteUser()
                self.view.addToConversation(dic['result'],dic['room'])




