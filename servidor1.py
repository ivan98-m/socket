from tkinter import *
from tkinter import ttk, messagebox
from socket import *
import _thread
import sqlite3 as sql
from sqlite3.dbapi2 import Cursor

class AplicacionServer():

    def __init__(self):

        self.raiz = Tk()
        self.raiz.resizable(0, 0)
        self.raiz.title("Server")
        self.conn=""

        btn_conectar = ttk.Button(self.raiz, text='Star Server', command=self.star_server)
        btn_conectar.grid(row = 0, column = 0, sticky = W, padx=25, pady=25)

        l2=ttk.Label(self.raiz,text='Chat')
        l2.grid(row = 1, column = 0, sticky = W, padx=25, pady=0)

        fr = Frame(self.raiz)
        fr.grid(row=2, column=0, padx=25)
        self.text_box = Text(fr, height = 8, width = 40)
        self.text_box.pack(side=LEFT, fill='both')
        self.text_box.config(bg='#D9D8D7', state=DISABLED)

        sbr = Scrollbar(fr)
        sbr.pack(side=RIGHT, fill="y")
        sbr.config(command=self.text_box.yview)
        self.text_box.config(yscrollcommand=sbr.set)

        self.txt_mensaje = ttk.Entry(self.raiz, width=43)
        self.txt_mensaje.grid(row=3,column=0,padx=25, pady=20, sticky=W)
        self.txt_mensaje.bind("<KeyRelease-Return>", self.press)

        btn_enviar = ttk.Button(self.raiz, text='Send', command=self.enviar)
        btn_enviar.grid(row=3, column=0, padx=25, sticky=E) 

        btn_buscar = ttk.Button(self.raiz, text="Search", command=self.buscar)
        btn_buscar.grid(row=2, column=1, padx=15, sticky=N)

        _thread.start_new_thread(self.receive, ())

        self.raiz.mainloop()
    
    def star_server(self):

        s = socket(AF_INET, SOCK_STREAM)
        host = 'localhost'  ## to use between devices in the same network eg.192.168.1.5
        port = 9898
        s.bind((host, port))
        s.listen(1)
        conn, addr = s.accept()
        self.conn=conn

    def chat(self, msg, state):
        
        self.text_box.config(state=NORMAL)
        if state==0:
            self.text_box.tag_configure('config-1', justify=RIGHT)
            self.text_box.insert(END, msg, 'config-1')
        else:
            self.text_box.tag_configure('config-2', justify=LEFT,foreground="green")
            self.text_box.insert(END, msg, 'config-2')
        self.text_box.config(state=DISABLED)
    
        self.text_box.yview(END)

    def enviar(self):
        #msg = self.txt_mensaje.get().strip()
        msg = ""
        msg = ("\nServidor: " + self.txt_mensaje.get().strip())
        try:
            # actiualizar chat
            self.chat(msg, 0)
            # enviar mensaje
            self.conn.send(msg.encode('utf_8'))
            self.txt_mensaje.delete(0, END)
        except:
            print("ERROR AL ENVIAR EL MENSAJE DESDE EL SERVIDOR")

    def receive(self):
        while 1:
            try:
                data = self.conn.recv(1024)
                msg = data.decode('utf_8')
                if msg != "":
                    self.chat(msg, 1)
            except:
                pass
            
    def press(self, event):
        self.enviar()

    def buscar(self ):
        conexion = sql.connect("usuarios.db")
        cursor = conexion.cursor()
        msg = ""
        msg = (self.txt_mensaje.get().strip())
        sql_instruccion = f"SELECT * FROM usuarios WHERE name like'{msg}'"
        cursor.execute(sql_instruccion)
        #devolver todos los datos seleccionados en una lista, dentro de una tupla
        datos = cursor.fetchall()
        if datos:
            self.autocompletar_nombre(datos)
            print(datos)
        else:
            messagebox.showwarning("Warning","No exite ese nombre en la BD")

        conexion.commit()
        conexion.close()

    def autocompletar_nombre(self, datos):
        self.txt_mensaje.delete(0, END)
        tupla=""
        for i in datos:
            tupla = i
        
        nombre = tupla[1]
        apellido = tupla[2]

        nombre_completo = nombre+" "+apellido
        self.txt_mensaje.insert(END, nombre_completo)


def main():
    mi_app = AplicacionServer()
    return(0)


if __name__ == '__main__':
    main()
