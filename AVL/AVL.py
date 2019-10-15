class NodoAVL():
    
    def __init__(self):
        self.izq = None
        self.der = None
        self.nombre = ""
        self.carnet = 0
        self.altura = 0 
        self.factor = 0

class AVL():

    def __init__(self):
        self.root = None

    def agregar(self, nuevo):
        if(self.root == None):
            self.root = nuevo
        else:
            self.agregarRecursivo(self.root, nuevo)

    def agregarRecursivo(self, root, nuevo):
        if(root.carnet > nuevo.carnet):
            if(root.izq != None):
                self.agregarRecursivo(root.izq, nuevo)
            else:
                root.izq = nuevo
        elif(root.carnet < nuevo.carnet):
            if(root.der != None):
                self.agregarRecursivo(root.der, nuevo)
            else:
                root.der = nuevo
        elif(root.carnet == nuevo.carnet):
            nuevo.izq = root.izq
            nuevo.der = root.der
            root = nuevo
        else:
            print("Error al agregar: " + str(nuevo.carnet))
    
    def grafica(self, root):
        retorno = ""
        rank = ""

        if(root.izq != None or root.der != None):
            retorno = "\"" + str(root.carnet) + "\"[label= \"<C0>| Carne: " + str(root.carnet) + "\\nNombre: " + root.nombre + "\\nAltura: " + str(root.altura) + "\\nFactor: " + str(root.factor) + "|<C1>\"];\n"
            rank = "{rank=same; "
        else:
            retorno = "\"" + str(root.carnet) + "\"[label= \"Carne: " + str(root.carnet) + "\\nNombre: " + root.nombre + "\\nAltura: " + str(root.altura) + "\\nFactor: " + str(root.factor) + "\"];\n"
            
        if(root.izq != None):
            retorno = retorno + self.grafica(root.izq)
            retorno = retorno + "\"" + str(root.carnet) + "\":C0->\"" + str(root.izq.carnet) + "\";\n"
            rank = rank + "\"" + str(root.izq.carnet) + "\" "
	
        if (root.der != None):
            retorno = retorno + self.grafica(root.der)
            retorno = retorno +  "\"" + str(root.carnet) + "\":C1->\"" + str(root.der.carnet) + "\";\n"
            rank = rank + "\"" + str(root.der.carnet) + "\" "
	
        if (root.izq != None or root.der != None):
            rank = rank + "}\n"

        retorno = retorno + rank
        return retorno
