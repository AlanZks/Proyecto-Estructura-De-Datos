# --------- Árbol Binario de Búsqueda con Mediana de Tres (ABBm3) ---------

class HojaABBm3:
    def __init__(self, llaves):
        self.llaves = sorted(llaves)        # La hoja almacena hasta 3 llaves de manera ordenada
        self.hoja = True                    # Marca el nodo como hoja

# --------- Definición del nodo interno para ABBm3 ---------
class NodoABBm3:
    def __init__(self, separador):
        self.separador = separador      # LLave que separa dos ramas (subárboles)
        self.izq = None                 # Subárbol izquierdo
        self.der = None                 # Subárbol derecho
        self.hoja = False               # Nodo interno, no hoja

# --------- Clase principal del Árbol ABBm3 ---------
class ABBm3:
    def __init__(self):
        self.raiz = None            # Nodo raíz del árbol
        self.comparaciones = 0      # Comparaciones realizadas en la operación actual
        self.divisiones = 0         # Conteo de divisiones de hoja
        self.altura = 0             # Altura del árbol
        self.camino = []            # Guarda los nodos visitados en la última operación

# --------- Insertar para ABBm3 ---------
    # Inserta una nueva llave en el árbol, usando inserción recursiva.
    def insertar(self, llave):
        self.comparaciones = 0
        self.camino = []
        self.raiz = self.insertar_recursivo(self.raiz, llave)
        self.altura = self.altura_arbol(self.raiz)

    def insertar_recursivo(self, nodo, llave):
        if nodo is None:                       # Si el nodo es nulo, crea una nueva hoja con la llave
            hoja = HojaABBm3([llave])
            self.camino.append(hoja)
            return hoja

        if nodo.hoja:
            self.comparaciones += 1
            self.camino.append(nodo)
            existe = False                   # Verifica si la llave ya existe en la hoja
            for valor in nodo.llaves:
                if valor == llave:
                    existe = True
                    break
            if existe:
                return nodo                     # no acepta duplicados
            if len(nodo.llaves) < 3:         # Si hay espacio en la hoja, agrega la nueva llave y ordena
                nodo.llaves.append(llave)
                nodo.llaves.sort()
                return nodo
            self.divisiones += 1   # Aumenta el contador de divisiones
            llaves_originales = list(nodo.llaves)    # Si la hoja está llena, se divide usando la mediana
            llaves_originales.sort()
            mediana = llaves_originales[1]
            menor = llaves_originales[0]
            mayor = llaves_originales[2]
            nuevo_nodo = NodoABBm3(mediana)
            nuevo_nodo.izq = HojaABBm3([menor])
            nuevo_nodo.der = HojaABBm3([mayor])
            return self.insertar_recursivo(nuevo_nodo, llave)  # Inserta la nueva llave en el subárbol correspondiente


        self.comparaciones += 1
        self.camino.append(nodo)                    # Si es un nodo interno, decide a qué subárbol ir
        if llave < nodo.separador:
            nodo.izq = self.insertar_recursivo(nodo.izq, llave)
        else:
            nodo.der = self.insertar_recursivo(nodo.der, llave)
        return nodo

    # --------- Buscar para ABBm3 ---------

    def buscar(self, llave):   # Busca una llave en el árbol
        self.comparaciones = 0
        self.camino = []
        return self.buscar_recursivo(self.raiz, llave)

    def buscar_recursivo(self, nodo, llave):
        if nodo is None:
            return False
        self.camino.append(nodo)

        if nodo.hoja:                  # Si encuentra una hoja, busca la llave
            self.comparaciones += 1
            for valor in nodo.llaves:
                if valor == llave:
                    return True
            return False
        self.comparaciones += 1          # Si es nodo interno, lo compara con el separador y baja al subárbol
        if llave == nodo.separador:
            return True
        elif llave < nodo.separador:
            return self.buscar_recursivo(nodo.izq, llave)
        else:
            return self.buscar_recursivo(nodo.der, llave)

    # --------- Eliminar para ABBm3 ---------
    def eliminar(self, llave):              # Elimina una llave del árbol
        self.comparaciones = 0
        self.camino = []
        self.raiz = self.eliminar_recursivo(self.raiz, llave)
        while self.raiz is not None and not self.raiz.hoja:   # Promueve subárbol si la raíz se reduce a un solo hijo
            izq = self.raiz.izq
            der = self.raiz.der
            if izq is None and der is not None:     #En caso de que uno de los hijos exista
                self.raiz = der
            elif der is None and izq is not None:       #Ambos hijos vaciós
                self.raiz = izq
            elif izq is None and der is None:
                self.raiz = None
            else:
                break           #Si ambos hijos existe, no se promueve nada

        if self.raiz is not None and self.raiz.hoja and len(self.raiz.llaves) == 0:     #Elimina la raiz vacia  si la hoja no tiene llaves
            self.raiz = None
        self.altura = self.altura_arbol(self.raiz)

    def eliminar_recursivo(self, nodo, llave):
        if nodo is None:
            return None
        self.camino.append(nodo)
                                            # Si llegamos a una hoja, elimina la llave si existe
        if nodo.hoja:
            self.comparaciones += 1
            if llave not in nodo.llaves:
                return nodo         #Si la  llave no existe
            nodo.llaves.remove(llave)    #Se elimina la llave
            if len(nodo.llaves) == 0:
                return None                 #La hoja queda vacia
            return nodo

        self.comparaciones += 1
        if llave < nodo.separador:                      # Si la llave es menor al separador, lo elimina en el subárbol izquierdo
            nodo.izq = self.eliminar_recursivo(nodo.izq, llave)         #Si la hoja izquierda queda vacia , se funciona con la de la derecha
            if nodo.izq is None and nodo.der is not None and nodo.der.hoja:
                nueva_llaves = [nodo.separador] + nodo.der.llaves
                return HojaABBm3(nueva_llaves)
                                                                                # Si la llave es mayor al separador, elimina en el subárbol derecho
        elif llave > nodo.separador:
            nodo.der = self.eliminar_recursivo(nodo.der, llave)
                                                                            # Si la hoja derecha quedó vacía, fusiona con la izquierda y convierte en hoja
            if nodo.der is None and nodo.izq is not None and nodo.izq.hoja:
                nueva_llaves = nodo.izq.llaves + [nodo.separador]
                return HojaABBm3(nueva_llaves)
        else:
                                                                # Caso: la llave es igual al separador, buscar un reemplazo
            if nodo.izq is not None and nodo.der is not None:
                if nodo.izq.hoja and nodo.der.hoja:
                    if len(nodo.izq.llaves) >= len(nodo.der.llaves):
                        reemplazo = max(nodo.izq.llaves)
                        nodo.separador = reemplazo
                        nodo.izq = self.eliminar_recursivo(nodo.izq, reemplazo)
                    else:
                        reemplazo = min(nodo.der.llaves)
                        nodo.separador = reemplazo
                        nodo.der = self.eliminar_recursivo(nodo.der, reemplazo)
                elif nodo.izq.hoja:
                    reemplazo = max(nodo.izq.llaves)
                    nodo.separador = reemplazo
                    nodo.izq = self.eliminar_recursivo(nodo.izq, reemplazo)
                elif nodo.der.hoja:
                    reemplazo = min(nodo.der.llaves)
                    nodo.separador = reemplazo
                    nodo.der = self.eliminar_recursivo(nodo.der, reemplazo)
                else:
                                                                        # Buscar el máximo en el subárbol izquierdo (caso general)
                    temp = self._maximo_nodo_y_padre(nodo.izq, nodo)
                    nodo.separador = temp[0].llaves[-1]
                    nodo.izq = self.eliminar_recursivo(nodo.izq, nodo.separador)
            elif nodo.izq is not None:
                return nodo.izq
            elif nodo.der is not None:
                return nodo.der
            else:
                return None

                                                                # Limpia en caso de si alguno de los hijos es hoja vacía
        if nodo.izq is not None and nodo.der is not None:
            if nodo.izq.hoja and len(nodo.izq.llaves) == 0:
                return nodo.der
            if nodo.der.hoja and len(nodo.der.llaves) == 0:
                return nodo.izq
        return nodo

    # --------- Mínimo y Máximo nodo (eliminación) para ABBm3 ---------
                                                        # Obtiene el valor mínimo en el subárbol
    def _minimo_valor_subarbol(self, nodo):
        if nodo is None:
            return None
        if nodo.hoja:
            return min(nodo.llaves) if nodo.llaves else None
        return self._minimo_valor_subarbol(nodo.izq)

                                                                    # Obtiene el valor máximo en el subárbol
    def _maximo_valor_subarbol(self, nodo):
        if nodo is None:
            return None
        if nodo.hoja:
            return max(nodo.llaves) if nodo.llaves else None
        return self._maximo_valor_subarbol(nodo.der)

    # --------- Altura del nodo de ABBm3 ---------
                                                            # Calcula recursivamente la altura del árbol
    def altura_arbol(self, nodo):
        if nodo is None:
            return 0
        if nodo.hoja:
            return 1
        izq_altura = self.altura_arbol(nodo.izq)
        der_altura = self.altura_arbol(nodo.der)
        return 1 + max(izq_altura, der_altura)

    # --------- Total de nodos para ABBm3 ---------
                                                                            # Cuenta el total de nodos
    def contar_nodos(self):
        return self._contar_nodos(self.raiz)

    def _contar_nodos(self, nodo):            # Recursivo para contar nodos
        if nodo is None:
            return 0
        if nodo.hoja:
            return 1
        return 1 + self._contar_nodos(nodo.izq) + self._contar_nodos(nodo.der)

    # --------- Factor de equilibrio de ABBm3 ---------

    def factor_equilibrio(self, nodo=None): # Calcula el factor de equilibrio de un nodo
        if nodo is None:
            nodo = self.raiz
        if nodo is None or nodo.hoja:
            return 0
        izq_altura = self.altura_arbol(nodo.izq)
        der_altura = self.altura_arbol(nodo.der)
        feq = izq_altura - der_altura
        if feq == 0:
            return 0
        elif feq == 1 or feq == -1:
            return feq
        else:
            return feq

    # --------- Formato visual de llaves en hoja (ABBm3) ---------
    def llaves_a_cadena(self, lista):         # Convierte una lista de llaves a cadena con formato {a,b,c}
        cadena = "{"
        i = 0
        for valor in lista:
            cadena += str(valor)
            if i < len(lista) - 1:
                cadena += ","
            i += 1
        cadena += "}"
        return cadena


