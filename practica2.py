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
arbol = AVL()
bseleccion = None
jbloque = ""
respuesta = False
agregar = False

def reporteAVL():
    global arbol
    nombre = "graficaAVL"
    doc = open(nombre + ".dot", "w")
    doc.write("digraph grafico{\nnode [shape = record];\ngraph [nodesep = 1];\nrankdir=TB;\n")

    doc.write(arbol.grafica(arbol.root))

    doc.write("}")
    doc.close()
    os.system("dot -Tjpg " + nombre + ".dot" + " -o " + nombre + ".jpg")
    os.system(nombre + ".jpg")

def reporteB():
    nombre = "graficaBloques"
    doc = open(nombre + ".dot", "w")
    doc.write("digraph grafico{\nnode [shape = record];\ngraph [nodesep = 1];\nrankdir=TB;\n")

    temp = lista.primero
    while(temp != None):
        if(temp == lista.primero):
            doc.write(str(temp.index)+"[label=\"CLASS: " + str(temp.clas) + "\\nTIMESTAMP: " + str(temp.time) + "\\nPHASH: "+temp.prev+"\\nHASH: "+temp.hash+"\"];\n")
            if(temp.siguiente != None):
                doc.write(str(temp.index) + "->" + str(temp.siguiente.index) + ";\n")
            temp = temp.siguiente
        if(temp == lista.ultimo):
            doc.write(str(temp.index)+"[label=\"CLASS: " + str(temp.clas) + "\\nTIMESTAMP: " + str(temp.time) + "\\nPHASH: "+temp.prev+"\\nHASH: "+temp.hash+"\"];\n")
            doc.write(str(temp.index) + "->" + str(temp.anterior.index) + ";\n")
            break
        elif (temp != None):
            doc.write(str(temp.index)+"[label=\"CLASS: " + str(temp.clas) + "\\nTIMESTAMP: " + str(temp.time) + "\\nPHASH: "+temp.prev+"\\nHASH: "+temp.hash+"\"];\n")
            doc.write(str(temp.index) + "->" + str(temp.siguiente.index) + ";\n")
            doc.write(str(temp.index) + "->" + str(temp.anterior.index) + ";\n")
            temp = temp.siguiente
        
    doc.write("}")
    doc.close()
    os.system("dot -Tjpg " + nombre + ".dot" + " -o " + nombre + ".jpg")
    os.system(nombre + ".jpg")

def arbolR(cadena):
    global arbol
    datos = json.loads(cadena)
    dos = json.dumps(datos.get("value"))
    dos = dos.replace("\"","")
    lis = dos.split("-")
    nuevo = NodoAVL()
    nuevo.carnet = lis[0]
    nuevo.nombre = lis[1]
    arbol.agregar(nuevo)
    lef = json.dumps(datos.get("left"))
    rig = json.dumps(datos.get("right"))
    if(lef != "null"):
        arbolR(lef)
    if(rig != "null"):
        arbolR(rig)

def marbol():
    stay = True
    while(stay):
        print("\n\n     Reportes de arbol\n")
        print("1. Arbol")
        print("2. Inorder")
        print("3. Preorder")
        print("4. Posorder")
        print("5. Salir")
        seleccion = input()
        if(seleccion == "1"):
            reporteAVL()
        elif(seleccion == "2"):
            arbol.inorder(arbol.root)
        elif(seleccion == "3"):
            arbol.preorder(arbol.root)
        elif(seleccion == "4"):
            arbol.posorder(arbol.root)
        elif(seleccion == "5"):
            stay = False
        else:
            print("ERROR: seleccion no valida")

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
                    hora = datetime.datetime.now()
                    actual = str(hora.strftime("%d-%m-%y-::%H:%M:%S"))
                    prev = ""
                    if(lista.contador == 0):
                        prev = "0000"
                    else:
                        prev = lista.ultimo.hash
                    para = str(lista.contador)+actual+nclase+jactual.replace(" ","")+prev
                    hac = hashlib.sha256(para.encode()).hexdigest()
                    bloque = {
                        "INDEX":lista.contador,
                        "TIMESTAMP":actual,
                        "CLASS":nclase,
                        "DATA":jactual,
                        "PREVIOUSHASH":prev,
                        "HASH":hac
                        }
                    jfinal = json.dumps(bloque, separators=(',', ':'))
                    #print(jfinal+"\n")
                    server.sendall(jfinal.encode('utf-8'))
                    ciclo = True
                    global respuesta
                    global agregar
                    while ciclo:
                        if(respuesta):
                            if(agregar):
                                nodo = Bloque(lista.contador, actual, nclase, jactual, prev, hac)
                                lista.insertar_f(nodo)
                                print("Bloque agregado \n")
                            respuesta = False
                            agregar = False
                            ciclo = False
                i = i+1
    except FileNotFoundError:
        print("Error con el archivo")

