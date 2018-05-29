from view.chatView import*
from tkinter import messagebox
from tkinter import *

class NewRoom:

    def __init__(self,client):
        self.root=self.inicializeRoot()
        self.small_font = ('Verdana', 10)
        self.big_font = ('Verdana', 10)
        self.inicializeLabels()
        self.inicializeButtons()
        self.incializeText()
        self.client=client
        self.root.mainloop()

    def inicializeRoot(self):
        root = Tk()
        root.title('Chat Service')
        root.resizable(False, False)
        root.configure(background='lightgrey')
        root.geometry("230x130")
        return root

    def inicializeLabels(self):
        label = Label(self.root, text="Please insert new chat name:", font=self.small_font, bg="lightgrey")
        label.place(relx=.5, rely=.25, anchor="c")

    #send message to server with the name of new room
    def enter(self,event=None):
        roomName=self.txtName.get("1.0",END)
        if not roomName :
            wind=messagebox.showerror("Erro", "Tem que indicar um nome")
        else:
            self.client.send("#enter %s"%roomName )
            self.root.destroy()

    def incializeText(self):
        self.txtName = Text(self.root, height=1.5, width=15, font=self.big_font)
        self.txtName.place(relx=.38, rely=.7, anchor="c")

    def inicializeButtons(self):
        button1 = Button(self.root, text = "ENTER", fg = "Black", command=self.enter, height=1, width=5, bg="grey")
        button1.bind('<Return>',self.enter)
        button1.place(relx=.8,rely=.7, anchor="c")
        self.root.bind('<Return>',self.enter)


