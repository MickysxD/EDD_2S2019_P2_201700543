from AVL.AVL import AVL
from AVL.AVL import NodoAVL
from ListaDoble.ListaDoble import ListaDoble
from ListaDoble.ListaDoble import Cuerpo
import csv
import os
import json
import hashlib
import datetime

av = AVL()
lista = ListaDoble()
json_data = json.dumps({})

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

                    jfinal = json.loads(bloque)
                i = i+1
    except FileNotFoundError:
        print("Error con el archivo")

def jleer(cadena):
    with open(cadena) as contenido:
        j = json.load(contenido)
        jactual = json.dumps(j)
        #jactual = jactual.replace(" ","")
        print(jactual)
        dir = json.dumps(j.get("INDEX")) + json.dumps(j.get("TIMESTAMP")).replace("\"","") + json.dumps(j.get("CLASS")).replace("\"","") + json.dumps(j.get("DATA")).replace(" ","") + json.dumps(j.get("PREVIOUSHASH")).replace("\"","")
        print(dir)
        print(hashlib.sha256(dir.encode()).hexdigest()+"\n")

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
    print(" 3. Reportes\n")
    seleccion = input()
    if(seleccion == "1"):
        insertarB()
    elif(seleccion == "2"):
        seleccionarB()
    elif(seleccion == "3"):
        reportes()
    else:
        print("Seleccion no valida")
    print("\n\n")

while(True):
    t = datetime.datetime.now()
    print(str(t.strftime("%d-%m-%y-::%H:%M:%S")))
    menu()
