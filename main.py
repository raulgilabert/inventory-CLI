import sqlite3
import os
from tabulate import tabulate


print("Programa inventario versión 0.1")

# Conexión con base de datos
base = sqlite3.connect("datos.db")
cursor = base.cursor()

# Comprovación de la existencia de la tabla con los datos,
# Si no existe, se crea
cursor.execute("CREATE TABLE IF NOT EXISTS data (Nombre TEXT UNIQUE, " +
               "Cantidad INTEGER, Minimo INTEGER, Precio INTEGER)")

global SI
SI = ["S", "s", "Si", "Sí", "SI", "SÍ", "si", "sí", "sI", "sÍ"]


def anadir():
    print("AÑADIR \n")

    # Petición de los datos y posterior inserción en la base de datos
    nombre = input("Nombre del producto: ")
    cantidad = input("Cantidad del producto: ")
    minimo = input("Cantidad mínima del producto: ")
    precio = input("Precio del producto: ")

    cursor.execute("INSERT INTO data(Nombre, Cantidad, Minimo, Precio)" +
                   " VALUES(?, ?, ?, ?)", (nombre, cantidad, minimo, precio))


def eliminar():
    print("ELIMINAR \n")

    # Petición de los datos y posterior eliminación de la base de datos
    Nombre = input("Nombre del producto a eliminar de la lista: ")

    txt = input("¿Está seguro de querer eliminar " + Nombre +
                " de la lista? [S/n]")

    if txt in SI:
        cursor.execute("DELETE FROM data WHERE Nombre=?", (Nombre,))

    else:
        print()
        print("Operación cancelada")


def modificar():
    print("MODIFICAR \n")

    # Petición de los datos
    Nombre = input("Nombre del producto al que modificar los datos: ")
    CantidadMod = int(input("Cantidad de la modificación del producto: "))

    # Petición de los datos antiguos a la base de datos para su modificación

    cursor.execute("SELECT Cantidad FROM data WHERE Nombre=?", (Nombre,))
    data = cursor.fetchone()
    CantidadActual = data[0]
    Cantidad = CantidadActual + CantidadMod

    # Subida de los datos actualizados a la base de datos
    cursor.execute("UPDATE data SET Cantidad=? WHERE Nombre=?",
                   (Cantidad, Nombre))


def ver():
    # Selección de todos los datos de la base de datos
    cursor.execute("SELECT * FROM data ORDER BY Nombre")
    datosIniciales = cursor.fetchall()

    # Añadir a estos datos la cantidad faltante para llegar al mínimo
    # Y meterlo en una lista para la impresión
    titulos = ["Nombre", "Cantidad", "Mínimo", "Faltante", "Precio", "Coste"]

    datos = []

    for d in datosIniciales:
        faltante = int(d[2])-int(d[1])
        coste = faltante*int(d[3])

        if faltante < 0:
            datos.append([d[0], d[1], d[2], 0, d[3], 0])
        else:
            datos.append([d[0], d[1], d[2], faltante, d[3], coste])

    print(tabulate(datos, headers=titulos, tablefmt="github"))
    print()
    print()


# Inicio del bucle principal del programa
funcion = ""

while True:
    os.system("clear")

    print("""
    Seleccione la función a utilizar:
    - Añadir datos (1)
    - Eliminar datos (2)
    - Variar datos (3)
    - Ver datos (4)
    - Salir del programa (5)
    """)

    funcion = int(input())

    os.system("clear")

    # Comprovación de la función a ejecutar
    if funcion == 1:
        anadir()
        input("Presione [Enter] para continuar")

    elif funcion == 2:
        eliminar()
        input("Presione [Enter] para continuar")

    elif funcion == 3:
        modificar()
        input("Presione [Enter] para continuar")

    elif funcion == 4:
        ver()
        input("Presione [Enter] para continuar")

    elif funcion == 5:
        # Asegurar que el usuario quiere salir del programa
        txt = input("¿Está seguro de que desea salir? [S/n]: ")

        if txt in SI:
            os.system("clear")
            break
        else:
            print()
            input("Volviendo, pulse [Enter] para continuar")

    else:
        input("Texto no válido, pulse [Enter] para continuar")

    base.commit()
