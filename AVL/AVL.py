class NodoAVL():
    
    def __init__(self):
        self.izq = None
        self.der = None
        self.nombre = ""
        self.carnet = 0
        self.altura = 1 
        self.factor = 0

class AVL():

    def __init__(self):
        self.root = None

    def agregar(self, nuevo):
        if(self.root == None):
            nuevo.altura = 1
            self.root = nuevo
        else:
            self.agregarAVL(self.root, nuevo)

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

    def altura(self, root):
        if(root == None):
            return 0
        else:
            return root.altura

    def rotacionI(self, root):
        aux = root.izq
        root.izq = aux.der
        aux.der = root
        root.factor = max([self.factor(root.izq), self.factor(root.der)]) + 1
        root.altura = max([self.altura(root.izq), self.altura(root.der)]) + 1
        aux.factor = max([self.factor(aux.izq), self.factor(aux.der)]) + 1
        aux.altura = max([self.altura(aux.izq), self.altura(aux.der)]) + 1
        return aux

    def rotacionD(self, root):
        aux = root.der
        root.der = aux.izq
        aux.izq = root
        root.factor = max([self.factor(root.izq), self.factor(root.der)]) + 1
        root.altura = max([self.altura(root.izq), self.altura(root.der)]) + 1
        aux.factor = max([self.factor(aux.izq), self.factor(aux.der)]) + 1
        aux.altura = max([self.altura(aux.izq), self.altura(aux.der)]) + 1
        return aux
    
    def rotacionDI(self, root):
        root.izq = self.rotacionD(root.izq)
        temp = self.rotacionI(root)
        return temp

    def rotacionDD(self, root):
        root.der = self.rotacionI(root.der)
        temp = self.rotacionD(root)
        return temp

    def agregarAVL(self, root, nuevo):
        padre = root
        if(nuevo.carnet < root.carnet):
            if(root.izq == None):
                root.izq = nuevo
            else:
                root.izq = self.agregarAVL(root.izq, nuevo)
                if(self.factor(root.izq) - self.factor(root.der) == 2):
                    if(nuevo.carnet < root.izq.carnet):
                       padre = self.rotacionI(root)
                    else:
                        padre =  self.rotacionDI(root)
        elif(nuevo.carnet > root.carnet):
            if(root.der == None):
                root.der = nuevo
            else:
                root.der = self.agregarAVL(root.der, nuevo)
                if(self.factor(root.der) - self.factor(root.izq) == 2):
                    if(nuevo.carnet > root.der.carnet):
                       padre = self.rotacionD(root)
                    else:
                        padre =  self.rotacionDD(root)
        else:
            print("Nodo duplicado")

        if(root.izq == None and root.der != None):
            root.factor = root.der.factor + 1
            root.altura = self.altura(root.der) + 1
        elif(root.izq != None and root.der == None):
            root.factor = root.izq.factor + 1
            root.altura = self.altura(root.izq) + 1
        else:
            root.factor = max([self.factor(root.izq), self.factor(root.der)]) + 1
            root.altura = max([self.altura(root.izq), self.altura(root.der)]) + 1

        self.root = padre
        return padre

    def inorder(self, root):
        if(root.izq != None):
            self.inorder(root.izq)

        print("Carne: " + str(root.carnet) + " Nombre: " + root.nombre + " Altura: " + str(root.altura) + " Factor: " + str(root.factor))

        if(root.der != None):
            self.inorder(root.der)

    def preorder(self, root):
        print("Carne: " + str(root.carnet) + " Nombre: " + root.nombre + " Altura: " + str(root.altura) + " Factor: " + str(root.factor))

        if(root.izq != None):
            self.inorder(root.izq)

        if(root.der != None):
            self.inorder(root.der)

    def posorder(self, root):
        if(root.izq != None):
            self.inorder(root.izq)

        if(root.der != None):
            self.inorder(root.der)

        print("Carne: " + str(root.carnet) + " Nombre: " + root.nombre + " Altura: " + str(root.altura) + " Factor: " + str(root.factor))