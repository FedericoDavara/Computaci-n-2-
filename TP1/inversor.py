import argparse
import os
import multiprocessing


def linea_de_proceso(linea,comandos):
    invertir_linea = linea[::-1]
    comandos.send(invertir_linea)
    comandos.close()


def main():
    parser = argparse.ArgumentParser(description='Invierte el orden de cada línea de un archivo de texto')
    parser.add_argument('-f', '--file', type=str, required=True)
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        lineas = f.readlines()

    procesos = []
    for linea in lineas:
        comando_pariente, comando_niños = multiprocessing.Pipe()
        proceso = multiprocessing.Process(target=linea_de_proceso, args=(linea.strip(), comando_niños))
        procesos.append((proceso, comando_pariente))
        proceso.start()

    lineas_invertidas = []
    for proceso, comando_pariente in procesos:
        proceso.join()
        lineas_invertidas.append(comando_pariente.recv())

    for linea in lineas_invertidas:
        print(linea)


if __name__ == '__main__':
    main()