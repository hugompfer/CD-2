import threading
from model import filesUtils
import os
from model import Room
from model.JsonHandler import *
from model.Room import *

class Hall:
    def __init__(self):
        self.rooms = self.loadRooms()  # roomName:room
        self.userRooms = {}  # user:rooms[]
        self.options = ['#enter', '#exit', '#rooms', '#ban', '#timeout', '#priv', '#users','#messages'] #available options
        self.users = [] #users

    #save rooms information in file
    def saveRooms(self):
        try:
            rooms = self.getRoomsInformation()
            filesUtils.saveInFile(rooms, 'model/rooms2.txt')
            os.rename('model/rooms2.txt', 'model/roomsOriginal.txt')
        except:
            os.remove('model/roomsOriginal.txt')
            os.rename('model/rooms2.txt', 'model/roomsOriginal.txt')

    #for each room get information to save in file
    def getRoomsInformation(self):
        dict = {}
        for room in self.rooms.values():
            dict[room.name] = {
                'admin':room.admin,
                'bans':room.bans,
                'timeouts':room.timeouts
            }
        return dict

    #load from file the information of rooms
    def loadRooms(self):
        roomLoaded = filesUtils.loadFromFile('model/roomsOriginal.txt')
        if roomLoaded == None or len(roomLoaded) == 0:
            rooms = {}
            rooms['Geral'] = Room('Geral', None,[],{})
        else:
            rooms = {}
            for name, dic in roomLoaded.items():
                admin=dic['admin']
                bans = list(dic['bans'])
                timeouts=dic['timeouts']
                rooms[name.strip()] = Room(name.strip(),
                                           admin if admin==None else admin.strip(),
                                           bans,
                                           timeouts)
        return rooms

    #welcome to chat, insert into users and user:rooms and enter to room geral
    def welcome(self, user):
        room = self.rooms['Geral']
        self.userRooms[user] = []
        self.userRooms[user].append(room.name)
        room.enterUser(user)
        self.users.append(user)

    #exit from chat, remove user from rooms
    def exitUser(self, user):
        self.users.remove(user)
        for room in self.userRooms[user]:
            self.rooms[room].exit(user)
        msg = 'Até à proxima ' + user.name + '\n'
        user.socket.sendall(msg.encode())
        user.socket.close()

    #if message is a chat option
    def isOption(self, msg):
        for op in self.options:
            if msg.__contains__(op):
                return True
        return False

    #handle message received
    def handleUserMessage(self, user, msg):
        if self.isOption(msg) or user in self.userRooms:
            self.handleOptions(user, msg)

    #detect what option wanted
    def handleOptions(self, user, msg):
        if self.options[0] in msg:
            self.enterRoom(user, msg)
        elif self.options[1] in msg:
            self.exitUser(user)
        elif self.options[2] in msg:
            self.showRooms(user)
        elif self.options[3] in msg:
            self.ban(user, msg)
        elif self.options[4] in msg:
            self.timeout(user, msg)
        elif self.options[5] in msg:
            self.privateMessage(user, msg)
        elif self.options[6] in msg:
            self.showUserInRoom(user, msg)
        else:
            self.sendMessage(user,msg)

    # show all rooms in chat
    def showRooms(self, user):
        list = []
        for room in self.rooms:
            list.append(room)
        user.socket.sendall(JsonHandler.encode('#rooms', list, None).encode())

    #send message to users room or try to enter in room if he is banned
    def sendMessage(self,user,msg):
        if user in self.userRooms:
            room = msg.split()[0]
            if user.name in self.rooms[room].bans or user.name in self.rooms[room].timeouts:
                self.rooms[msg.split()[0]].enterUser(user)
            else:
                self.rooms[room].broadcast(user, msg.split(msg.split()[0], 1)[1], False)

    #show users in received room
    def showUserInRoom(self, user, msg):
        room = msg.split()[1]
        dic = JsonHandler.encode('#users', self.rooms[room].getUsers(), None)
        user.socket.sendall(dic.encode())

    #broadcast to all rooms a message
    def broadcastToAllRooms(self, user, msg):
        for room in self.rooms.values():
            room.broadcast(user, msg, True)

    #send a private message
    def privateMessage(self, user, msg):
        username = msg.split()[1]
        message = msg.split(username)[1]
        userToSend = self.getUser(username)
        if userToSend != False and username!=user.name:
            userToSend.socket.sendall(
                JsonHandler.encode('#msg', '\n(%s - mensagem privada) ' % user.name + message, None).encode())
            user.socket.sendall(
                JsonHandler.encode('#msg', '\n(%s - mensagem privada) ' % user.name + message, None).encode())

    #close all connections
    def closeAll(self):
        for user in self.users:
            msg = 'Até à proxima ' + user.name + '\n'
            user.socket.sendall(msg.encode())

    #get user from a username received
    def getUser(self, username):
        for user in self.users:
            if username.strip() == user.name.strip():
                return user
        return False

    #check if username is in room
    def userIsInThisRoom(self,username,roomName):
        for user,rooms in self.userRooms.items():
            if user.name==username:
                for room in rooms:
                    if roomName == room:
                        return True
        return False

    #ban user and save into file
    def ban(self, admin, msg):
        username = msg.split()[2]
        room = msg.split()[1]
        room = self.rooms[room]
        room.ban(admin, self.getUser(username))
        self.saveRooms()

    #timeout user and save into file
    def timeout(self, admin, msg):
        room = msg.split()[1]
        username = msg.split()[2]
        time = msg.split()[3]
        user = self.getUser(username)
        if user != False:
            room = self.rooms[room]
            room.timeout(admin, user, time)
            self.saveRooms()
        else:
            admin.socket.sendall(JsonHandler.encode('#msg','O utilizador ' + username + ' não está na sala').encode())

    def checkRoomAssocioate(self, user):
        if self.userRooms[user] == None:
            self.userRooms[user] = []

    #createa room/switch from rooms
    def enterRoom(self, user, msg):
        try:
            roomName = msg.split()[1]
            self.checkRoomAssocioate(user)
            if not roomName in self.rooms:
                room = Room(roomName, user.name,[],{})
                self.rooms[roomName] = room
                self.userRooms[user].append(roomName)
                self.rooms[roomName].enterUser(user)
                self.saveRooms()
            elif not roomName in self.userRooms[user]:
                room = self.rooms[roomName]
                self.userRooms[user].append(roomName)
                room.enterUser(user)
        except IndexError:
            user.socket.sendall(JsonHandler.encode('#msg','tem que indicar o nome da sala').encode())