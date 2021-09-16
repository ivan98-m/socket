from tkinter import *
from tkinter import ttk
from socket import *
import _thread
#import tkinter.scrolledtext as st

class AplicacionCliente():

    def __init__(self):
        self.raiz = Tk()
        self.raiz.geometry('495x285+500+50')
        self.raiz.resizable(0, 0)
        self.raiz.title("Cliente")
        self.conexion=""

        btn_conectar = ttk.Button(self.raiz, text='Connet', command=self.conectar)
        btn_conectar.place(x=25, y=25)

        l2=ttk.Label(self.raiz,text='Chat')
        l2.place(x=25, y=70)

        fr = Frame(self.raiz)
        fr.place(x=25, y=90)
        self.text_box = Text(fr, height = 8, width = 40)
        self.text_box.pack(side=LEFT, fill='both', expand=True)
        self.text_box.config(bg='#D9D8D7',state=DISABLED)

        sbr= Scrollbar(fr)
        sbr.pack(side=RIGHT, fill="y")
        sbr.config(command=self.text_box.yview)
        self.text_box.config(yscrollcommand=sbr.set)

        self.txt_mensaje = ttk.Entry(self.raiz)
        self.txt_mensaje.place(x=25,y=240, width=260, height=25)
        self.txt_mensaje.bind("<KeyRelease-Return>", self.press)

        btn_enviar = ttk.Button(self.raiz, text='Send', command=self.enviar)
        btn_enviar.place(x=286, y=238, width=80, height=28)

        btn_buscar = ttk.Button(self.raiz, text="Search")
        btn_buscar.place(x=400, y=90)

        _thread.start_new_thread(self.receive, ())

        self.raiz.mainloop()

    def conectar(self):
        # initializa socket
        s = socket(AF_INET, SOCK_STREAM)
        host = 'localhost'  ## to use between devices in the same network eg.192.168.1.5
        port = 9898
        # conectar con el server
        s.connect((host, port))
        self.conexion=s

    def chat(self, msg, state):

        self.text_box.config(state=NORMAL)
        if state==0:
            self.text_box.tag_configure('config-1', justify=RIGHT)
            self.text_box.insert(END, msg,'config-1')
        else:
            self.text_box.tag_configure('config-2', justify=LEFT,foreground="red")
            self.text_box.insert(END, msg, 'config-2')
        self.text_box.config(state=DISABLED)
        # show the latest messages
        self.text_box.yview(END)

    def enviar(self):
        #msg = self.txt_mensaje.get().strip()
        msg = ""
        msg = ("\nCliente: " + self.txt_mensaje.get().strip())
        try:
            self.chat(msg, 0)
            self.conexion.send(msg.encode('utf_8'))
            self.txt_mensaje.delete(0, END)
        except:
            print("ERROR AL ENVIAR EL MENSAJE DESDE EL SERVIDOR")

    def receive(self):
        while 1:
            try:
                data = self.conexion.recv(1024)
                msg = data.decode('utf_8')
                if msg != "":
                    self.chat(msg, 1)
            except:
                pass
    
    def press(self, event):
        self.enviar()

def main():
    mi_app = AplicacionCliente()
    return(0)

if __name__ == '__main__':
    main()


