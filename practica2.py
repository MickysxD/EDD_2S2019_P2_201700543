from AVL.AVL import AVL
from AVL.AVL import NodoAVL
import csv
import os
import json
import hashlib

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
                if(i < 3):
                    print(line[0])
                    print(line[1])
                    i = i+1
                else:
                    i = i+1
                print("\n")
    except FileNotFoundError:
        print("")

carga("Estructuras de datos.csv")

av = AVL()
