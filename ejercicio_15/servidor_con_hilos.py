#!/usr/bin/python3
import socket
import threading

def hilos_de_trabajo(connection):
    print("Inicializando hilos de trabajo...")

    while True:
        datos = connection.recv(1024)
        if datos.decode() == '\r\n':
            continue
        else:
            mensaje = datos.decode()
            print("Se ha recibido el mensaje: %s" % mensaje)
            if mensaje == "exit\r\n":
                respuesta = "\nHasta pronto!\r\n".encode("utf-8")
                connection.send(respuesta)
                print("El cliente termino la conexion.\r\n")
                connection.close()
                break
            else:
                mensaje_de_respuesta = mensaje.upper() + "\r\n"
                connection.send(mensaje_de_respuesta.encode("utf-8"))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host_address = ""
listening_port = 50001

server_socket.bind((host_address, listening_port))
server_socket.listen(5)

while True:
    client_socket, client_address = server_socket.accept()

    print("Te has conectado a %s" % str(client_address))

    mensaje_de_bienvenida = 'Gracias por utilizar nuesto servidor' + "\r\n"
    client_socket.send(mensaje_de_bienvenida.encode('ascii'))

    worker = threading.Thread(target=hilos_de_trabajo, args=(client_socket,))
    worker.start()