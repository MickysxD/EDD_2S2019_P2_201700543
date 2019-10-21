from AVL.AVL import AVL
from AVL.AVL import NodoAVL
from ListaDoble.ListaDoble import ListaDoble
from ListaDoble.ListaDoble import Bloque
import csv
import os
import json
import hashlib
import datetime
import socket
import select
import sys
from _thread import *

lista = ListaDoble()
jbloque = ""
respuesta = False
agregar = False

def graf(avl):
    nombre = "graficaAVL"
    doc = open(nombre + ".dot", "w")
    doc.write("digraph grafico{\nnode [shape = record];\ngraph [nodesep = 1];\nrankdir=TB;\n")

    doc.write(avl.grafica(avl.root))

    doc.write("}")
    doc.close()
    os.system("dot -Tjpg " + nombre + ".dot" + " -o " + nombre + ".jpg")
    os.system(nombre + ".jpg")

def carga(cadena):
    try:
        with open(cadena) as csvfile:  
            reader = csv.reader(csvfile, delimiter=',')
            i = 1
            nclase = ""
            for line in reader:
                if(i == 1):
                    nclase = line[1]
                if(i == 2):
                    datos = json.loads(line[1])
                    jactual = json.dumps(datos)
                    jactual = jactual.replace(" ","")
                    hora = datetime.datetime.now()
                    actual = str(hora.strftime("%d-%m-%y-::%H:%M:%S"))
                    prev = ""
                    hac = hashlib.sha256(jactual.encode()).hexdigest()
                    if(lista.contador == 0):
                        prev = "0000"
                    else:
                        prev = lista.ultimo.hash
                    bloque = {"INDEX":lista.contador,"TIMESTAMP":actual,"CLASS":nclase,"DATA":jactual,"PREVIOUSHASH":prev,"HASH":hac}
                    jfinal = json.dumps(bloque, separators=(',', ':'))
                    jbloque = json.dumps(jfinal)
                    server.sendall(jbloque.encode('utf-8'))
                    ciclo = True
                    while ciclo:
                        if(respuesta):
                            if(agregar):
                                index = 0
                                if(lista.contador != 0):
                                    nodo = Bloque(lista.contador, actual, nclase, jactual, prev, hac)
                                    lista.insertar_f(nodo)
                            respuesta = False
                            agregar = False
                            ciclo = False
                i = i+1
    except FileNotFoundError:
        print("Error con el archivo")

def jleer(cadena):
    with open(cadena) as contenido:
        j = json.load(contenido)
        jactual = json.dumps(j)
        #jactual = jactual.replace(" ","")
        dir = json.dumps(j.get("INDEX")) + json.dumps(j.get("TIMESTAMP")).replace("\"","") + json.dumps(j.get("CLASS")).replace("\"","") + json.dumps(j.get("DATA")).replace(" ","") + json.dumps(j.get("PREVIOUSHASH")).replace("\"","")

def insertarB():
    print("     Insertar Bloque\n")
    print(" Ingrese la direccion del archivo .csv")
    seleccion = input()
    print("\n")
    carga("e.csv")
    jleer("ENVIO_BLOQUE.json")

def seleccionarB():
    print("seleccionar")

def reportes():
    print("reportes")

def menu():
    print("     Menu\n")
    print(" 1. Insertar Bloque")
    print(" 2. Seleccionar Bloque")
    print(" 3. Reportes")
    print(" 4. Salir\n")
    seleccion = input()
    if(seleccion == "1"):
        insertarB()
    elif(seleccion == "2"):
        seleccionarB()
    elif(seleccion == "3"):
        reportes()
    elif(seleccion == "4"):
        exit()
    else:
        print("Seleccion no valida")
    print("\n\n")

def coneccion():
    while True:

        # maintains a list of possible input streams
        read_sockets = select.select([server], [], [], 1)[0]
        import msvcrt
        if msvcrt.kbhit(): read_sockets.append(sys.stdin)

        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)
                print (message.decode('utf-8'))
                if(message == "true"):
                    respuesta = True
                    agregar = True
                elif(message == "false"):
                    respuesta = True
                    agregar = False
            else:
                message = sys.stdin.readline()
                server.sendall(message.encode('utf-8'))
                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print ("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

while(True):
    start_new_thread(coneccion,())
    menu()

server.close()