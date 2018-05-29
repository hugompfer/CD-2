from model.User import User
from model import filesUtils
import os

class Manager:

    def __init__(self):
        self.users=self.loadUsers()#username:pw

    #load users credentials from file
    def loadUsers(self):
        roomLoaded = filesUtils.loadFromFile('model/usersOriginal.txt')
        users = {}
        if roomLoaded == None or len(roomLoaded) == 0:
            return users
        else:
            for username, pw in roomLoaded.items():
                users[username] = pw
        return users

    #check if credentials exists
    def isUser(self,username, pw):
        if username.strip() in self.users.keys():
            if self.users[username.strip()].strip() == pw:
                return True
        return False

    #save users credentials to file
    def saveUsers(self):
        try:
            filesUtils.saveInFile(self.users, 'model/users1.txt')
            os.rename('model/users1.txt', 'model/usersOriginal.txt')
            """threading.Timer(5, self.saveAdministrators).start()"""
        except:
            os.remove('model/usersOriginal.txt')
            os.rename('model/users1.txt', 'model/usersOriginal.txt')

    #register username,pw into file, returns error message if something is wrong
    def register(self,username,pw):
        if(not username or not pw):
            return 'Credenciais inválidas!'
        if username.strip() in self.users.keys():
            return 'Username existente!'
        else:
            self.users[username.strip()]=pw.strip()
            self.saveUsers()
            return 'Registo efetuado com sucesso!'

