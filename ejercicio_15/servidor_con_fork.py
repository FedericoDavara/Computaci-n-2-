#!/usr/bin/python3
import socket
import os
import sys
import signal

signal.signal(signal.SIGCHLD, signal.SIG_IGN)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host_address = ""
listening_port = 50002

server_socket.bind((host_address, listening_port))
server_socket.listen(5)

while True:
    client_socket, client_address = server_socket.accept()

    print("Conexion desde %s" % str(client_address))

    mensaje_de_bienvenida = "Bienvenido gracias por su conexion" + "\r\n"
    client_socket.send(mensaje_de_bienvenida.encode('ascii'))
    
    try:
        child_pid = os.fork()
        if not child_pid:
            while True:
                msg = client_socket.recv(1024)
                if not msg.decode():
                    break
                else:
                    data = msg.decode()
                    print("Received: %s" % data)
                    if data == "exit\r\n":
                        response = "\nHasta pronto\r\n".encode("utf-8")
                        client_socket.send(response)
                        client_socket.close()
                        print("El cliente %s ha finalizado la conexion\r\n" % str(client_address))
                        sys.exit(0)
                    else:
                        response_msg = data.upper() + "\r\n"
                        client_socket.send(response_msg.encode("utf-8"))
    except BrokenPipeError:
        print("El cliente termino la conexion")

    client_socket.close()