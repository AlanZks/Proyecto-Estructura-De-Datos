# --------- Importaciones y utilidades ---------
import tkinter as tk
from tkinter import ttk, messagebox
from abb import ABB
from abbm3 import ABBm3
import datetime
import time

# --------- Función para verificar si un número es primo ---------
def es_primo(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

# --------- Función para determinar el color de un nodo ---------
def color_nodo(nodo, abb_clase, es_abbm3):
    # Para ABBm3: hojas con números primos en azul, otras en verde
    if es_abbm3:
        if nodo.hoja:
            tiene_primo = False
            for k in nodo.llaves:
                if es_primo(k):
                    tiene_primo = True
                    break
            if tiene_primo:
                return "#63a4ff"
            return "#b8e994"
    else:
        # Para ABB normal: azul si el valor es primo
        if nodo.valor is not None and es_primo(nodo.valor):
            return "#63a4ff"
    # Color por factor de equilibrio (balance del nodo)
    feq = abb_clase.factor_equilibrio(nodo)
    if feq == 0:
        return "#b9f6ca"
    elif feq == 1 or feq == -1:
        return "#fff59d"
    else:
        return "#ff8a80"

# --------- Clase principal para la interfaz visual ---------
class VisualizadorArboles(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Árboles Binarios")
        self.geometry("1920x700")
        self.minsize(1200, 600)


        self.abb = ABB()             # Instancias de ABB y ABBm3
        self.abbm3 = ABBm3()
        self.ultimo_camino_abb = []    # Variables para almacenar el último camino recorrido y tiempos de operación
        self.ultimo_camino_abbm3 = []
        self.tiempo_abb = 0.0
        self.tiempo_abbm3 = 0.0

        self.crear_interfaz()            # Construcción de la interfaz grafica

    # --------- Construcción de la interfaz gráfica ---------
    def crear_interfaz(self):
        # Título
        etiqueta_titulo = tk.Label(self, text="Interfaz Visual para Árboles Binarios", font=("Arial", 16, "bold"))
        etiqueta_titulo.pack(pady=10)

        # Marcos principales para los árboles
        marco = tk.Frame(self)
        marco.pack(fill=tk.BOTH, expand=True)

        # Canvas para el ABB
        self.lienzo_abb = tk.Canvas(marco, bg="white", width=880, height=500)
        self.lienzo_abb.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        self.lienzo_abb.create_text(440, 20, text="Visualización ABB", font=("Arial", 12, "bold"))

        # Canvas para el  ABBm3
        self.lienzo_abbm3 = tk.Canvas(marco, bg="white", width=880, height=500)
        self.lienzo_abbm3.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        self.lienzo_abbm3.create_text(440, 20, text="Visualización ABBm3", font=("Arial", 12, "bold"))

        # --------- Controles de operaciones ---------
        controles = tk.Frame(self)
        controles.pack(pady=10)

        # Entrada y botón para insertar
        tk.Label(controles, text="Insertar:").grid(row=0, column=0)
        self.entrada_insertar = tk.Entry(controles, width=5)
        self.entrada_insertar.grid(row=0, column=1)
        boton_insertar = ttk.Button(controles, text="➕", command=self.insertar_valor)
        boton_insertar.grid(row=0, column=2, padx=5)

        # Entrada y botón para eliminar
        tk.Label(controles, text="Eliminar:").grid(row=0, column=3)
        self.entrada_eliminar = tk.Entry(controles, width=5)
        self.entrada_eliminar.grid(row=0, column=4)
        boton_eliminar = ttk.Button(controles, text="🗑️", command=self.eliminar_valor)
        boton_eliminar.grid(row=0, column=5, padx=5)

        # Entrada y botón para buscar
        tk.Label(controles, text="Buscar:").grid(row=0, column=6)
        self.entrada_buscar = tk.Entry(controles, width=5)
        self.entrada_buscar.grid(row=0, column=7)
        boton_buscar = ttk.Button(controles, text="🔍", command=self.buscar_valor)
        boton_buscar.grid(row=0, column=8, padx=5)

        # Botón para ver el recorrido paso a paso
        boton_paso = ttk.Button(controles, text="Paso a paso", command=self.mostrar_ultimo_camino)
        boton_paso.grid(row=0, column=9, padx=5)

        # Botón para mostrar estadísticas
        boton_estadisticas = ttk.Button(controles, text="Estadísticas", command=self.mostrar_estadisticas)
        boton_estadisticas.grid(row=0, column=10, padx=5)

        # Botón para resetear ambos árboles
        boton_resetear = ttk.Button(controles, text="Resetear", command=self.resetear_arboles)
        boton_resetear.grid(row=0, column=11, padx=5)

    # --------- Insertar valor en ambos árboles ---------
    def insertar_valor(self):
        try:
            valor = int(self.entrada_insertar.get())
            lineas_log = []
            lineas_log.append(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Inserción de {valor}")

            # ABB
            inicio_abb = time.time()
            self.abb.insertar(valor)
            final_abb = time.time()
            self.tiempo_abb = (final_abb - inicio_abb) * 1000
            self.ultimo_camino_abb = self.abb.camino
            camino_abb = self.camino_a_cadena(self.ultimo_camino_abb)
            lineas_log.append(f"ABB  - Camino: {camino_abb}")
            lineas_log.append(f"ABB  - Comparaciones: {self.abb.comparaciones}")
            lineas_log.append(f"ABB  - Tiempo (ms): {self.tiempo_abb:.2f}")

            # ABBm3
            inicio_abbm3 = time.time()
            self.abbm3.insertar(valor)
            final_abbm3 = time.time()
            self.tiempo_abbm3 = (final_abbm3 - inicio_abbm3) * 1000
            self.ultimo_camino_abbm3 = self.abbm3.camino
            camino_abbm3 = self.camino_a_cadena(self.ultimo_camino_abbm3)
            lineas_log.append(f"ABBm3- Camino: {camino_abbm3}")
            lineas_log.append(f"ABBm3- Comparaciones: {self.abbm3.comparaciones}")
            lineas_log.append(f"ABBm3- Tiempo (ms): {self.tiempo_abbm3:.2f}")

            self.guardar_procedimiento(lineas_log)
            self.redibujar()
            self.entrada_insertar.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido")

    # --------- Eliminar valor de ambos árboles ---------
    def eliminar_valor(self):
        try:
            valor = int(self.entrada_eliminar.get())
            lineas_log = []
            lineas_log.append(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Eliminación de {valor}")

            # ABB
            inicio_abb = time.time()
            self.abb.eliminar(valor)
            final_abb = time.time()
            self.tiempo_abb = (final_abb - inicio_abb) * 1000
            self.ultimo_camino_abb = self.abb.camino
            camino_abb = self.camino_a_cadena(self.ultimo_camino_abb)
            lineas_log.append(f"ABB  - Camino: {camino_abb}")
            lineas_log.append(f"ABB  - Comparaciones: {self.abb.comparaciones}")
            lineas_log.append(f"ABB  - Tiempo (ms): {self.tiempo_abb:.2f}")

            # ABBm3
            inicio_abbm3 = time.time()
            self.abbm3.eliminar(valor)
            final_abbm3 = time.time()
            self.tiempo_abbm3 = (final_abbm3 - inicio_abbm3) * 1000
            self.ultimo_camino_abbm3 = self.abbm3.camino
            camino_abbm3 = self.camino_a_cadena(self.ultimo_camino_abbm3)
            lineas_log.append(f"ABBm3- Camino: {camino_abbm3}")
            lineas_log.append(f"ABBm3- Comparaciones: {self.abbm3.comparaciones}")
            lineas_log.append(f"ABBm3- Tiempo (ms): {self.tiempo_abbm3:.2f}")

            self.guardar_procedimiento(lineas_log)
            self.redibujar()
            self.entrada_eliminar.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido")

    # --------- Buscar valor en ambos árboles ---------
    def buscar_valor(self):
        try:
            valor = int(self.entrada_buscar.get())
            lineas_log = []
            lineas_log.append(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Búsqueda de {valor}")

            # Limpia caminos previos
            self.abb.camino = []
            self.abbm3.camino = []

            # ABB
            inicio_abb = time.time()
            encontrado_abb = self.abb.buscar(valor)
            final_abb = time.time()
            self.tiempo_abb = (final_abb - inicio_abb) * 1000
            self.ultimo_camino_abb = self.abb.camino
            camino_abb = self.camino_a_cadena(self.ultimo_camino_abb)
            lineas_log.append(f"ABB  - Camino: {camino_abb}")
            lineas_log.append(f"ABB  - Comparaciones: {self.abb.comparaciones}")
            if encontrado_abb:
                lineas_log.append("ABB  - Resultado: Encontrado")
            else:
                lineas_log.append("ABB  - Resultado: No encontrado")
            lineas_log.append(f"ABB  - Tiempo (ms): {self.tiempo_abb:.2f}")

            # ABBm3
            inicio_abbm3 = time.time()
            encontrado_abbm3 = self.abbm3.buscar(valor)
            final_abbm3 = time.time()
            self.tiempo_abbm3 = (final_abbm3 - inicio_abbm3) * 1000
            self.ultimo_camino_abbm3 = self.abbm3.camino
            camino_abbm3 = self.camino_a_cadena(self.ultimo_camino_abbm3)
            lineas_log.append(f"ABBm3- Camino: {camino_abbm3}")
            lineas_log.append(f"ABBm3- Comparaciones: {self.abbm3.comparaciones}")
            if encontrado_abbm3:
                lineas_log.append("ABBm3- Resultado: Encontrado")
            else:
                lineas_log.append("ABBm3- Resultado: No encontrado")
            lineas_log.append(f"ABBm3- Tiempo (ms): {self.tiempo_abbm3:.2f}")

            mensaje = (
                f"Valor {valor}\n"
                f"ABB: {'Encontrado' if encontrado_abb else 'No encontrado'}\n"
                f"ABBm3: {'Encontrado' if encontrado_abbm3 else 'No encontrado'}"
            )
            messagebox.showinfo("Resultado de búsqueda", mensaje)

            self.guardar_procedimiento(lineas_log)
            self.redibujar()
            self.entrada_buscar.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido")

    # --------- Convierte un camino de nodos en cadena legible ---------
    def camino_a_cadena(self, camino):
        nombres = []
        for n in camino:
            if n is None:
                continue
            if hasattr(n, 'hoja') and n.hoja:
                cadena = "{"
                i = 0
                for valor in n.llaves:
                    cadena += str(valor)
                    if i < len(n.llaves) - 1:
                        cadena += ","
                    i += 1
                cadena += "}"
                nombres.append(cadena)
            elif hasattr(n, 'valor'):
                nombres.append("[" + str(n.valor) + "]")
            else:
                nombres.append("[" + str(n.separador) + "]")
        return " -> ".join(nombres)

    # --------- Guarda el procedimiento en un archivo (procedimientos.txt) ---------
    def guardar_procedimiento(self, lineas):
        with open("procedimientos.txt", "a", encoding="utf-8") as archivo:
            for l in lineas:
                archivo.write(l + "\n")

    # --------- Resetea ambos árboles ---------
    def resetear_arboles(self):
        self.abb = ABB()
        self.abbm3 = ABBm3()
        self.ultimo_camino_abb = []
        self.ultimo_camino_abbm3 = []
        self.tiempo_abb = 0.0
        self.tiempo_abbm3 = 0.0
        self.redibujar()

    # --------- Muestra estadisticas comparativas ---------
    def mostrar_estadisticas(self):
        ventana_estadisticas = tk.Toplevel(self)
        ventana_estadisticas.title("Estadísticas Comparativas")
        ventana_estadisticas.geometry("700x320")

        tk.Label(ventana_estadisticas, text="Estadísticas Comparativas", font=("Arial", 14, "bold")).pack(pady=10)

        marco = tk.Frame(ventana_estadisticas)
        marco.pack(pady=10)

        encabezados = ["Métrica", "ABB", "ABBm3"]
        i = 0
        while i < len(encabezados):
            tk.Label(marco, text=encabezados[i], font=("Arial", 12, "bold"), borderwidth=1, relief="solid", width=18, padx=5).grid(row=0, column=i, sticky="nsew")
            i += 1

        estadisticas = [
            ("Comparaciones", str(self.abb.comparaciones), str(self.abbm3.comparaciones)),
            ("Divisiones de hoja", "-", str(self.abbm3.divisiones)),  # ABB no tiene divisiones de hoja
            ("Altura", str(self.abb.altura), str(self.abbm3.altura)),
            ("Nodos", str(self.abb.contar_nodos()), str(self.abbm3.contar_nodos())),
            ("Factor equilibrio (raíz)", str(self.abb.factor_equilibrio()), str(self.abbm3.factor_equilibrio())),
            ("Tiempo (ms)", f"{self.tiempo_abb:.2f}", f"{self.tiempo_abbm3:.2f}")
        ]

        j = 0
        while j < len(estadisticas):
            met, abb_val, abbm3_val = estadisticas[j]
            tk.Label(marco, text=met, borderwidth=1, relief="solid", width=18).grid(row=j+1, column=0, sticky="nsew")
            tk.Label(marco, text=abb_val, borderwidth=1, relief="solid", width=18).grid(row=j+1, column=1, sticky="nsew")
            tk.Label(marco, text=abbm3_val, borderwidth=1, relief="solid", width=18).grid(row=j+1, column=2, sticky="nsew")
            j += 1

    # --------- Redibuja ambos árboles en sus canvas ---------
    def redibujar(self):
        self.lienzo_abb.delete("all")
        self.lienzo_abbm3.delete("all")
        ancho_canvas = 880
        margen_izq = 100
        margen_der = 100
        y_inicio = 50
        x_centro = ancho_canvas // 2

        if hasattr(self.abb, "altura"):
            max_profundidad_abb = self.abb.altura
        else:
            max_profundidad_abb = 1
        if hasattr(self.abbm3, "altura"):
            max_profundidad_abbm3 = self.abbm3.altura
        else:
            max_profundidad_abbm3 = 1

        def calcular_dx(profundidad, max_profundidad):
            dx_min = 25
            dx_max = (ancho_canvas - margen_izq - margen_der) // 2
            if max_profundidad < 2:
                return dx_max
            factor = 1
            i = 0
            while i < profundidad:
                factor = factor * 2
                i += 1
            dx = dx_max // factor
            if dx < dx_min:
                dx = dx_min
            return dx

        self.lienzo_abb.create_text(x_centro, 20, text="Visualización ABB", font=("Arial", 12, "bold"))
        self.dibujar_arbol(self.lienzo_abb, self.abb.raiz, x_centro, y_inicio, 0, camino=self.ultimo_camino_abb,
                        funcion_dx=lambda d: calcular_dx(d, max_profundidad_abb), es_abbm3=False, profundidad=0)

        self.lienzo_abbm3.create_text(x_centro, 20, text="Visualización ABBm3", font=("Arial", 12, "bold"))
        self.dibujar_arbol(self.lienzo_abbm3, self.abbm3.raiz, x_centro, y_inicio, 0, camino=self.ultimo_camino_abbm3,
                        funcion_dx=lambda d: calcular_dx(d, max_profundidad_abbm3), es_abbm3=True, profundidad=0)

    # --------- Dibuja recursivamente un árbol en su canvas ---------
    def dibujar_arbol(self, lienzo, nodo, x, y, dx, camino=None, funcion_dx=None, es_abbm3=False, profundidad=0):
        if not nodo:
            return

        nodo_en_camino = False
        if camino:
            i = 0
            while i < len(camino):
                if nodo == camino[i]:
                    nodo_en_camino = True
                    break
                i += 1

        relleno_rect = color_nodo(nodo, self.abb if not es_abbm3 else self.abbm3, es_abbm3)
        if nodo_en_camino:
            relleno_rect = "#ffe599"

        # Etiqueta visual y tamaño del nodo
        if es_abbm3:
            if nodo.hoja:
                etiqueta = "{"
                i = 0
                for valor in nodo.llaves:
                    etiqueta += str(valor)
                    if i < len(nodo.llaves) - 1:
                        etiqueta += ","
                    i += 1
                etiqueta += "}"
                ancho_rect = 12 + 8 * len(nodo.llaves)
                if ancho_rect < 20:
                    ancho_rect = 20
            else:
                etiqueta = "[" + str(nodo.separador) + "]"
                ancho_rect = 28
        else:
            etiqueta = str(nodo.valor)
            ancho_rect = 24

        lienzo.create_rectangle(x - ancho_rect, y - 15, x + ancho_rect, y + 15, fill=relleno_rect, outline="black")
        lienzo.create_text(x, y, text=etiqueta, font=("Arial", 10, "bold"))

        dx_siguiente = 90
        if funcion_dx:
            dx_siguiente = funcion_dx(profundidad+1)

        # Dibuja ramas del árbol según tipo
        if es_abbm3:
            if not nodo.hoja:
                if nodo.izq:
                    lienzo.create_line(x, y + 15, x - dx_siguiente, y + 60 - 15)
                    self.dibujar_arbol(lienzo, nodo.izq, x - dx_siguiente, y + 60, dx_siguiente, camino=camino, funcion_dx=funcion_dx, es_abbm3=es_abbm3, profundidad=profundidad+1)
                if nodo.der:
                    lienzo.create_line(x, y + 15, x + dx_siguiente, y + 60 - 15)
                    self.dibujar_arbol(lienzo, nodo.der, x + dx_siguiente, y + 60, dx_siguiente, camino=camino, funcion_dx=funcion_dx, es_abbm3=es_abbm3, profundidad=profundidad+1)
        else:
            if nodo.izq:
                lienzo.create_line(x, y + 15, x - dx_siguiente, y + 60 - 15)
                self.dibujar_arbol(lienzo, nodo.izq, x - dx_siguiente, y + 60, dx_siguiente, camino=camino, funcion_dx=funcion_dx, es_abbm3=es_abbm3, profundidad=profundidad+1)
            if nodo.der:
                lienzo.create_line(x, y + 15, x + dx_siguiente, y + 60 - 15)
                self.dibujar_arbol(lienzo, nodo.der, x + dx_siguiente, y + 60, dx_siguiente, camino=camino, funcion_dx=funcion_dx, es_abbm3=es_abbm3, profundidad=profundidad+1)

    # --------- Muestra el último camino recorrido (ventana paso a paso) ---------
    def mostrar_ultimo_camino(self):
        VentanaPasoAPaso(self,
                         camino_abb=self.ultimo_camino_abb,
                         camino_abbm3=self.ultimo_camino_abbm3,
                         raiz_abb=self.abb.raiz,
                         raiz_abbm3=self.abbm3.raiz)

# --------- Ventana para mostrar el recorrido paso a paso ---------
class VentanaPasoAPaso(tk.Toplevel):
    def __init__(self, master, camino_abb, camino_abbm3, raiz_abb, raiz_abbm3):
        super().__init__(master)
        self.title("Paso a Paso - Recorrido")
        self.geometry("1000x600")
        self.camino_abb = camino_abb or []
        self.camino_abbm3 = camino_abbm3 or []
        self.raiz_abb = raiz_abb
        self.raiz_abbm3 = raiz_abbm3
        self.indice_abb = 0
        self.indice_abbm3 = 0

        # Canvas para ABB
        self.lienzo_abb = tk.Canvas(self, bg="white", width=480, height=400)
        self.lienzo_abb.grid(row=0, column=0, padx=10, pady=10)
        self.lienzo_abb.create_text(240, 20, text="ABB", font=("Arial", 12, "bold"))

        # Canvas para ABBm3
        self.lienzo_abbm3 = tk.Canvas(self, bg="white", width=480, height=400)
        self.lienzo_abbm3.grid(row=0, column=1, padx=10, pady=10)
        self.lienzo_abbm3.create_text(240, 20, text="ABBm3", font=("Arial", 12, "bold"))

        # Controles de navegación
        marco_nav = tk.Frame(self)
        marco_nav.grid(row=1, column=0, columnspan=2, pady=10)

        tk.Label(marco_nav, text="ABB Paso:").grid(row=0, column=0)
        self.boton_prev_abb = ttk.Button(marco_nav, text="⬅️", command=self.prev_abb)
        self.boton_prev_abb.grid(row=0, column=1)
        self.etiqueta_paso_abb = tk.Label(marco_nav, text="1 / " + str(max(1, len(self.camino_abb))))
        self.etiqueta_paso_abb.grid(row=0, column=2)
        self.boton_next_abb = ttk.Button(marco_nav, text="➡️", command=self.next_abb)
        self.boton_next_abb.grid(row=0, column=3)

        tk.Label(marco_nav, text="   ").grid(row=0, column=4)

        tk.Label(marco_nav, text="ABBm3 Paso:").grid(row=0, column=5)
        self.boton_prev_abbm3 = ttk.Button(marco_nav, text="⬅️", command=self.prev_abbm3)
        self.boton_prev_abbm3.grid(row=0, column=6)
        self.etiqueta_paso_abbm3 = tk.Label(marco_nav, text="1 / " + str(max(1, len(self.camino_abbm3))))
        self.etiqueta_paso_abbm3.grid(row=0, column=7)
        self.boton_next_abbm3 = ttk.Button(marco_nav, text="➡️", command=self.next_abbm3)
        self.boton_next_abbm3.grid(row=0, column=8)

        self.redibujar_ambos()

    # --------- Redibuja ambos recorridos ---------
    def redibujar_ambos(self):
        self.redibujar_abb()
        self.redibujar_abbm3()

    # --------- Redibuja el recorrido ABB ---------
    def redibujar_abb(self):
        self.lienzo_abb.delete("all")
        self.lienzo_abb.create_text(240, 20, text="ABB", font=("Arial", 12, "bold"))
        if self.camino_abb:
            camino_resaltado = []
            i = 0
            while i <= self.indice_abb and i < len(self.camino_abb):
                camino_resaltado.append(self.camino_abb[i])
                i += 1
            nodo_actual = camino_resaltado[-1]
        else:
            camino_resaltado = []
            nodo_actual = None
        self.dibujar_arbol_paso(self.lienzo_abb, self.raiz_abb, 240, 50, 0, camino_resaltado, nodo_actual, es_abbm3=False, profundidad=0)
        total = max(1, len(self.camino_abb))
        self.etiqueta_paso_abb.config(text=str(self.indice_abb+1 if self.camino_abb else 0) + " / " + str(total))

    # --------- Redibuja el recorrido ABBm3 ---------
    def redibujar_abbm3(self):
        self.lienzo_abbm3.delete("all")
        self.lienzo_abbm3.create_text(240, 20, text="ABBm3", font=("Arial", 12, "bold"))
        if self.camino_abbm3:
            camino_resaltado = []
            i = 0
            while i <= self.indice_abbm3 and i < len(self.camino_abbm3):
                camino_resaltado.append(self.camino_abbm3[i])
                i += 1
            nodo_actual = camino_resaltado[-1]
        else:
            camino_resaltado = []
            nodo_actual = None
        self.dibujar_arbol_paso(self.lienzo_abbm3, self.raiz_abbm3, 240, 50, 0, camino_resaltado, nodo_actual, es_abbm3=True, profundidad=0)
        total = max(1, len(self.camino_abbm3))
        self.etiqueta_paso_abbm3.config(text=str(self.indice_abbm3+1 if self.camino_abbm3 else 0) + " / " + str(total))

    # --------- Navegación pasos ABB ---------
    def prev_abb(self):
        if self.indice_abb > 0:
            self.indice_abb -= 1
            self.redibujar_abb()

    def next_abb(self):
        if self.camino_abb and self.indice_abb < len(self.camino_abb) - 1:
            self.indice_abb += 1
            self.redibujar_abb()

    # --------- Navegación pasos ABBm3 ---------
    def prev_abbm3(self):
        if self.indice_abbm3 > 0:
            self.indice_abbm3 -= 1
            self.redibujar_abbm3()

    def next_abbm3(self):
        if self.camino_abbm3 and self.indice_abbm3 < len(self.camino_abbm3) - 1:
            self.indice_abbm3 += 1
            self.redibujar_abbm3()

    # --------- Dibuja el árbol resaltando el camino y nodo actual ---------
    def dibujar_arbol_paso(self, lienzo, nodo, x, y, dx, camino_resaltado, nodo_actual, es_abbm3=False, profundidad=0):
        if not nodo:
            return

        nodo_en_camino = False
        i = 0
        while i < len(camino_resaltado):
            if nodo == camino_resaltado[i]:
                nodo_en_camino = True
                break
            i += 1

        if nodo == nodo_actual:
            relleno_rect = "#fa6400"
        elif nodo_en_camino:
            relleno_rect = "#ffe599"
        else:
            relleno_rect = color_nodo(nodo, self.master.abb if not es_abbm3 else self.master.abbm3, es_abbm3)

        if es_abbm3:
            if nodo.hoja:
                etiqueta = "{"
                i = 0
                for valor in nodo.llaves:
                    etiqueta += str(valor)
                    if i < len(nodo.llaves) - 1:
                        etiqueta += ","
                    i += 1
                etiqueta += "}"
                ancho_rect = 12 + 8 * len(nodo.llaves)
                if ancho_rect < 20:
                    ancho_rect = 20
            else:
                etiqueta = "[" + str(nodo.separador) + "]"
                ancho_rect = 28
        else:
            etiqueta = str(nodo.valor)
            ancho_rect = 24

        lienzo.create_rectangle(x - ancho_rect, y - 15, x + ancho_rect, y + 15, fill=relleno_rect, outline="black")
        lienzo.create_text(x, y, text=etiqueta, font=("Arial", 10, "bold"))

        def calcular_dx(d):
            dx_min = 25
            dx_max = 180
            factor = 1
            i = 0
            while i < d:
                factor = factor * 2
                i += 1
            dx = dx_max // factor
            if dx < dx_min:
                dx = dx_min
            return dx

        dx_siguiente = calcular_dx(profundidad+1)

        # Dibuja ramas del árbol según tipo
        if es_abbm3:
            if not nodo.hoja:
                if nodo.izq:
                    lienzo.create_line(x, y + 15, x - dx_siguiente, y + 60 - 15)
                    self.dibujar_arbol_paso(lienzo, nodo.izq, x - dx_siguiente, y + 60, dx_siguiente, camino_resaltado, nodo_actual, es_abbm3, profundidad+1)
                if nodo.der:
                    lienzo.create_line(x, y + 15, x + dx_siguiente, y + 60 - 15)
                    self.dibujar_arbol_paso(lienzo, nodo.der, x + dx_siguiente, y + 60, dx_siguiente, camino_resaltado, nodo_actual, es_abbm3, profundidad+1)
        else:
            if nodo.izq:
                lienzo.create_line(x, y + 15, x - dx_siguiente, y + 60 - 15)
                self.dibujar_arbol_paso(lienzo, nodo.izq, x - dx_siguiente, y + 60, dx_siguiente, camino_resaltado, nodo_actual, es_abbm3, profundidad+1)
            if nodo.der:
                lienzo.create_line(x, y + 15, x + dx_siguiente, y + 60 - 15)
                self.dibujar_arbol_paso(lienzo, nodo.der, x + dx_siguiente, y + 60, dx_siguiente, camino_resaltado, nodo_actual, es_abbm3, profundidad+1)