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

    def factor(self, root):
        if(root == None):
            return -1
        else:
            return root.factor

    def rotacionDD(self, root):
        aux = root.izq
        root.izq = aux.der
        aux.der = root
        root.factor = max([root.izq.factor, root.der.factor]) + 1
        aux.factor = max([aux.izq.factor, aux.der.factor]) + 1
        return aux

    def rotacionII(self, root):
        aux = root.der
        root.der = aux.izq
        aux.izq = root
        root.factor = max([root.izq.factor, root.der.factor]) + 1
        aux.factor = max([aux.izq.factor, aux.der.factor]) + 1
        return aux
    
    def rotacionDI(self, root):
        root.izq = self.rotacionII(root.izq)
        temp = self.rotacionDD(root)
        return temp

    def rotacionID(self, root):
        root.der = self.rotacionDD(root.der)
        temp = self.rotacionII(root)
        return temp

    def agregarAVL(self, root, nuevo):
        padre = root
        if(nuevo.carnet < root.carnet):
            if(root.izq == None):
                root.izq = nuevo
            else:
                root.izq = self.agregarAVL(root.izq, nuevo)
                if(root.izq.factor - root.der.factor == 2):
                    if(nuevo.carnet < root.izq.carnet):
                       padre = self.rotacionDI(root)
                    else:
                        padre =  self.rotacionDD(root)
        
        elif(nuevo.carnet > root.carnet):
            if(root.der == None):
                root.der = nuevo
            else:
                root.der = self.agregarAVL(root.der, nuevo)
                if(root.der.factor - root.izq.factor == 2):
                    if(nuevo.carnet > root.der.carnet):
                       padre = self.rotacionID(root)
                    else:
                        padre =  self.rotacionII(root)
        else:
            print("Nodo duplicado")

        if(root.izq == None and root.der != None):
            root.factor = root.der.factor + 1
        elif(root.izq != None and root.der == None):
            root.factor = root.izq.factor + 1
        else:
            root.factor = max([root.izq.factor, root.der.factor]) + 1

        return padre

