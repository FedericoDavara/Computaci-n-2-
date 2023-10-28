import argparse
import os
import threading
import socket
import cv2

def procesar_imagen(archivo_entrada, archivo_salida):
    # Cargar la imagen y convertirla a escala de grises
    imagen = cv2.imread(archivo_entrada, cv2.IMREAD_COLOR)
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Guardar la imagen procesada
    cv2.imwrite(archivo_salida, imagen_gris)

def manejar_cliente(socket_cliente, archivo_imagen):
    # Procesar la imagen
    archivo_salida = 'gris_' + archivo_imagen
    procesar_imagen(archivo_imagen, archivo_salida)

    # Enviar la imagen procesada de vuelta al cliente
    with open(archivo_salida, 'rb') as f:
        socket_cliente.sendall(f.read())

    socket_cliente.close()

def servidor(ip, puerto, archivo_imagen):
    # Crear un socket que admite tanto IPv4 como IPv6
    socket_servidor = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    try:
        # Intentar vincular a IPv6
        socket_servidor.bind((ip, puerto))
    except socket.error:
        # Si falla, intentar vincular a IPv4
        socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_servidor.bind((ip, puerto))

    socket_servidor.listen(5)
    print(f"Escuchando en {ip}:{puerto}")

    while True:
        socket_cliente, direccion = socket_servidor.accept()
        print(f"Conexión aceptada desde {direccion[0]}:{direccion[1]}")
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(socket_cliente, archivo_imagen))
        hilo_cliente.start()

def main():
    parser = argparse.ArgumentParser(description='Tp2 - Procesa imágenes')
    parser.add_argument('-i', '--ip', required=True, help='Dirección de escucha')
    parser.add_argument('-p', '--puerto', type=int, required=True, help='Puerto de escucha')
    parser.add_argument('-f', '--archivo', required=True, help='Nombre del archivo de imagen a procesar')
    args = parser.parse_args()

    try:
        servidor(args.ip, args.puerto, args.archivo)
    except KeyboardInterrupt:
        print('Servidor detenido.')

if __name__ == '__main__':
    main()
