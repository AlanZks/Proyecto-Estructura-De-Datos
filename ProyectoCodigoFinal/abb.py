# --------- Árbol Binario de Búsqueda (ABB) ---------

class NodoABB:
    def __init__(self, valor):
        self.valor = valor          #Valor del nodo
        self.izq = None             #Referencia al subárbol izquierdo
        self.der = None             #Referencia al subárbol derecho
        self.hoja = False           #No se utiliza pero esta para compatibilidad de la interfaz

class ABB:
    def __init__(self):
        self.raiz = None            #Nodo ráiz del arbol
        self.comparaciones = 0      #Comparaciones realizadas por operación
        self.altura = 0             #Altura del arbol
        self.camino = []            #Guarda los nodos visitados en la ultima operacion

# ---------Insertar para ABBm---------

    def insertar(self, valor):
        self.comparaciones = 0              #Se reinicia el contador de comparaciones
        self.camino = []                    #Limpia el camino de nodos anterior
        self.raiz = self.insertar_recursivo(self.raiz, valor)       #Inserta el valor de manera recursiva
        self.altura = self.altura_arbol(self.raiz)              #Actualiza la altura del arbol

    def insertar_recursivo(self, nodo, valor):
        if nodo is None:
            nuevo = NodoABB(valor)              #En caso de tener la hoja vacia se crea un nuevo nodo
            self.camino.append(nuevo)           #Registra el nodo en el camino recorrido
            return nuevo
        self.comparaciones += 1                 #Cuenta la comparacion actual
        self.camino.append(nodo)                  #Guarda el nodo visitado
        if valor < nodo.valor:
            nodo.izq = self.insertar_recursivo(nodo.izq, valor)
        elif valor > nodo.valor:                                #Se inserta un nodo al subárbol izquierdo /al igual al derecho
            nodo.der = self.insertar_recursivo(nodo.der, valor)
        elif valor == nodo.valor:
            return nodo
        return nodo                                     #En caso de ser iguales, no se inserta

# ---------Buscar para ABBm---------

    def buscar(self, valor):
        self.comparaciones = 0
        self.camino = []
        return self.buscar_recursivo(self.raiz, valor)  #Se llama la busqueda recursiva desde la raiz

    def buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return False
        self.comparaciones += 1
        self.camino.append(nodo)        #Guarda el nodo visitado

        if valor == nodo.valor:
            return True
        elif valor < nodo.valor:
            return self.buscar_recursivo(nodo.izq, valor)
        else:                                               #Busca para el subárbol izquierdo / derecho
            return self.buscar_recursivo(nodo.der, valor)

# ---------Eliminar para ABBm---------

    def eliminar(self, valor):
        self.comparaciones = 0
        self.camino = []
        self.raiz = self.eliminar_recursivo(self.raiz, valor)   #Inicia la eliminacion recursiva
        self.altura = self.altura_arbol(self.raiz)              #Actualiza la altura del arbol

    def eliminar_recursivo(self, nodo, valor):
        if nodo is None:
            return nodo                                      #Si no se encuentra el valor, se retorna el nodo original
        self.comparaciones += 1
        self.camino.append(nodo)                #Guarda el nodo visitado
        if valor < nodo.valor:
            nodo.izq = self.eliminar_recursivo(nodo.izq, valor)
        elif valor > nodo.valor:                                #Busca para el subárbol izquierdo / derecho
            nodo.der = self.eliminar_recursivo(nodo.der, valor)
        else:
            if nodo.izq is None:
                return nodo.der                 #Remplaza por hijo derecho (En caso de no haber izquierdo)
            elif nodo.der is None:
                return nodo.izq                 #Remplaza por hijo izquierdo (En caso de haber derecho)
                                                #en caso de dos hijos, se remplazan por el sucesor inorden
            temp = self.minimo_nodo(nodo.der)
            nodo.valor = temp.valor
            nodo.der = self.eliminar_recursivo(nodo.der, temp.valor)        #Elimina el sucesor
        return nodo

# ---------Mínimo nodo (eliminación) para ABB---------

    def minimo_nodo(self, nodo):
        actual = nodo
        while actual.izq is not None:
            self.comparaciones += 1     #Cuenta las comparaciones al recorrer hacia la izquierda
            actual = actual.izq         #Avanza al nodo más a la izquierda
        return actual                   #Retorna el nodo con el minimo valor

# ---------Altura del nodo de ABBm---------

    def altura_arbol(self, nodo):
        if nodo is None:
            return 0                        #Nodo nulo tiene altura 0
        izq_altura = self.altura_arbol(nodo.izq)        #Calcula la altura del subarbol izq/der
        der_altura = self.altura_arbol(nodo.der)
        if izq_altura > der_altura:
            mayor = izq_altura
        else:
            mayor = der_altura
        return mayor + 1                #La altura es 1 + la mayor entre ambos lado

# --------- Total de nodos para ABBm---------
    def contar_nodos(self):
        return self._contar_nodos(self.raiz)            #Comienza el conteo desde la raíz

    def _contar_nodos(self, nodo):
        if nodo is None:
            return 0                                #Nodo nulo no cuenta
        return 1 + self._contar_nodos(nodo.izq) + self._contar_nodos(nodo.der) #Cuenta el nodo actual y el de ambos subárboles

# --------- Factor de equilibrio de n ABBm---------
    def factor_equilibrio(self, nodo=None):
        if nodo is None:
            nodo = self.raiz                        #Si no pasa el nodo , se utiliza la raiz
        if nodo is None:
            return 0                                #Arbol vacio, significa equilibrio neutro

        izq_altura = self.altura_arbol(nodo.izq)        #Altura del subárbol izquierdo
        der_altura = self.altura_arbol(nodo.der)        #Altura del subárbol derecho
        feq = der_altura - izq_altura

        if feq == 0:
            return 0                    #Arbol perfectamente equilibrado
        elif feq == 1 or feq == -1:
            return feq                  #Leve desbalance h
        else:
            return feq                  #Un mayor desbalance