def jleer(cadena):
    try:
        #print(cadena+"\n")
        jfinal = json.loads(cadena)
        datos = json.loads(json.dumps(jfinal.get("DATA")))
        jactual = json.dumps(datos)
        #print(jactual+"\n")
        jactual = jactual.replace(" ","").replace("\"","").replace("\\","\"")
        #print(jactual+"\n")
        para = json.dumps(jfinal.get("INDEX")) + json.dumps(jfinal.get("TIMESTAMP")).replace("\"","") + json.dumps(jfinal.get("CLASS")).replace("\"","") + jactual + json.dumps(jfinal.get("PREVIOUSHASH")).replace("\"","")
        actual = hashlib.sha256(para.encode()).hexdigest()
        enviado = json.dumps(jfinal.get("HASH")).replace("\"","")
        #print(para+"\n")
        #print(actual+"\n")
        #print(enviado+"\n")
        if(actual == enviado):
            msm = "true"
            server.sendall(msm.encode('utf-8'))
        else:
            msm = "false"
            server.sendall(msm.encode('utf-8'))
        ciclo = True
        global respuesta
        global agregar
        while ciclo:
            if(respuesta):
                if(agregar):
                    nodo = Bloque(json.dumps(jfinal.get("INDEX")), json.dumps(jfinal.get("TIMESTAMP")), json.dumps(jfinal.get("CLASS")).replace("\"",""), jactual, json.dumps(jfinal.get("PREVIOUSHASH")).replace("\"",""), actual)
                    lista.insertar_f(nodo)
                    jleer(jbloque)
                    print("Bloque agregado \n")
                respuesta = False
                agregar = False
                ciclo = False
    except ValueError:
        print("ERROR: Cadena no valida")

def insertarB():
    print("\n\n     Insertar Bloque\n")
    print(" Ingrese la direccion del archivo .csv")
    seleccion = input()
    carga(seleccion)
    
def seleccionarB():
    aux = lista.primero
    global bseleccion
    stay = True
    while(stay):
        if(aux != None):
            print("\n\n\n       Seleccionar Bloque\n")
            print("     INDEX: "+str(aux.index))
            print("     TIMESTAMP: "+aux.time)
            print("     CLASS: "+aux.clas)
            print("     DATA: "+aux.data)
            print("     PREVIOUSHASH: "+aux.prev)
            print("     HASH: "+aux.hash)
            print("\n1. Siguiente")
            print("2. Anterior")
            print("3. Seleccionar")
            print("4. Salir\n")

            seleccion = input()
            
            if(seleccion == "1" and aux.siguiente != None):
                aux = aux.siguiente
            elif(seleccion == "2" and aux.anterior != None):
                aux = aux.anterior
            elif(seleccion == "3"):
                print(" Seleccionado\n")
                bseleccion = aux
                stay = False
            elif(seleccion == "4"):
                stay = False
        else:
            stay = False

def reportes():
    stay = True
    while(stay):
        print("\n\n     Reportes\n")
        print("1. Reporte de bloques")
        print("2. Reporte de Arbol")
        print("3. Salir")
        seleccion = input()
        if(seleccion == "1"):
            if(lista.contador != 0):
                reporteB()
            else:
                print("ERROR: No hay bloques a graficars")
        elif(seleccion == "2"):
            if(bseleccion != None):
                global arbol
                arbol = AVL()
                arbolR(bseleccion.data)
                marbol()
            else:
                print("ERROR: No hay bloque escogido")
        elif(seleccion == "3"):
            stay = False

def menu():
    print("\n\n     Menu\n")
    print(" 1. Insertar Bloque")
    print(" 2. Seleccionar Bloque")
    print(" 3. Reportes")
    print(" 4. Salir\n")
    seleccion = input()
    if(seleccion == "1"):
        insertarB()
    elif(seleccion == "2"):
        if(lista.contador != 0):
            seleccionarB()
        else:
            print(" No hay bloque a escoger")
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
                msm = message.decode('utf-8')
                #print (msm)
                global respuesta
                global agregar
                if(msm == "true"):
                    respuesta = True
                    agregar = True
                elif(msm == "false"):
                    respuesta = True
                    agregar = False
                elif(respuesta == False):
                    cadena  = msm
                    jleer(cadena)
                sys.stdout.flush()
            else:
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