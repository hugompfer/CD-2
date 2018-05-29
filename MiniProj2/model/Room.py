import datetime
from model import JsonHandler

class Room:
    def __init__(self, name, admin,bans=[],timeouts={}):
        self.users = []#user
        self.name = name #room name
        self.admin = admin #name of admin name
        self.bans =bans #name of banned users
        self.timeouts=timeouts #name of timeouts users
        self.messages=[] #room messages

    #exit user from room
    def exit(self,user):
        if user in self.users:
            self.users.remove(user)

    #user enter in room, check if is banned
    def enterUser(self,user):
        msg = 'Bem vindo a sala #' + self.name + ' ' + user.name
        if not user in self.users:
            if user.name in self.bans:
                msg = '\n'+user.name + ' estas banido da sala #' + self.name
            elif user.name in self.timeouts:
                if datetime.datetime.now()>=self.timeouts[user.name]:
                    del self.timeouts[user.name]
                    self.users.append(user)
                    msg = '\n'+user.name + ' já não estas banido da sala #' + self.name
                else:
                    msg ='\n'+ user.name + ' estas banido da sala até ' + self.timeouts[user.name].strftime("%Y-%m-%d %H:%M:%S")
            else:
                self.users.append(user)
            user.socket.sendall(JsonHandler.encode('#msg',msg,self.name).encode())
            self.messages.append(msg)

    #broadcast a message from user or administrator
    def broadcast(self, user, msg,isSuperModerator):
        if isSuperModerator:
            msg= '\n************* ANUNCIO ************* \n(Admin {0} - {1}) {2}'.format(user,datetime.datetime.now().strftime('%H:%M:%S'),msg)
        else:
            msg ='({0} - {1}) {2}'.format(user.name ,datetime.datetime.now().strftime('%H:%M:%S'),msg)
            msg=msg.replace('\n','')
            msg = msg+'\n'
        for u in self.users:
            u.socket.sendall(JsonHandler.encode('#msg','\n'+msg,self.name).encode())
        self.messages.append(msg)

    #ban a user if a supposed admin have permissions
    def ban(self,admin,userToBan):
        if admin.name != userToBan.name and userToBan in  self.users:
            if admin.name==self.admin :
                self.users.remove(userToBan)
                self.bans.append(userToBan.name)
                msg = ' O utilizador ' + userToBan.name + ' foi banido.'
                userToBan.socket.sendall(JsonHandler.encode('#msg', '\nFoste banido desta sala',self.name).encode())
                self.broadcast(admin,msg,False)
            else:
                msg = '\n'+admin.name +' não tem permissões para banir.'
                admin.socket.sendall(JsonHandler.encode('#msg',msg,self.name).encode())

    # timeout a user if a supposed admin have permissions
    def timeout(self,admin,userToTimeout,time):
        if admin.name != userToTimeout.name and userToTimeout in self.users:
            if admin.name == self.admin :
                self.users.remove(userToTimeout)
                msg = ' O utilizador ' + userToTimeout.name + ' foi banido temporariamente por '+str(time) +' minuto(s)'
                now = datetime.datetime.now()
                now_plus = now + datetime.timedelta(minutes=int(time))
                userToTimeout.socket.sendall(JsonHandler.encode('#msg', '\nFoste banido temporariamente por '+str(time) +' minuto(s)',self.name).encode())
                self.timeouts[userToTimeout.name]=now_plus
                self.broadcast(admin,msg,False)
            else:
                msg = admin.name + ' não tens permissões para dar timeouts.'
                admin.socket.sendall(JsonHandler.encode('#msg','\n'+msg,self.name).encode())

    #get all usernames
    def getUsers(self):
        list=[]
        for user in self.users:
            list.append(user.name)
        return list
