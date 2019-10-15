from AVL.AVL import AVL
from AVL.AVL import NodoAVL
import csv
import os

def graf(avl):
    nombre = "graficaAVL"
    doc = open(nombre + ".dot", "w")
    doc.write("digraph grafico{\nnode [shape = record];\ngraph [nodesep = 1];\nrankdir=TB;\n")

    doc.write(avl.grafica(avl.root))

    doc.write("}")
    doc.close()
    os.system("dot -Tjpg " + nombre + ".dot" + " -o " + nombre + ".jpg")
    os.system(nombre + ".jpg")


av = AVL()

nodo = NodoAVL()
nodo.nombre = "Micky"
nodo.carnet = 2019
av.agregar(nodo)

nodo = NodoAVL()
nodo.nombre = "Ju"
nodo.carnet = 2017
av.agregar(nodo)

nodo = NodoAVL()
nodo.nombre = "E"
nodo.carnet = 2018
av.agregar(nodo)

nodo = NodoAVL()
nodo.nombre = "Ji"
nodo.carnet = 2015
av.agregar(nodo)

nodo = NodoAVL()
nodo.nombre = "Miguel"
nodo.carnet = 2020
av.agregar(nodo)

graf(av)