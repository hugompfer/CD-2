from tkinter import *
from view.newRoom import *
from model import chatClient
import threading
from tkinter import messagebox
from view.timeout import AddTime

class ChatView:
    def __init__(self,client):
        self.close = False
        self.messages = {}  # room:messages[]
        self.small_font = ('Verdana', 10)
        self.big_font = ('Verdana', 10)
        self.root=self.inicializeRoot()
        self.inicializeLabels()
        self.client = client
        self.client.addView(self)
        self.client.start()
        self.conversation = self.inicializeList() #messages text
        self.txtMessage = self.inicializeText() #user text
        self.inializeButtons()
        self.inicializeUserOnline() #list of users online
        self.roomsList = self.inicializeRoomsList() #list of rooms
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.mainloop()

    def inicializeRoot(self):
        root = Tk()
        root.title('Chat Service')
        root.resizable(False, False)
        root.geometry("600x480")
        return root

    def inicializeList(self):
        entry = Text(self.root, height=18, width=40, font=self.small_font)
        entry.place(relx=.5, rely=0.4, anchor="c")
        return entry

    def inicializeUserOnline(self):
        self.userOnline = Listbox(self.root, height=15, width=17)
        self.userOnline.place(relx=.89, rely=0.35, anchor="c")
        threadUsers = threading.Thread(target=self.updateUsers,
                                  args=())
        threadUsers.start()

    #update users list until closed
    def updateUsers(self):
        if not self.close:
            self.client.send("#users %s" % self.label2["text"].split()[2])
            threading.Timer(3, self.updateUsers).start()

    def inicializeRoomsList(self):
        listbox3 = Listbox(self.root, height=18, width=17)
        listbox3.place(relx=.12, rely=0.4, anchor="c")
        threadRooms = threading.Thread(target=self.updateRooms,
                                  args=())
        threadRooms.start()
        listbox3.bind("<<ListboxSelect>>", self.onSelectRoomsList)
        return listbox3

    # update rooms list until closed
    def updateRooms(self):
        if not self.close:
            self.client.send("#rooms")
            threading.Timer(1, self.updateRooms).start()

    #change room
    def onSelectRoomsList(self,evt):
        try:
            selected = self.roomsList.curselection()
            name = self.roomsList.get(selected[0])
            name=name.strip()
            if name != self.label2['text'].split()[2]:
                self.label2['text'] = "Chat Name: " + name
                self.client.send('#enter %s' %name)
                self.conversation.delete('1.0', END)
                self.checkMessage(name)
                self.insertMessagesIntoConversation()
        except:
           pass

    #insert into conversation text
    def insertMessagesIntoConversation(self):
        for msg in  self.messages[self.label2['text'].split()[2]]:
            self.conversation.insert(END,msg)

    def inicializeLabels(self):
        label1 = Label(self.root, text="Online users", font=self.small_font)
        label1.place(relx=.9, rely=.06, anchor="c")

        self.label2 = Label(self.root, text="Chat Name: Geral", font=self.small_font)
        self.label2.place(relx=.48, rely=.06, anchor="c")

        label3 = Label(self.root, text="Options", font=self.small_font)
        label3.place(relx=.9, rely=.63, anchor="c")

        label4 = Label(self.root, text="Rooms List", font=self.small_font)
        label4.place(relx=.11, rely=.06, anchor="c")

        label5 = Label(self.root, text="To send a private message:\n1.check the checkbutton\n                           2.write:username_to_send_message message", font=self.small_font)
        label5.place(relx=.25, rely=.90, anchor="c")

    def inicializeText(self):
        entry = Text(self.root, height=1.5, width=24, font=self.small_font)
        entry.place(relx=.42, rely=.8, anchor="c")
        return entry

    def inializeButtons(self):
        sender = Button( self.root, text="SEND", fg="Darkblue", command= self.send, height=2, width=9)
        sender.bind('<Return>', self.send)
        sender.place(relx=.68, rely=.8, anchor="c")
        self.root.bind('<Return>',  self.send)

        new = Button( self.root, text=" New ", fg="Green", command= self.new, height=1, width=9)
        new.place(relx=.9, rely=.7, anchor="c")

        leave = Button( self.root, text=" Timeout ", command=self.addTime, fg="blue",  height=1, width=9)
        leave.place(relx=.9, rely=.76, anchor="c")

        ban = Button(self.root, text=" Ban ", fg="Red", command=self.ban, height=1, width=9)
        ban.place(relx=.9, rely=.82, anchor="c")

        timeout = Button(self.root,text=" Exit ", fg="Orange",command= self.callback, height=1, width=9)
        timeout.place(relx=.9, rely=.88, anchor="c")

        self.radioSelected = False
        checkbox = Checkbutton(self.root, text="Private Message", command=self.select, height=1,  width=15)
        checkbox.place(relx=.12, rely=.8, anchor="c")

    def select(self):
        self.radioSelected=not self.radioSelected

    #send normal message or private message if checkbox is selectec
    def send(self,event=None):
        room=self.label2['text'].split()[2]
        msg=self.txtMessage.get(1.0, END)
        msg=msg.replace('\n', '')
        if self.radioSelected:
            self.client.send("#priv {0} {1}".format(msg.split()[0], msg.split(msg.split()[0])[1]))
        else:
            self.client.send("{0} {1}".format(room, msg))
        self.txtMessage.delete('1.0', END)

    #add message to a conversation, or if is not in room add to list of room messages
    def addToConversation(self,msg,room):
        if self.label2['text'].split()[2]==room or room==None:
            self.conversation.insert(END, msg)
        self.checkMessage(room)
        self.messages[room].append(msg)

    def checkMessage(self,name):
        try:
            if self.messages[name] == None:
                self.messages[name]=[]
        except:
            self.messages[name] = []

    #add to list of rooms a room
    def addToRooms(self,list):
        self.roomsList.delete(0, END)
        for item in list:
            if not item in self.roomsList.keys():
                self.roomsList.insert(END, item)

    def callback(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.exit()

    def exit(self):
        try:
            self.close=True
            self.client.send('#exit')
            self.root.destroy()
        except:
            self.root.destroy()

    #add user to users list
    def addToUser(self,list):
        self.userOnline.delete(0, END)
        for item in list:
            item = item.replace('\n', '')
            self.userOnline.insert(END, item)

    def new(self):
        new = NewRoom(self.client)

    #ban to user if is selected in users list
    def ban(self):
        if str(self.userOnline.curselection()) == "()":
            messagebox.showinfo("Erro", "Selecione o user a banir")
        else:
            position = self.userOnline.curselection()
            user=self.userOnline.get(position[0])
            user = user.replace('\n', '')
            self.userToDelete=user
            self.client.send('#ban {0} {1}'.format(self.label2['text'].split()[2],user))

    def deleteUser(self):
        self.userOnline.delete(self.userToDelete)

    #open new window to insert the time to timeout
    def addTime(self):
        if str(self.userOnline.curselection()) == "()":
            messagebox.showinfo("Erro", "Selecione o user a banir")
        else:
            position = self.userOnline.curselection()
            user = self.userOnline.get(position[0])
            user = user.replace('\n', '')
            new=AddTime(self.label2['text'].split()[2],user,self)

    def timeout(self,room,user, time):
        self.client.send('#timeout {0} {1} {2}'.format(room,user,time))







