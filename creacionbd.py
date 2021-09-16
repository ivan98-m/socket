import sqlite3 as sql
from sqlite3.dbapi2 import Cursor

def crear_db():
    conexion = sql.connect("usuarios.db")
    conexion.commit()
    conexion.close()

def crear_tabla():
    conexion = sql.connect("usuarios.db")
    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            apellido TEXT,
            edad INTEGER
        )"""
    )
    conexion.commit()
    conexion.close()

def insertar_fila(id, nombre, apellido, edad):
    conexion = sql.connect("usuarios.db")
    cursor = conexion.cursor()
    sql_instruccion = f"INSERT INTO usuarios VALUES ({id}, '{nombre}', '{apellido}', {edad})"
    cursor.execute(sql_instruccion)
    conexion.commit()
    conexion.close()

def insertar_filas(lista_personas):
    conexion = sql.connect("usuarios.db")
    cursor = conexion.cursor()
    sql_instruccion = f"INSERT INTO usuarios VALUES (?, ?, ?, ?)"
    cursor.executemany(sql_instruccion, lista_personas)
    conexion.commit()
    conexion.close()

def consultar_tabla():
    conexion = sql.connect("usuarios.db")
    cursor = conexion.cursor()
    sql_instruccion = f"SELECT * FROM usuarios"
    cursor.execute(sql_instruccion)
    #devolver todos los datos seleccionados en una lista, 
    datos = cursor.fetchall()
    conexion.commit()
    conexion.close()
    print(datos)

def buscar():
    conexion = sql.connect("usuarios.db")
    cursor = conexion.cursor()
    sql_instruccion = f"SELECT * FROM usuarios WHERE name like'jose'"
    cursor.execute(sql_instruccion)
    #devolver todos los datos seleccionados en una lista, 
    datos = cursor.fetchall()
    conexion.commit()
    conexion.close()
    print(datos)

if __name__ == "__main__":

    buscar()

    lista_personas = [
        (4, 'Andrea', 'Arrieta', 20),
        (5, 'Alejandra', 'Avila', 21)
    ]
    #insertar_filas(lista_personas)
    #consultar_tabla()
    #insertar_fila(3,"Raul", "Arias", 22)
