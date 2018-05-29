from model.chatClient import ChatClient
from view.chatView import *
from tkinter import messagebox
from tkinter import *

class LoginView:
    def __init__(self):
        self.client = ChatClient('127.0.0.1', 8000)
        self.client.startCheckLogin()
        self.client.addView(self)
        self.small_font = ('Verdana', 10)
        self.big_font = ('Verdana', 10)
        self.root=self.inicializeRoot()
        self.photo= PhotoImage(file="images/chat.gif")
        self.incializeLabels()
        self.txtUser = self.incializeTxtUser()
        self.txtPW = self.incializeTxtPW()
        self.btnEnterUser = self.inicializeBtnEnterUser()
        self.btnRegister=self.inicializeBtnEnterRegister()
        self.username=None
        self.root.mainloop()

    def inicializeRoot(self):
        root =Tk()
        root.title('Chat Service')
        root.resizable(False, False)
        root.configure(background='lightGrey')
        root.geometry("500x490")
        return root

    def incializeLabels(self):
        labelUser = Label(self.root, text="Please insert your Username.", font=self.small_font, bg="lightgrey")
        labelUser.place(relx=.5, rely=.38, anchor="c")

        labelPW = Label(self.root, text="Please insert your Password.", font=self.small_font, bg="lightgrey", )
        labelPW.place(relx=.5, rely=.55, anchor="c")

        labelPhoto = Label(self.root, image=self.photo)
        labelPhoto.place(relx=.515, rely=0.15, anchor="c")

    def incializeTxtUser(self):
        entry = Entry(self.root, name="text2", font=self.big_font)
        entry.config(width=30)
        entry.place(relx=.5, rely=.45, anchor="c")
        return entry

    def incializeTxtPW(self):
        entry =Entry(self.root, name="text4", show="*", font=self.big_font)
        entry.place(relx=.5, rely=.60, anchor="c")
        entry.config(width=30)
        return entry

    def showUserNotFound(self):
        messagebox.showinfo("Login", "Credenciais Incorretas")

    #try o login, send to server a msg with credentials
    def enterUser(self,event=None):
        self.username = self.txtUser.get()
        self.client.send('Login: '+self.txtUser.get()+'-'+self.txtPW.get())

    # try o register, send to server a msg with credentials
    def registerUser(self,event=None):
        self.client.send('Register: '+self.txtUser.get() + '-' + self.txtPW.get())

    def showMessgae(self,type,msg):
        messagebox.showinfo(type,msg)

    # go to chat window
    def goTochat(self):
        client=self.client
        self.root.withdraw()
        screen = ChatView(client)

    def inicializeBtnEnterUser(self):
        button1 = Button(self.root, text="Enter", fg="Black", command=self.enterUser, height=2, width=13, bg="Grey")
        button1.place(relx=.51, rely=0.75, anchor="c")
        return button1

    def inicializeBtnEnterRegister(self):
        button1 = Button(self.root, text="Register", fg="Black", command=self.registerUser, height=2, width=13, bg="Grey")
        button1.place(relx=.51, rely=0.90, anchor="c")
        return button1


