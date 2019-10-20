from AVL.AVL import AVL
from AVL.AVL import NodoAVL
import csv
import os
import json
import hashlib

av = AVL()
jactual = json()

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
            for line in reader:
                if(i == 2):
                    jactual = json.load(line[1])
                    print(jactual)
                    i = i+1
                if(i < 3):
                    print(line[0])
                    print(line[1])
                    i = i+1
                else:
                    i = i+1
                print("\n")
    except FileNotFoundError:
        print("Error con el archivo")

def insertarB():
    print("     Insertar Bloque\n")
    print(" Ingrese la direccion del archivo .csv")
    seleccion = input()
    carga(seleccion)

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
    menu()
