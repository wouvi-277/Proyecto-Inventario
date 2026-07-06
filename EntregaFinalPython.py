import sqlite3
from colorama import Fore, init
init()
conexion = sqlite3.connect('inventario.db')
cursor = conexion.cursor()
#crear tabal del inventario
cursor.execute('''
               CREATE TABLE IF NOT EXISTS inventario(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nombre TEXT NOT NULL,
               descripcion TEXT,
               cantidad  INTEGER NOT NULL,
               precio REAL NOT NULL,
               categoria TEXT
               ) 
''')
conexion.commit()
conexion.close()
#registrar nuevos productos
def registrar_producto():
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    try:
        print(Fore.CYAN,'REGISTRO DEL INVENTARIO')
        nom = input('Ingrese el nombre del producto a agregar: ').strip().capitalize()
        descrip = input('Ingrese una breve descripcion del producto: ')
        canti = int(input('Ingrese la cantidad del producto agregado: '))
        valor = float(input('Ingrese el precio del producto a agregar: '))
        catego = input('Ingrese la categoria a la que pertenece el producto a agregar: ')

        if nom == '':
            print(Fore.RED,'[ERROR] El nombre no puede estar vacio')
            return
        if canti < 0:
            print(Fore.RED,'La cantidad de productos no puede ser menor a cero')
            return
        if valor <= 0:
            print(Fore.RED,'El precio de los productos debe ser mayor a cero.')
            return
        
    except ValueError:
        print(Fore.RED,'[ERROR] El tipo de dato es invalido.')
    try:
        conexion.execute('BEGIN TRANSACTION')
        cursor.execute('INSERT INTO inventario (nombre, descripcion, cantidad, precio, categoria) VALUES (?,?,?,?,?)',(nom,descrip,canti,valor,catego))
        conexion.commit()
        print(Fore.GREEN,'Productos agregados al inventario exitosamente.')
    except sqlite3.Error as e:
        #si salta error se deshace la accion
        conexion.rollback()
        print(f'Error al registrar el producto {e}')
    finally:
        conexion.close()

#visualizar los productos registrados
def ver_productos():
    print(Fore.YELLOW,'INVENTARIO')
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM inventario')
    inventario = cursor.fetchall()
    for producto in inventario:
        print(f'ID: {producto[0]}, Nombre: {producto[1]}, Descripcion: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoria: {producto[5]}')

#actualizar datos desde su id
def actualizar_produ():
    print('Modificacion de producto')
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    while True:
        try:
            while True:
                id_update = input('Ingrese el ID del producto: ')
                cursor.execute('SELECT * FROM inventario WHERE id = ?',(id_update,))
                existente = cursor.fetchone()
                if not existente:
                    print('No se encontro un producto con ese ID.')
                    continue
                else:
                    break
           
            nuevo_precio = float(input('Ingrese el precio altualizado del producto: '))
            if nuevo_precio <= 0:
                print(Fore.RED,'El precio de los productos debe ser mayor a cero.')
            break
        except ValueError:
            print('Ingresa un numero valido.')
    
        try:
            cursor.execute('UPDATE inventario SET precio = ? WHERE id = ?',(nuevo_precio,id_update))
            conexion.commit()
            print(Fore.GREEN,'Precio actualizado con exito.')
        except sqlite3.Error as e:
            conexion.rollback()
            print(Fore.RED,'[Error] El producto no fue actualizado.')
        except TypeError:
            print(Fore.RED,'ID no encontrado.') 
        finally:
            conexion.close()

#eliminar productos desde si id
def eliminar_producto():
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    try:
        conexion.execute('BEGIN TRANSACTION')
        id_delete = input('Ingrese el ID a eliminar: ')
        cursor.execute('DELETE FROM inventario WHERE id = ?',(id_delete,))
        borrado = cursor.fetchone()
        if not borrado:
            print(Fore.YELLOW,'[INFO] No se encontro el ID.')
        else:
            conexion.commit()
            print(Fore.GREEN,'Producto eliminado con exito.')
    except sqlite3.Error as e:
        #si salta error se deshace la accion
        conexion.rollback()
        print(f'Error al ELIMINAR el producto {e}')
    except TypeError:
        print(Fore.RED,'ID no encontrado.')
    finally:
        conexion.close()

#buscar productos mediante su id, opcional,con nombre o categoria
def buscar_produ():
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    try:
        id_buscar = input('Ingrese el ID a buscar: ')
        cursor.execute('SELECT * FROM inventario WHERE id = ?',(id_buscar,))
        producto_bus = cursor.fetchone()
        print(f'ID: {producto_bus[0]}, Nombre: {producto_bus[1]}, Descripcion: {producto_bus[2]}, Cantidad: {producto_bus[3]}, Precio: {producto_bus[4]}, Categoria: {producto_bus[5]}')
    except sqlite3.Error as e:
        #si salta error se deshace la accion
        print(f'Error. No se encontro el producto buscado {e}')
    except TypeError:
        print(Fore.RED,'ID no encontrado.')
    finally:
        conexion.close()
    
#reporte de productos con misma cantidad o algun limite estableido por el usuario
def reporte_espe():
    conexion = sqlite3.connect('inventario.db')
    cursor = conexion.cursor()
    try:
        while True:
            limite = int(input('Ingrese el limite de cantidad de producto: '))
            if limite >= 0:
                break
            else:
                print('Ingrese valor positivo')
        cursor.execute('SELECT * FROM inventario WHERE cantidad <= ?',(limite,))
        limite_cantidad = cursor.fetchall()
        for i in limite_cantidad:
            print(f'ID: {i[0]}, Nombre: {i[1]}, Descripcion: {i[2]}, Cantidad: {i[3]}, Precio: {i[4]}, Caategoria: {i[5]}')
    except sqlite3.Error as e:
        #si salta error se deshace la accion
        print(f'Error. No se encontro el producto reportado {e}')
    finally:
        conexion.close()  

print('MENU DE OPCIONES')
print('Ingrese 1 para registrar un nuevo producto.')
print('Ingrese 2 para visualizar el inventario.')
print('Ingrese 3 para actualizar los datos de un producto.')
print('Ingrese 4 para eliminar un producto.')
print('Ingrese 5 para buscar mediante su id.')
print('Ingrese 6 para buscar por cantidad de productos.')
print('Ingrese 7 para finalizar.')
while True:
    opcion= int(input('ingrese una opcion para continuar: '))
    if opcion == 1:
        registrar_producto()
    if opcion == 2:
        ver_productos()
    if opcion == 3:
        actualizar_produ()
    if opcion == 4:
        eliminar_producto()
    if opcion == 5:
        buscar_produ()
    if opcion == 6:
        reporte_espe()
    if opcion == 7:
        break





