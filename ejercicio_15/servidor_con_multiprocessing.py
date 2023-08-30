#!/usr/bin/python3
import socket
import multiprocessing
import sys

def child_process(connection):
    print("Inicializando proceso hijo...\n")
    sock, addr = connection

    while True:
        mensaje = sock.recv(1024)
        if mensaje.decode() == '\r\n':
            continue
        else:
            datos = mensaje.decode()
            print("Se recibio: %s de %s" % (mensaje, addr))
            if datos == "exit\r\n":
                reply = "\nHasta pronto\r\n".encode("utf-8")
                sock.send(reply)
                print("El cliente %s ha cerrado la conexion\r\n" % str(addr))
                break
            else:
                reply_msg = datos.upper() + "\r\n"
                sock.send(reply_msg.encode("utf-8"))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host_address = ""
listening_port = 50001

server_socket.bind((host_address, listening_port))
server_socket.listen(5)

while True:
    client = server_socket.accept()

    client_socket, client_address = client

    print("Te has conectado a %s" % str(client_address))

    initial_msg = 'Bienvenido gracias por usar nuestro servidor' + "\r\n"
    client_socket.send(initial_msg.encode('ascii'))

    child_proc = multiprocessing.Process(target=child_process, args=(client,))
    child_proc.start()

    client_socket.close()