from view.chatView import*
from tkinter import messagebox

class AddTime:

    def __init__(self,room,user,view):
        self.root=self.inicializeRoot()
        self.small_font = ('Verdana', 10)
        self.big_font = ('Verdana', 10)
        self.inicializeLabels()
        self.inicializeButtons()
        self.incializeText()
        self.user=user
        self.room=room
        self.view=view
        self.root.mainloop()

    def inicializeRoot(self):
        root = Tk()
        root.title('Chat Service')
        root.resizable(False, False)
        root.configure(background='lightgrey')
        root.geometry("230x130")
        return root

    def inicializeLabels(self):
        label = Label(self.root, text="Please insert time (minutes):", font=self.small_font, bg="lightgrey")
        label.place(relx=.5, rely=.25, anchor="c")

    #call method timeout of chatview
    def enter(self,event=None):
        try:
            data=self.txtTime.get("1.0",END)
            data=data.replace('\n','')
            number=int(data)
            self.view.timeout(self.room,self.user, number)
            self.root.destroy()
        except ValueError:
            wind = messagebox.showerror("Erro", "Tem que indicar um numero")

    def incializeText(self):
        self.txtTime = Text(self.root, height=1.5, width=15, font=self.big_font)
        self.txtTime.place(relx=.38, rely=.7, anchor="c")

    def inicializeButtons(self):
        button1 = Button(self.root, text = "ENTER", fg = "Black", command=self.enter, height=1, width=5, bg="grey")
        button1.bind('<Return>',self.enter)
        button1.place(relx=.8,rely=.7, anchor="c")
        self.root.bind('<Return>',self.enter)

