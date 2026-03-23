# Probability.py (Paso 1: layout principal con grid)
import tkinter as tk
import math
<<<<<<< HEAD
from tkinter import ttk, messagebox
=======
from tkinter import ttk, messagebox, filedialog
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)

class Probability:
    def __init__(self, root, x=0, y=0, width=600, height=400, parent_frame=None):
        self.is_embedded = parent_frame is not None

        if self.is_embedded:
            # === Modo embebido dentro de un frame ===
<<<<<<< HEAD
            self.sub_window = tk.Frame(parent_frame, bg="skyblue1")
=======
            self.sub_window = tk.Frame(parent_frame, bg="black")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
            self.sub_window.grid(row=0, column=0, sticky="nsew")  # usar grid

            # permitir expansión en el contenedor padre
            parent_frame.rowconfigure(0, weight=1)
            parent_frame.columnconfigure(0, weight=1)
        else:
            # === Modo ventana independiente ===
            self.sub_window = tk.Toplevel(root)
            self.sub_window.title("Probabilidades")
            self.sub_window.geometry(f"{width}x{height}+{x}+{y}")
<<<<<<< HEAD
            self.sub_window.configure(bg="skyblue1")

        # === Toolbar arriba, principle_frame ocupa el resto ===
        self.toolbar = None  # solo se crea en running()
        self.principle_frame = tk.Frame(self.sub_window, bg="skyblue1")
=======
            self.sub_window.configure(bg="black")

        # === Toolbar arriba, principle_frame ocupa el resto ===
        self.toolbar = None  # solo se crea en running()
        self.principle_frame = tk.Frame(self.sub_window, bg="black")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)

        if self.is_embedded:
            self.principle_frame.grid(row=1, column=0, sticky="nsew")
            self.sub_window.rowconfigure(1, weight=1)
            self.sub_window.columnconfigure(0, weight=1)
        else:
            self.principle_frame.grid(row=0, column=0, sticky="nsew")
            self.sub_window.rowconfigure(0, weight=1)
            self.sub_window.columnconfigure(0, weight=1)

    def _set_grid(self, widget, rows=1, cols=1):
        """Helper: configura row/column weights para permitir expansión."""
        for r in range(rows):
            try:
                widget.rowconfigure(r, weight=1)
            except Exception:
                pass
        for c in range(cols):
            try:
                widget.columnconfigure(c, weight=1)
            except Exception:
                pass

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def simple_success(self, root):
        self.clear_frame(root)

<<<<<<< HEAD
        lf = tk.LabelFrame(root, text="Sucesos Simples", bg="skyblue1", font=("Arial", 12, "bold"))
=======
        lf = tk.LabelFrame(root, text="Sucesos Simples", bg="black", fg="white", font=("Arial", 12, "bold"))
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        lf.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # permitir expansión
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        lf.rowconfigure(1, weight=1)  # tabla
        lf.columnconfigure(0, weight=1)

        muestras = {}  # Diccionario para guardar {"nombre": cantidad}

        # Entradas para nueva muestra
<<<<<<< HEAD
        entrada_frame = tk.Frame(lf, bg="skyblue1")
=======
        entrada_frame = tk.Frame(lf, bg="black")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        entrada_frame.grid(row=0, column=0, sticky="ew", pady=5)
        entrada_frame.columnconfigure(1, weight=1)
        entrada_frame.columnconfigure(3, weight=1)

<<<<<<< HEAD
        tk.Label(entrada_frame, text="Nombre de la muestra:", bg="skyblue1").grid(row=0, column=0, sticky="w", padx=2)
        nombre_entry = tk.Entry(entrada_frame)
        nombre_entry.grid(row=0, column=1, padx=5, sticky="ew")

        tk.Label(entrada_frame, text="Cantidad:", bg="skyblue1").grid(row=0, column=2, sticky="w", padx=2)
        cantidad_entry = tk.Entry(entrada_frame)
        cantidad_entry.grid(row=0, column=3, padx=5, sticky="ew")

        tabla_frame = tk.Frame(lf, bg="skyblue1")
=======
        tk.Label(entrada_frame, text="Nombre de la muestra:", bg="black", fg="white").grid(row=0, column=0, sticky="w", padx=2)
        nombre_entry = tk.Entry(entrada_frame)
        nombre_entry.grid(row=0, column=1, padx=5, sticky="ew")

        tk.Label(entrada_frame, text="Cantidad:", bg="black", fg="white").grid(row=0, column=2, sticky="w", padx=2)
        cantidad_entry = tk.Entry(entrada_frame)
        cantidad_entry.grid(row=0, column=3, padx=5, sticky="ew")

        tabla_frame = tk.Frame(lf, bg="black")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        tabla_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        tabla_frame.columnconfigure(0, weight=1)
        tabla_frame.rowconfigure(0, weight=1)

        def actualizar_tabla():
            for widget in tabla_frame.winfo_children():
                widget.destroy()
            # Cabeceras / valores en columnas horizontales
            for idx, (nombre, cantidad) in enumerate(muestras.items()):
                header = tk.Label(tabla_frame, text=nombre, bg="lightgray", width=12)
                val = tk.Label(tabla_frame, text=str(cantidad), bg="white", width=12)
                header.grid(row=0, column=idx, padx=2, sticky="n")
                val.grid(row=1, column=idx, padx=2, sticky="n")
                tabla_frame.columnconfigure(idx, weight=1)

        def agregar_muestra():
            nombre = nombre_entry.get().strip()
            try:
                cantidad = int(cantidad_entry.get())
                if nombre and cantidad > 0:
                    if nombre in muestras:
                        muestras[nombre] += cantidad
                    else:
                        muestras[nombre] = cantidad
                    nombre_entry.delete(0, tk.END)
                    cantidad_entry.delete(0, tk.END)
                    actualizar_tabla()
            except ValueError:
                pass  # manejo simple

<<<<<<< HEAD
        btns_frame = tk.Frame(lf, bg="skyblue1")
=======
        btns_frame = tk.Frame(lf, bg="black")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        btns_frame.grid(row=2, column=0, sticky="ew", pady=5)
        btns_frame.columnconfigure(0, weight=1)
        btn_agregar = tk.Button(btns_frame, text="Agregar Muestra", command=agregar_muestra)
        btn_agregar.grid(row=0, column=0, padx=5, sticky="w")

<<<<<<< HEAD
        resultado_label = tk.Label(lf, text="", bg="skyblue1", font=("Arial", 12, "bold"))
=======
        resultado_label = tk.Label(lf, text="", bg="black", fg="white", font=("Arial", 12, "bold"))
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        resultado_label.grid(row=3, column=0, sticky="nsew", pady=10)

        def calcular_probabilidad(eventos_seleccionados):
            total = sum(muestras.values())
            seleccionados = sum(muestras[ev] for ev in eventos_seleccionados if ev in muestras)
            prob = seleccionados / total if total > 0 else 0
            resultado_label.config(text=f"P(A) = {prob * 100:.2f}%")

        def seleccionar_eventos():
            if not muestras:
                resultado_label.config(text="Primero ingrese el espacio muestral.")
                return

            win = tk.Toplevel(root)
            win.title("Seleccionar Evento A")
            win.grid_rowconfigure(0, weight=1)
            win.grid_columnconfigure(0, weight=1)

            sel_frame = tk.Frame(win)
            sel_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            seleccionados = {}

            for i, nombre in enumerate(muestras.keys()):
                var = tk.BooleanVar()
                cb = tk.Checkbutton(sel_frame, text=nombre, variable=var)
                cb.grid(row=i, column=0, sticky="w")
                seleccionados[nombre] = var

            def confirmar():
                eventos = [nombre for nombre, var in seleccionados.items() if var.get()]
                calcular_probabilidad(eventos)
                win.destroy()

            tk.Button(sel_frame, text="Calcular P(A)", command=confirmar).grid(row=len(muestras)+1, column=0, pady=10)

        tk.Button(lf, text="Seleccionar Evento A y Calcular", command=seleccionar_eventos).grid(row=4, column=0, pady=5, sticky="ew")

    def exclusive_success(self, root):
        self.clear_frame(root)

        espacio_muestral = []

<<<<<<< HEAD
        lf = tk.LabelFrame(root, text="Sucesos Excluyentes", bg="skyblue1", font=("Arial", 12, "bold"))
=======
        lf = tk.LabelFrame(root, text="Sucesos Excluyentes", bg="black", fg="white", font=("Arial", 12, "bold"))
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        lf.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        lf.rowconfigure(0, weight=1)
        lf.rowconfigure(1, weight=0)
        lf.columnconfigure(0, weight=1)

        tabla = ttk.Treeview(lf, columns=("Muestra", "Cantidad"), show="headings")
        tabla.heading("Muestra", text="Muestra")
        tabla.heading("Cantidad", text="Cantidad")
        tabla.grid(row=0, column=0, sticky="nsew", pady=10)

        def actualizar_tabla():
            for row in tabla.get_children():
                tabla.delete(row)
            for muestra, cantidad in espacio_muestral:
                for _ in range(cantidad):
                    tabla.insert("", "end", values=(muestra, 1))

        def agregar_muestra():
            win = tk.Toplevel(root)
            win.title("Agregar Muestra")
            win.geometry("300x150")
            win.grid_columnconfigure(1, weight=1)

            tk.Label(win, text="Nombre de la muestra:").grid(row=0, column=0, pady=5, sticky="w")
            nombre_entry = tk.Entry(win)
            nombre_entry.grid(row=0, column=1, pady=5, sticky="ew")

            tk.Label(win, text="Cantidad de repeticiones:").grid(row=1, column=0, pady=5, sticky="w")
            cantidad_entry = tk.Entry(win)
            cantidad_entry.grid(row=1, column=1, pady=5, sticky="ew")

            def confirmar():
                try:
                    nombre = nombre_entry.get().strip()
                    cantidad = int(cantidad_entry.get())
                    if not nombre or cantidad <= 0:
                        raise ValueError
                    espacio_muestral.append((nombre, cantidad))
                    actualizar_tabla()
                    win.destroy()
                except:
                    messagebox.showerror("Error", "Entrada inválida. Intente de nuevo.")

            tk.Button(win, text="Agregar", command=confirmar).grid(row=2, column=0, columnspan=2, pady=10)

        def calcular_evento():
            if not espacio_muestral:
                messagebox.showwarning("Advertencia", "Agrega al menos una muestra.")
                return

            universo = []
            for muestra, cantidad in espacio_muestral:
                universo.extend([muestra] * cantidad)

            win = tk.Toplevel(root)
            win.title("Seleccionar Eventos A y B")
            win.geometry("400x400")
            win.grid_columnconfigure(0, weight=1)

            event_frame = tk.Frame(win)
            event_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            event_frame.columnconfigure(0, weight=1)
            event_frame.columnconfigure(1, weight=1)

            evento_a_vars = {}
            evento_b_vars = {}

            tk.Label(event_frame, text="Selecciona los elementos para Evento A:").grid(row=0, column=0, sticky="w")
            tk.Label(event_frame, text="Selecciona los elementos para Evento B:").grid(row=0, column=1, sticky="w")

            muestras_unicas = sorted(set(universo))
            for i, muestra in enumerate(muestras_unicas, start=1):
                varA = tk.BooleanVar()
                varB = tk.BooleanVar()
                evento_a_vars[muestra] = varA
                evento_b_vars[muestra] = varB
                tk.Checkbutton(event_frame, text=muestra, variable=varA).grid(row=i, column=0, sticky="w")
                tk.Checkbutton(event_frame, text=muestra, variable=varB).grid(row=i, column=1, sticky="w")

            resultado_label = tk.Label(win, text="", font=("Arial", 11, "bold"))
            resultado_label.grid(row=1, column=0, pady=10, sticky="ew")

            def calcular():
                eventoA = set()
                eventoB = set()

                for muestra in universo:
                    if evento_a_vars.get(muestra, tk.BooleanVar()).get():
                        eventoA.add(muestra)
                    if evento_b_vars.get(muestra, tk.BooleanVar()).get():
                        eventoB.add(muestra)

                if eventoA.isdisjoint(eventoB):
                    resultado = (len(eventoA) + len(eventoB)) / len(universo)
                    resultado_label.config(text=f"P(A ∪ B) = {resultado*100:.2f}%")
                else:
                    resultado_label.config(text="Los eventos NO son excluyentes.")

            tk.Button(win, text="Calcular", command=calcular).grid(row=2, column=0, pady=5)

<<<<<<< HEAD
        btns = tk.Frame(lf, bg="skyblue1")
=======
        btns = tk.Frame(lf, bg="black")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        btns.grid(row=1, column=0, pady=5, sticky="ew")
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)

        tk.Button(btns, text="Agregar Muestra", command=agregar_muestra).grid(row=0, column=0, padx=10, sticky="w")
        tk.Button(btns, text="Seleccionar Eventos y Calcular", command=calcular_evento).grid(row=0, column=1, padx=10, sticky="e")

    def dependant_success(self, root):
        self.clear_frame(root)

        espacio_muestral = []

<<<<<<< HEAD
        lf = tk.LabelFrame(root, text="Teorema de Bayes", bg="skyblue1", font=("Arial", 12, "bold"))
=======
        lf = tk.LabelFrame(root, text="Teorema de Bayes", bg="black", fg="white", font=("Arial", 12, "bold"))
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        lf.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        lf.rowconfigure(0, weight=1)
        lf.rowconfigure(1, weight=0)
        lf.columnconfigure(0, weight=1)

        tabla = ttk.Treeview(lf, columns=("Muestra", "Cantidad"), show="headings")
        tabla.heading("Muestra", text="Muestra")
        tabla.heading("Cantidad", text="Cantidad")
        tabla.grid(row=0, column=0, sticky="nsew", pady=10)

        def actualizar_tabla():
            for row in tabla.get_children():
                tabla.delete(row)
            for muestra, cantidad in espacio_muestral:
                for _ in range(cantidad):
                    tabla.insert("", "end", values=(muestra, 1))

        def agregar_muestra():
            win = tk.Toplevel(root)
            win.title("Agregar Muestra")
            win.geometry("300x150")
            win.grid_columnconfigure(1, weight=1)

            tk.Label(win, text="Nombre de la muestra:").grid(row=0, column=0, pady=5, sticky="w")
            nombre_entry = tk.Entry(win)
            nombre_entry.grid(row=0, column=1, pady=5, sticky="ew")

            tk.Label(win, text="Cantidad de repeticiones:").grid(row=1, column=0, pady=5, sticky="w")
            cantidad_entry = tk.Entry(win)
            cantidad_entry.grid(row=1, column=1, pady=5, sticky="ew")

            def confirmar():
                try:
                    nombre = nombre_entry.get().strip()
                    cantidad = int(cantidad_entry.get())
                    if not nombre or cantidad <= 0:
                        raise ValueError
                    espacio_muestral.append((nombre, cantidad))
                    actualizar_tabla()
                    win.destroy()
                except:
                    messagebox.showerror("Error", "Entrada inválida. Intente de nuevo.")

            tk.Button(win, text="Agregar", command=confirmar).grid(row=2, column=0, columnspan=2, pady=10)

        def calcular_bayes():
            if not espacio_muestral:
                messagebox.showwarning("Advertencia", "Agrega al menos una muestra.")
                return

            universo = []
            for muestra, cantidad in espacio_muestral:
                universo.extend([muestra] * cantidad)

            muestras_unicas = sorted(set(universo))

            win = tk.Toplevel(root)
            win.title("Seleccionar Eventos A y B")
            win.geometry("400x450")
            win.grid_columnconfigure(0, weight=1)
            frame = tk.Frame(win)
            frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)

            evento_a_vars = {}
            evento_b_vars = {}

            tk.Label(frame, text="Selecciona los elementos para Evento A:").grid(row=0, column=0, sticky="w")
            tk.Label(frame, text="Selecciona los elementos para Evento B:").grid(row=0, column=1, sticky="w")

            for i, muestra in enumerate(muestras_unicas, start=1):
                varA = tk.BooleanVar()
                varB = tk.BooleanVar()
                evento_a_vars[muestra] = varA
                evento_b_vars[muestra] = varB
                tk.Checkbutton(frame, text=muestra, variable=varA).grid(row=i, column=0, sticky="w")
                tk.Checkbutton(frame, text=muestra, variable=varB).grid(row=i, column=1, sticky="w")

            resultado_label = tk.Label(win, text="", font=("Arial", 11, "bold"))
            resultado_label.grid(row=1, column=0, pady=10, sticky="ew")

            def calcular():
                eventoA = set([m for m, v in evento_a_vars.items() if v.get()])
                eventoB = set([m for m, v in evento_b_vars.items() if v.get()])

                if not eventoA or not eventoB:
                    resultado_label.config(text="Selecciona al menos un valor para A y B.")
                    return

                total = len(universo)
                conteo_A = sum(1 for x in universo if x in eventoA)
                conteo_B = sum(1 for x in universo if x in eventoB)
                conteo_AyB = sum(1 for x in universo if x in eventoA and x in eventoB)

                try:
                    P_A = conteo_A / total
                    P_B = conteo_B / total
                    P_B_given_A = conteo_AyB / conteo_A if conteo_A else 0

                    if P_B == 0:
                        raise ZeroDivisionError

                    P_A_given_B = (P_B_given_A * P_A) / P_B
                    resultado_label.config(text=f"P(A | B) = {P_A_given_B:.4f} ({P_A_given_B*100:.2f}%)")
                except ZeroDivisionError:
                    resultado_label.config(text="No se puede dividir entre 0.")

            tk.Button(win, text="Calcular", command=calcular).grid(row=2, column=0, pady=5)

<<<<<<< HEAD
        btns = tk.Frame(lf, bg="skyblue1")
=======
        btns = tk.Frame(lf, bg="black")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        btns.grid(row=1, column=0, pady=5, sticky="ew")
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)

        tk.Button(btns, text="Agregar Muestra", command=agregar_muestra).grid(row=0, column=0, padx=10, sticky="w")
        tk.Button(btns, text="Seleccionar Eventos y Calcular", command=calcular_bayes).grid(row=0, column=1, padx=10, sticky="e")

    def independent_success(self, root):
        self.clear_frame(root)

        espacio_muestral = []

<<<<<<< HEAD
        lf = tk.LabelFrame(root, text="Sucesos Independientes", bg="skyblue1", font=("Arial", 12, "bold"))
=======
        lf = tk.LabelFrame(root, text="Sucesos Independientes", bg="black", fg="white", font=("Arial", 12, "bold"))
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        lf.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        lf.rowconfigure(0, weight=1)
        lf.rowconfigure(1, weight=0)
        lf.columnconfigure(0, weight=1)

        tabla = ttk.Treeview(lf, columns=("Muestra", "Cantidad"), show="headings")
        tabla.heading("Muestra", text="Muestra")
        tabla.heading("Cantidad", text="Cantidad")
        tabla.grid(row=0, column=0, sticky="nsew", pady=10)

        def actualizar_tabla():
            for row in tabla.get_children():
                tabla.delete(row)
            for muestra, cantidad in espacio_muestral:
                for _ in range(cantidad):
                    tabla.insert("", "end", values=(muestra, 1))

        def agregar_muestra():
            win = tk.Toplevel(root)
            win.title("Agregar Muestra")
            win.geometry("300x150")
            win.grid_columnconfigure(1, weight=1)

            tk.Label(win, text="Nombre de la muestra:").grid(row=0, column=0, pady=5, sticky="w")
            nombre_entry = tk.Entry(win)
            nombre_entry.grid(row=0, column=1, pady=5, sticky="ew")

            tk.Label(win, text="Cantidad de repeticiones:").grid(row=1, column=0, pady=5, sticky="w")
            cantidad_entry = tk.Entry(win)
            cantidad_entry.grid(row=1, column=1, pady=5, sticky="ew")

            def confirmar():
                try:
                    nombre = nombre_entry.get().strip()
                    cantidad = int(cantidad_entry.get())
                    if not nombre or cantidad <= 0:
                        raise ValueError
                    espacio_muestral.append((nombre, cantidad))
                    actualizar_tabla()
                    win.destroy()
                except:
                    messagebox.showerror("Error", "Entrada inválida. Intente de nuevo.")

            tk.Button(win, text="Agregar", command=confirmar).grid(row=2, column=0, columnspan=2, pady=10)

        def calcular_independientes():
            if not espacio_muestral:
                messagebox.showwarning("Advertencia", "Agrega al menos una muestra.")
                return

            universo = []
            for muestra, cantidad in espacio_muestral:
                universo.extend([muestra] * cantidad)

            muestras_unicas = sorted(set(universo))

            win = tk.Toplevel(root)
            win.title("Seleccionar Eventos A y B")
            win.geometry("400x450")
            win.grid_columnconfigure(0, weight=1)
            frame = tk.Frame(win)
            frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)

            evento_a_vars = {}
            evento_b_vars = {}

            tk.Label(frame, text="Selecciona los elementos para Evento A:").grid(row=0, column=0, sticky="w")
            tk.Label(frame, text="Selecciona los elementos para Evento B:").grid(row=0, column=1, sticky="w")

            for i, muestra in enumerate(muestras_unicas, start=1):
                varA = tk.BooleanVar()
                varB = tk.BooleanVar()
                evento_a_vars[muestra] = varA
                evento_b_vars[muestra] = varB
                tk.Checkbutton(frame, text=muestra, variable=varA).grid(row=i, column=0, sticky="w")
                tk.Checkbutton(frame, text=muestra, variable=varB).grid(row=i, column=1, sticky="w")

            resultado_label = tk.Label(win, text="", font=("Arial", 11, "bold"))
            resultado_label.grid(row=1, column=0, pady=10, sticky="ew")

            def calcular():
                eventoA = set([m for m, v in evento_a_vars.items() if v.get()])
                eventoB = set([m for m, v in evento_b_vars.items() if v.get()])

                if not eventoA or not eventoB:
                    resultado_label.config(text="Selecciona al menos un valor para A y B.")
                    return

                total = len(universo)
                prob_A = sum(1 for x in universo if x in eventoA) / total
                prob_B = sum(1 for x in universo if x in eventoB) / total
                prob_indep = prob_A * prob_B

                resultado_label.config(
                    text=f"P(A) = {prob_A:.4f}, P(B) = {prob_B:.4f}\nP(A ∩ B) = {prob_indep:.4f} ({prob_indep*100:.2f}%)"
                )

            tk.Button(win, text="Calcular", command=calcular).grid(row=2, column=0, pady=5)

<<<<<<< HEAD
        btns = tk.Frame(lf, bg="skyblue1")
=======
        btns = tk.Frame(lf, bg="black")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        btns.grid(row=1, column=0, pady=5, sticky="ew")
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)

        tk.Button(btns, text="Agregar Muestra", command=agregar_muestra).grid(row=0, column=0, padx=10, sticky="w")
        tk.Button(btns, text="Seleccionar Eventos y Calcular", command=calcular_independientes).grid(row=0, column=1, padx=10, sticky="e")

    def non_exclusive_success(self, root):
        self.clear_frame(root)

        espacio_muestral = []

<<<<<<< HEAD
        lf = tk.LabelFrame(root, text="Sucesos No Excluyentes", bg="skyblue1", font=("Arial", 12, "bold"))
=======
        lf = tk.LabelFrame(root, text="Sucesos No Excluyentes", bg="black", fg="white", font=("Arial", 12, "bold"))
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        lf.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        lf.rowconfigure(0, weight=1)
        lf.rowconfigure(1, weight=0)
        lf.columnconfigure(0, weight=1)

        tabla = ttk.Treeview(lf, columns=("Muestra", "Cantidad"), show="headings")
        tabla.heading("Muestra", text="Muestra")
        tabla.heading("Cantidad", text="Cantidad")
        tabla.grid(row=0, column=0, sticky="nsew", pady=10)

        def actualizar_tabla():
            for row in tabla.get_children():
                tabla.delete(row)
            for muestra, cantidad in espacio_muestral:
                for _ in range(cantidad):
                    tabla.insert("", "end", values=(muestra, 1))

        def agregar_muestra():
            win = tk.Toplevel(root)
            win.title("Agregar Muestra")
            win.geometry("300x150")
            win.grid_columnconfigure(1, weight=1)

            tk.Label(win, text="Nombre de la muestra:").grid(row=0, column=0, pady=5, sticky="w")
            nombre_entry = tk.Entry(win)
            nombre_entry.grid(row=0, column=1, pady=5, sticky="ew")

            tk.Label(win, text="Cantidad de repeticiones:").grid(row=1, column=0, pady=5, sticky="w")
            cantidad_entry = tk.Entry(win)
            cantidad_entry.grid(row=1, column=1, pady=5, sticky="ew")

            def confirmar():
                try:
                    nombre = nombre_entry.get().strip()
                    cantidad = int(cantidad_entry.get())
                    if not nombre or cantidad <= 0:
                        raise ValueError
                    espacio_muestral.append((nombre, cantidad))
                    actualizar_tabla()
                    win.destroy()
                except:
                    messagebox.showerror("Error", "Entrada inválida. Intente de nuevo.")

            tk.Button(win, text="Agregar", command=confirmar).grid(row=2, column=0, columnspan=2, pady=10)

        def calcular_no_excluyentes():
            if not espacio_muestral:
                messagebox.showwarning("Advertencia", "Agrega al menos una muestra.")
                return

            universo = []
            for muestra, cantidad in espacio_muestral:
                universo.extend([muestra] * cantidad)

            muestras_unicas = sorted(set(universo))

            win = tk.Toplevel(root)
            win.title("Seleccionar Eventos A y B")
            win.geometry("400x450")
            win.grid_columnconfigure(0, weight=1)
            frame = tk.Frame(win)
            frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)

            evento_a_vars = {}
            evento_b_vars = {}

            tk.Label(frame, text="Selecciona los elementos para Evento A:").grid(row=0, column=0, sticky="w")
            tk.Label(frame, text="Selecciona los elementos para Evento B:").grid(row=0, column=1, sticky="w")

            for i, muestra in enumerate(muestras_unicas, start=1):
                varA = tk.BooleanVar()
                varB = tk.BooleanVar()
                evento_a_vars[muestra] = varA
                evento_b_vars[muestra] = varB
                tk.Checkbutton(frame, text=muestra, variable=varA).grid(row=i, column=0, sticky="w")
                tk.Checkbutton(frame, text=muestra, variable=varB).grid(row=i, column=1, sticky="w")

            resultado_label = tk.Label(win, text="", font=("Arial", 11, "bold"))
            resultado_label.grid(row=1, column=0, pady=10, sticky="ew")

            def calcular():
                eventoA = set([m for m, v in evento_a_vars.items() if v.get()])
                eventoB = set([m for m, v in evento_b_vars.items() if v.get()])

                if not eventoA or not eventoB:
                    resultado_label.config(text="Selecciona al menos un valor para A y B.")
                    return

                total = len(universo)
                prob_A = sum(1 for x in universo if x in eventoA) / total
                prob_B = sum(1 for x in universo if x in eventoB) / total
                prob_A_inter_B = sum(1 for x in universo if x in eventoA and x in eventoB) / total

                prob_union = prob_A + prob_B - prob_A_inter_B

                resultado_label.config(
                    text=(
                        f"P(A) = {prob_A:.4f}, P(B) = {prob_B:.4f}, P(A ∩ B) = {prob_A_inter_B:.4f}\n"
                        f"P(A ∪ B) = {prob_union:.4f} ({prob_union*100:.2f}%)"
                    )
                )

            tk.Button(win, text="Calcular", command=calcular).grid(row=2, column=0, pady=5)

<<<<<<< HEAD
        btns = tk.Frame(lf, bg="skyblue1")
=======
        btns = tk.Frame(lf, bg="black")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        btns.grid(row=1, column=0, pady=5, sticky="ew")
        btns.columnconfigure(0, weight=1)
        btns.columnconfigure(1, weight=1)

        tk.Button(btns, text="Agregar Muestra", command=agregar_muestra).grid(row=0, column=0, padx=10, sticky="w")
        tk.Button(btns, text="Seleccionar Eventos y Calcular", command=calcular_no_excluyentes).grid(row=0, column=1, padx=10, sticky="e")

    def tree_diagram_self_window(self, root):
        self.clear_frame(root)

<<<<<<< HEAD
        lf = tk.Frame(root, bg="skyblue1")
=======
        lf = tk.Frame(root, bg="black")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        lf.grid(row=0, column=0, sticky="nsew")
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        lf.rowconfigure(0, weight=1)
        lf.columnconfigure(0, weight=1)
        lf.columnconfigure(1, weight=0)

        nodos = {}
        nodo_id_counter = [0]
        seleccionado = {"id": None}
        current_scale = [1.0]  # escala global del canvas
        min_scale, max_scale = 0.5, 3.0

# === Canvas con scrollbars ===
        canvas_frame = tk.Frame(lf)
        canvas_frame.grid(row=0, column=0, sticky="nsew")
        canvas_frame.grid_propagate(False)  # evita que el frame cambie de tamaño automáticamente
        canvas_frame.config(width=600, height=400)  # tamaño inicial fijo

        x_scroll = tk.Scrollbar(canvas_frame, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")
        y_scroll = tk.Scrollbar(canvas_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        canvas = tk.Canvas(canvas_frame, bg="white",
                           xscrollcommand=x_scroll.set,
                           yscrollcommand=y_scroll.set)
        canvas.pack(side="left", fill="both", expand=True)

        x_scroll.config(command=canvas.xview)
        y_scroll.config(command=canvas.yview)

# ==== Controles a la derecha ====
<<<<<<< HEAD
        controls = tk.Frame(lf, bg="skyblue1")
        controls.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

# botones de control
        controls_buttons = tk.Frame(controls, bg="skyblue1")
=======
        controls = tk.Frame(lf, bg="black")
        controls.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

# botones de control
        controls_buttons = tk.Frame(controls, bg="black")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        controls_buttons.pack(side="top", fill="x", pady=(0, 8))

# label de aviso con tamaño fijo y cambio de color según estado
        aviso_label = tk.Label(
            controls,
            text="",                     # texto inicial vacío
<<<<<<< HEAD
            bg="skyblue1",
=======
            bg="black", fg="white",
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
            font=("Arial", 10, "bold"),
            width=25,                    # ancho fijo en caracteres
            height=2,                    # alto fijo en líneas
            anchor="center",
            justify="center",
            wraplength=180               # dividir texto largo en varias líneas
        )
        aviso_label.pack(side="top", pady=(8, 0), fill="x")

# función helper para actualizar aviso sin cambiar tamaño
        def actualizar_aviso(texto, color="black"):
            aviso_label.config(text=texto, fg=color)

        # ==== Crear nodos ====
        def crear_nodo(padre=None, evento="Evento", prob=1.0):
            nodo_id_counter[0] += 1
            nid = nodo_id_counter[0]
            nodos[nid] = {"evento": evento, "prob": prob, "padre": padre, "hijos": [], "tags": f"nodo_{nid}"}
            if padre:
                nodos[padre]["hijos"].append(nid)
            dibujar_arbol()
            return nid

        # ==== Calcular tamaño de subárbol ====
        def calcular_altura(nid):
            hijos = nodos[nid]["hijos"]
            if not hijos:
                return 1
            return sum(calcular_altura(h) for h in hijos)

        # ==== Dibujar árbol ====
        def dibujar_arbol():
            canvas.delete("all")

            hojas_probs = []  # guardará probabilidades finales de hojas

            def recorrer_prob(nid):
                prob = nodos[nid]["prob"]
                padre = nodos[nid]["padre"]
                while padre is not None:
                    prob *= nodos[padre]["prob"]
                    padre = nodos[padre]["padre"]
                return prob

            def dibujar_recursivo(nid, x, y, altura_total):
                evento = nodos[nid]["evento"]
                prob = nodos[nid]["prob"]

                ancho, alto = 90, 40
                tag = nodos[nid]["tags"]

                rect = canvas.create_rectangle(x, y, x+ancho, y+alto, fill="lightblue", tags=(tag,))
                txt = canvas.create_text(x+ancho/2, y+alto/2, text=f"{evento}\nP={prob}", font=("Arial", 8), tags=(tag,))
                nodos[nid]["obj"] = (rect, txt, x, y, ancho, alto)

                hijos = nodos[nid]["hijos"]
                if hijos:
                    altura_usada = 0
                    for h in hijos:
                        sub_altura = calcular_altura(h) * 60
                        hijo_y = y - altura_total/2 + altura_usada + sub_altura/2
                        hijo_x = x + 150
                        canvas.create_line(x+ancho, y+alto/2, hijo_x, hijo_y+alto/2, arrow="last")
                        dibujar_recursivo(h, hijo_x, hijo_y, sub_altura)
                        altura_usada += sub_altura
                else:
                    prob_acum = recorrer_prob(nid)
                    hojas_probs.append(prob_acum)
                    canvas.create_text(x+ancho+50, y+alto/2, text=f"Final={prob_acum:.4f}",
                                       font=("Arial", 8),
                                       fill="blue")

            # dibujar desde cada raíz
            y_inicial = 200
            for nid, data in list(nodos.items()):
                if data["padre"] is None:
                    altura = calcular_altura(nid) * 60
                    dibujar_recursivo(nid, 50, y_inicial, altura)
                    y_inicial += altura + 50

            # actualizar scrollregion
            bbox = canvas.bbox("all")
            if bbox:
                canvas.configure(scrollregion=bbox)

            # verificar suma de probabilidades finales y mostrar aviso en controls (derecha)
            if hojas_probs:
                total = sum(hojas_probs)
                if abs(total - 1) > 0.001:
                    actualizar_aviso(f"⚠️ La suma de finales = {total:.4f} (≠ 1)", "red")
                else:
                    actualizar_aviso(f"La suma de finales = {total:.4f}", "green")
            else:
                actualizar_aviso("", "black")

        # ==== Selección de nodos ====
        def seleccionar(event):
            # Asegurarnos de convertir la posición del clic a coordenadas del canvas
            # y obtener el item bajo el cursor.
            cx = canvas.canvasx(event.x)
            cy = canvas.canvasy(event.y)
            items = canvas.find_overlapping(cx, cy, cx, cy)
            nid = None
            for itm in items[::-1]:  # priorizar el tope
                tags = canvas.gettags(itm)
                for t in tags:
                    if t.startswith("nodo_"):
                        nid = int(t.split("_")[1])
                        break
                if nid is not None:
                    break

            if nid is None:
                return

            seleccionado["id"] = nid
            # resetear colores (solo rectángulos)
            for nid2, data in nodos.items():
                if "obj" in data:
                    try:
                        canvas.itemconfig(data["obj"][0], fill="lightblue")
                    except Exception:
                        pass
            try:
                canvas.itemconfig(nodos[nid]["obj"][0], fill="orange")
            except Exception:
                pass

        # focus al entrar para asegurar que wheel/gestures lleguen al canvas
        canvas.bind("<Enter>", lambda e: canvas.focus_set())
        canvas.bind("<Button-1>", seleccionar)

        # ==== Manejador unificado para mousewheel / trackpad / Button-4/5 ====
        import math as _math

        def on_mouse_wheel(event):
            """
            - Ctrl + wheel -> zoom (limitado)
            - Shift + wheel -> scroll horizontal
            - wheel -> scroll vertical
            Soporta event.delta (Windows/Mac/trackpad) y Button-4/5 (Linux)
            """
            # obtener delta robustamente
            if hasattr(event, "delta"):
                delta = event.delta
            else:
                # event.num para Button-4 (up) y Button-5 (down)
                if getattr(event, "num", None) == 4:
                    delta = 120
                elif getattr(event, "num", None) == 5:
                    delta = -120
                else:
                    delta = 0

            # detectar modificadores (intentos compatibles)
            state = getattr(event, "state", 0)
            ctrl = (state & 0x0004) != 0  # ctrl en muchos sistemas
            shift = (state & 0x0001) != 0  # shift en muchos sistemas

            # si Ctrl -> zoom
            if ctrl:
                factor = 1.1 if delta > 0 else 0.9
                new_scale = current_scale[0] * factor
                if min_scale <= new_scale <= max_scale:
                    current_scale[0] = new_scale
                    # usar coordenadas del canvas como punto focal
                    cx = canvas.canvasx(event.x)
                    cy = canvas.canvasy(event.y)
                    canvas.scale("all", cx, cy, factor, factor)
                    bbox = canvas.bbox("all")
                    if bbox:
                        canvas.configure(scrollregion=bbox)
                return "break"

            # desplazamiento (trackpad/rueda)
            # normalizamos a pasos (1 por notch)
            step = int(delta / 120) if delta != 0 else 0
            if step == 0:
                step = 1 if delta > 0 else -1 if delta < 0 else 0

            if shift:
                # horizontal
                canvas.xview_scroll(-step, "units")
            else:
                # vertical
                canvas.yview_scroll(-step, "units")

            return "break"

        # enlaces:
        # - bind sobre canvas para Button-4/5 (Linux)
        canvas.bind("<Button-4>", on_mouse_wheel)
        canvas.bind("<Button-5>", on_mouse_wheel)
        # - para Windows/Mac/trackpad:
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

        # ==== Mostrar ramas (mejorado) ====
        def calcular_ramas():
            resultados = []

            def recorrer(nid, prob_acum, camino, probs):
                prob_actual = prob_acum * nodos[nid]["prob"]
                camino_actual = camino + [nodos[nid]["evento"]]
                probs_actual = probs + [nodos[nid]["prob"]]

                if not nodos[nid]["hijos"]:
                    resultados.append((camino_actual, probs_actual, prob_actual))
                else:
                    for h in nodos[nid]["hijos"]:
                        recorrer(h, prob_actual, camino_actual, probs_actual)

            if seleccionado["id"] is not None:
                # mostrar SOLO el recorrido hasta el nodo seleccionado (desde raíz)
                nid = seleccionado["id"]
                camino = []
                probs = []
                prob_acum = 1.0
                # construir lista desde nodo hasta raíz y luego invertir
                stack = []
                cur = nid
                while cur is not None:
                    stack.append(cur)
                    cur = nodos[cur]["padre"]
                stack.reverse()
                camino = [nodos[i]["evento"] for i in stack]
                probs = [nodos[i]["prob"] for i in stack]
                for p in probs:
                    prob_acum *= p
                resultados.append((camino, probs, prob_acum))
            else:
                # mostrar todas las ramas completas
                for nid, data in list(nodos.items()):
                    if data["padre"] is None:
                        recorrer(nid, 1.0, [], [])

            win = tk.Toplevel(root)
            win.title("Resultados de ramas")
            text = tk.Text(win, width=70, height=20)
            text.pack()

            for camino, probs, prob_final in resultados:
                detalle = " -> ".join([f"{ev}(P={p})" for ev, p in zip(camino, probs)])
                text.insert("end", f"Camino: {detalle}\n")
                text.insert("end", f"Probabilidad acumulada: {prob_final:.4f}\n\n")

        # ==== Botones de control (empaquetados en controls_buttons) ====
        tk.Button(controls_buttons, text="🌳 Crear Raíz", command=lambda: crear_nodo(None, "Raíz", 1.0)).pack(pady=5, fill="x")
        tk.Button(controls_buttons, text="➕ Crear Rama", command=lambda: crear_nodo(seleccionado["id"], "Hijo", 0.5)).pack(pady=5, fill="x")
        tk.Button(controls_buttons, text="✏️ Editar Nodo", command=lambda: editar_nodo_wrapper()).pack(pady=5, fill="x")
        tk.Button(controls_buttons, text="🗑️ Eliminar Nodo", command=lambda: eliminar_nodo_wrapper()).pack(pady=5, fill="x")
        tk.Button(controls_buttons, text="📊 Mostrar Ramas", command=calcular_ramas).pack(pady=5, fill="x")

        # helpers para editar/eliminar (se definen aquí para que existan cuando se asignan a botones)
        def editar_nodo_wrapper():
            if seleccionado["id"] is None:
                return
            nid = seleccionado["id"]
            win = tk.Toplevel(root)
            win.title("Editar Nodo")
            win.grid_columnconfigure(1, weight=1)

            tk.Label(win, text="Evento:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
            evento_entry = tk.Entry(win)
            evento_entry.insert(0, nodos[nid]["evento"])
            evento_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

            tk.Label(win, text="Probabilidad:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
            prob_entry = tk.Entry(win)
            prob_entry.insert(0, str(nodos[nid]["prob"]))
            prob_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

            def guardar():
                try:
                    nodos[nid]["evento"] = evento_entry.get()
                    nodos[nid]["prob"] = float(prob_entry.get())
                    dibujar_arbol()
                    win.destroy()
                except Exception:
                    messagebox.showerror("Error", "Probabilidad inválida.")

            tk.Button(win, text="Guardar", command=guardar).grid(row=2, column=0, columnspan=2, pady=10)

        def eliminar_nodo_wrapper():
            if seleccionado["id"] is None:
                return
            nid = seleccionado["id"]

            def borrar(n):
                for h in list(nodos[n]["hijos"]):
                    borrar(h)
                nodos.pop(n, None)
            borrar(nid)

            for pid, data in list(nodos.items()):
                if nid in data["hijos"]:
                    data["hijos"].remove(nid)
            seleccionado["id"] = None
            dibujar_arbol()

        # dibujar inicialmente (si ya hay nodos)
        dibujar_arbol()

    def bernoulli_self_window(self, root):
        self.clear_frame(root)

<<<<<<< HEAD
        lf = tk.LabelFrame(root, text="Distribución de Bernoulli", bg="skyblue1", font=("Arial", 12, "bold"))
=======
        lf = tk.LabelFrame(root, text="Distribución de Bernoulli", bg="black", fg="white", font=("Arial", 12, "bold"))
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        lf.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        lf.columnconfigure(1, weight=1)

        tk.Label(lf, text="Probabilidad de éxito (p):").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        p_entry = tk.Entry(lf)
        p_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(lf, text="Valor de x (0 o 1):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        x_entry = tk.Entry(lf)
        x_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        resultado_label = tk.Label(lf, text="", font=("Arial", 11, "bold"))
        resultado_label.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        def calcular():
            try:
                p = float(p_entry.get())
                x = int(x_entry.get())
                if not (0 <= p <= 1):
                    raise ValueError("p debe estar entre 0 y 1")
                if x not in [0, 1]:
                    raise ValueError("x debe ser 0 o 1")

                resultado = (p ** x) * ((1 - p) ** (1 - x))
                resultado_label.config(text=f"P(X={x}) = {resultado:.6f}")
            except Exception as e:
                messagebox.showerror("Error", f"Entrada inválida: {e}")

        tk.Button(lf, text="Calcular", command=calcular).grid(row=3, column=0, columnspan=2, pady=5)

    def binomial_self_window(self, root):
        self.clear_frame(root)

<<<<<<< HEAD
        lf = tk.LabelFrame(root, text="Distribución Binomial", bg="skyblue1", font=("Arial", 12, "bold"))
=======
        lf = tk.LabelFrame(root, text="Distribución Binomial", bg="black", fg="white", font=("Arial", 12, "bold"))
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        lf.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        lf.columnconfigure(1, weight=1)

        tk.Label(lf, text="Número de ensayos (n):").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        n_entry = tk.Entry(lf)
        n_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(lf, text="Número de éxitos (k):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        k_entry = tk.Entry(lf)
        k_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(lf, text="Probabilidad de éxito (p):").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        p_entry = tk.Entry(lf)
        p_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

        resultado_label = tk.Label(lf, text="", font=("Arial", 11, "bold"))
        resultado_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        def calcular():
            try:
                n = int(n_entry.get())
                k = int(k_entry.get())
                p = float(p_entry.get())

                if n < 0 or k < 0:
                    raise ValueError("n y k deben ser no negativos")
                if k > n:
                    raise ValueError("k no puede ser mayor que n")
                if not (0 <= p <= 1):
                    raise ValueError("p debe estar entre 0 y 1")

                comb = math.comb(n, k)
                resultado = comb * (p ** k) * ((1 - p) ** (n - k))
                resultado_label.config(text=f"P(X={k}) = {resultado:.6f}")
            except Exception as e:
                messagebox.showerror("Error", f"Entrada inválida: {e}")

        tk.Button(lf, text="Calcular", command=calcular).grid(row=4, column=0, columnspan=2, pady=5)

    def poisson_self_window(self, root):
        self.clear_frame(root)

<<<<<<< HEAD
        lf = tk.LabelFrame(root, text="Distribución de Poisson", bg="skyblue1", font=("Arial", 12, "bold"))
=======
        lf = tk.LabelFrame(root, text="Distribución de Poisson", bg="black", fg="white", font=("Arial", 12, "bold"))
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        lf.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        lf.columnconfigure(1, weight=1)

        tk.Label(lf, text="Tasa promedio (λ):").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        lambda_entry = tk.Entry(lf)
        lambda_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(lf, text="Número de eventos (k):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        k_entry = tk.Entry(lf)
        k_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        resultado_label = tk.Label(lf, text="", font=("Arial", 11, "bold"))
        resultado_label.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        def calcular():
            try:
                lmbda = float(lambda_entry.get())
                k = int(k_entry.get())

                if lmbda < 0:
                    raise ValueError("λ debe ser no negativo")
                if k < 0:
                    raise ValueError("k debe ser no negativo")

                resultado = (lmbda ** k) * math.exp(-lmbda) / math.factorial(k)
                resultado_label.config(text=f"P(X={k}) = {resultado:.6f}")
            except Exception as e:
                messagebox.showerror("Error", f"Entrada inválida: {e}")

        tk.Button(lf, text="Calcular", command=calcular).grid(row=3, column=0, columnspan=2, pady=5)

<<<<<<< HEAD
    def running(self):
        if self.is_embedded:
            # === Toolbar pegada arriba ===
            self.toolbar = tk.Frame(self.sub_window, bg="skyblue1")
=======
    def normal_self_window(self, root):
        self.clear_frame(root)

        lf = tk.LabelFrame(root, text="Distribución Normal", bg="black", fg="white", font=("Arial", 12, "bold"))
        lf.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        lf.columnconfigure(1, weight=1)

        # Parámetros de la distribución
        tk.Label(lf, text="Media (μ):").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        mu_entry = tk.Entry(lf)
        mu_entry.insert(0, "0")
        mu_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(lf, text="Desviación estándar (σ):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        sigma_entry = tk.Entry(lf)
        sigma_entry.insert(0, "1")
        sigma_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        # Tipo de cálculo
        tk.Label(lf, text="Tipo de cálculo:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        tipo_var = tk.StringVar(value="menor")
        frame_tipo = tk.Frame(lf, bg="black")
        frame_tipo.grid(row=2, column=1, sticky="w", pady=5, padx=5)
        tk.Radiobutton(frame_tipo, text="P(X < x)", variable=tipo_var, value="menor", bg="black").pack(side="left", padx=5)
        tk.Radiobutton(frame_tipo, text="P(X > x)", variable=tipo_var, value="mayor", bg="black").pack(side="left", padx=5)
        tk.Radiobutton(frame_tipo, text="P(a < X < b)", variable=tipo_var, value="entre", bg="black").pack(side="left", padx=5)

        # Valores
        tk.Label(lf, text="Valor x (o valor a):").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        x_entry = tk.Entry(lf)
        x_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(lf, text="Valor b (solo para 'entre'):").grid(row=4, column=0, sticky="w", pady=5, padx=5)
        b_entry = tk.Entry(lf)
        b_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=5)

        # Frame para resultados
        resultado_frame = tk.Frame(lf, bg="white", relief="sunken", borderwidth=2)
        resultado_frame.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        lf.rowconfigure(6, weight=1)

        resultado_text = tk.Text(resultado_frame, height=8, wrap="word", font=("Courier", 10))
        resultado_text.pack(fill="both", expand=True)

        def calcular():
            try:
                mu = float(mu_entry.get())
                sigma = float(sigma_entry.get())

                if sigma <= 0:
                    raise ValueError("σ debe ser mayor que 0")

                tipo = tipo_var.get()
                x = float(x_entry.get())

                resultado_text.delete(1.0, tk.END)
                resultado_text.insert(tk.END, "=" * 50 + "\n")
                resultado_text.insert(tk.END, "  DISTRIBUCIÓN NORMAL\n")
                resultado_text.insert(tk.END, "=" * 50 + "\n\n")
                resultado_text.insert(tk.END, f"Parámetros:\n")
                resultado_text.insert(tk.END, f"  μ (media) = {mu}\n")
                resultado_text.insert(tk.END, f"  σ (desv. estándar) = {sigma}\n\n")

                # Calcular Z-score
                z = (x - mu) / sigma

                if tipo == "menor":
                    # P(X < x)
                    # Usando la función de distribución acumulada de la normal estándar
                    from scipy.stats import norm
                    prob = norm.cdf(z)
                    resultado_text.insert(tk.END, f"Cálculo: P(X < {x})\n\n")
                    resultado_text.insert(tk.END, f"Z-score: z = (x - μ) / σ = {z:.4f}\n\n")
                    resultado_text.insert(tk.END, f"Resultado:\n")
                    resultado_text.insert(tk.END, f"  P(X < {x}) = {prob:.6f}\n")
                    resultado_text.insert(tk.END, f"  P(X < {x}) = {prob * 100:.4f}%\n")

                elif tipo == "mayor":
                    # P(X > x)
                    from scipy.stats import norm
                    prob = 1 - norm.cdf(z)
                    resultado_text.insert(tk.END, f"Cálculo: P(X > {x})\n\n")
                    resultado_text.insert(tk.END, f"Z-score: z = (x - μ) / σ = {z:.4f}\n\n")
                    resultado_text.insert(tk.END, f"Resultado:\n")
                    resultado_text.insert(tk.END, f"  P(X > {x}) = {prob:.6f}\n")
                    resultado_text.insert(tk.END, f"  P(X > {x}) = {prob * 100:.4f}%\n")

                elif tipo == "entre":
                    # P(a < X < b)
                    b = float(b_entry.get())
                    if b <= x:
                        raise ValueError("b debe ser mayor que a")

                    from scipy.stats import norm
                    z_a = (x - mu) / sigma
                    z_b = (b - mu) / sigma
                    prob = norm.cdf(z_b) - norm.cdf(z_a)

                    resultado_text.insert(tk.END, f"Cálculo: P({x} < X < {b})\n\n")
                    resultado_text.insert(tk.END, f"Z-scores:\n")
                    resultado_text.insert(tk.END, f"  z_a = ({x} - μ) / σ = {z_a:.4f}\n")
                    resultado_text.insert(tk.END, f"  z_b = ({b} - μ) / σ = {z_b:.4f}\n\n")
                    resultado_text.insert(tk.END, f"Resultado:\n")
                    resultado_text.insert(tk.END, f"  P({x} < X < {b}) = {prob:.6f}\n")
                    resultado_text.insert(tk.END, f"  P({x} < X < {b}) = {prob * 100:.4f}%\n")

                resultado_text.insert(tk.END, "\n" + "=" * 50 + "\n")

            except ValueError as e:
                messagebox.showerror("Error", f"Entrada inválida: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al calcular: {e}")

        tk.Button(lf, text="Calcular Probabilidad", command=calcular,
                 font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=2, pady=10)

    def chi_square_self_window(self, root):
        self.clear_frame(root)

        # Frame principal
        main_frame = tk.Frame(root, bg="black")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Frame superior: Configuración
        config_frame = tk.LabelFrame(main_frame, text="Configuración de la Tabla de Contingencia",
                                      bg="black", fg="white", font=("Arial", 11, "bold"))
        config_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # Variables para dimensiones
        dim_frame = tk.Frame(config_frame, bg="black")
        dim_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(dim_frame, text="Número de filas (categorías):", bg="black").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        filas_entry = tk.Entry(dim_frame, width=10)
        filas_entry.insert(0, "4")
        filas_entry.grid(row=0, column=1, padx=5, pady=3)

        tk.Label(dim_frame, text="Número de columnas (categorías):", bg="black").grid(row=0, column=2, sticky="w", padx=5, pady=3)
        columnas_entry = tk.Entry(dim_frame, width=10)
        columnas_entry.insert(0, "3")
        columnas_entry.grid(row=0, column=3, padx=5, pady=3)

        tk.Label(dim_frame, text="Nivel de significancia α:", bg="black", fg="white").grid(row=0, column=4, sticky="w", padx=5, pady=3)
        alpha_entry = tk.Entry(dim_frame, width=10)
        alpha_entry.insert(0, "0.05")
        alpha_entry.grid(row=0, column=5, padx=5, pady=3)

        # Frame para la tabla de datos
        tabla_container = tk.Frame(main_frame, bg="black")
        tabla_container.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        tabla_container.rowconfigure(0, weight=1)
        tabla_container.columnconfigure(0, weight=1)

        # Canvas con scrollbar para la tabla
        canvas = tk.Canvas(tabla_container, bg="white")
        scrollbar_y = tk.Scrollbar(tabla_container, orient="vertical", command=canvas.yview)
        scrollbar_x = tk.Scrollbar(tabla_container, orient="horizontal", command=canvas.xview)
        tabla_frame = tk.Frame(canvas, bg="white")

        tabla_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=tabla_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Variables globales para la tabla
        tabla_widgets = {"entries": [], "labels_fila": [], "labels_columna": []}

        def crear_tabla():
            # Limpiar tabla anterior
            for widget in tabla_frame.winfo_children():
                widget.destroy()
            tabla_widgets["entries"].clear()
            tabla_widgets["labels_fila"].clear()
            tabla_widgets["labels_columna"].clear()

            try:
                n_filas = int(filas_entry.get())
                n_cols = int(columnas_entry.get())

                if n_filas < 2 or n_cols < 2:
                    raise ValueError("Debe haber al menos 2 filas y 2 columnas")

                # Encabezado vacío
                tk.Label(tabla_frame, text="", bg="lightgray", width=15, relief="ridge").grid(row=0, column=0, padx=1, pady=1)

                # Etiquetas de columnas
                for j in range(n_cols):
                    label_entry = tk.Entry(tabla_frame, width=12, justify="center", font=("Arial", 9, "bold"))
                    label_entry.insert(0, f"Categoría {j+1}")
                    label_entry.grid(row=0, column=j+1, padx=1, pady=1)
                    tabla_widgets["labels_columna"].append(label_entry)

                # Crear filas con etiquetas y entradas de datos
                for i in range(n_filas):
                    # Etiqueta de fila
                    label_entry = tk.Entry(tabla_frame, width=15, justify="left", font=("Arial", 9, "bold"))
                    label_entry.insert(0, f"Categoría {i+1}")
                    label_entry.grid(row=i+1, column=0, padx=1, pady=1)
                    tabla_widgets["labels_fila"].append(label_entry)

                    # Entradas de datos
                    fila_entries = []
                    for j in range(n_cols):
                        entry = tk.Entry(tabla_frame, width=12, justify="center")
                        entry.insert(0, "0")
                        entry.grid(row=i+1, column=j+1, padx=1, pady=1)
                        fila_entries.append(entry)
                    tabla_widgets["entries"].append(fila_entries)

            except ValueError as e:
                messagebox.showerror("Error", f"Dimensiones inválidas: {e}")

        def cargar_ejemplo():
            # Datos del Excel
            filas_entry.delete(0, tk.END)
            filas_entry.insert(0, "4")
            columnas_entry.delete(0, tk.END)
            columnas_entry.insert(0, "3")
            crear_tabla()

            # Etiquetas
            labels_fila = ["Toshiba", "Seagate", "Western Digital", "Maxtor"]
            labels_col = ["Baja", "Normal", "Alta"]
            datos = [[2, 8, 4], [2, 7, 1], [3, 4, 2], [2, 4, 1]]

            for i, label in enumerate(labels_fila):
                tabla_widgets["labels_fila"][i].delete(0, tk.END)
                tabla_widgets["labels_fila"][i].insert(0, label)

            for j, label in enumerate(labels_col):
                tabla_widgets["labels_columna"][j].delete(0, tk.END)
                tabla_widgets["labels_columna"][j].insert(0, label)

            for i in range(len(datos)):
                for j in range(len(datos[0])):
                    tabla_widgets["entries"][i][j].delete(0, tk.END)
                    tabla_widgets["entries"][i][j].insert(0, str(datos[i][j]))

        def importar_desde_excel():
            try:
                # Abrir diálogo para seleccionar archivo
                archivo = filedialog.askopenfilename(
                    title="Seleccionar archivo Excel",
                    filetypes=[
                        ("Archivos Excel", "*.xlsx *.xls"),
                        ("Todos los archivos", "*.*")
                    ]
                )

                if not archivo:
                    return  # Usuario canceló

                # Leer archivo Excel
                import pandas as pd
                df = pd.read_excel(archivo, sheet_name=0, header=0, index_col=0)

                # Detectar dimensiones
                n_filas = len(df)
                n_cols = len(df.columns)

                if n_filas < 2 or n_cols < 2:
                    messagebox.showerror("Error", "El archivo debe tener al menos 2 filas y 2 columnas de datos")
                    return

                # Actualizar campos de dimensiones
                filas_entry.delete(0, tk.END)
                filas_entry.insert(0, str(n_filas))
                columnas_entry.delete(0, tk.END)
                columnas_entry.insert(0, str(n_cols))

                # Crear tabla con las dimensiones detectadas
                crear_tabla()

                # Extraer etiquetas de filas (índice del DataFrame)
                labels_fila = df.index.tolist()
                for i, label in enumerate(labels_fila):
                    tabla_widgets["labels_fila"][i].delete(0, tk.END)
                    tabla_widgets["labels_fila"][i].insert(0, str(label))

                # Extraer etiquetas de columnas
                labels_col = df.columns.tolist()
                for j, label in enumerate(labels_col):
                    tabla_widgets["labels_columna"][j].delete(0, tk.END)
                    tabla_widgets["labels_columna"][j].insert(0, str(label))

                # Cargar datos
                datos = df.values
                for i in range(n_filas):
                    for j in range(n_cols):
                        valor = datos[i, j]
                        # Verificar si es un número válido
                        try:
                            valor_num = float(valor)
                            if valor_num < 0:
                                messagebox.showwarning("Advertencia",
                                    f"Valor negativo detectado en fila {i+1}, columna {j+1}. Se establecerá a 0.")
                                valor_num = 0
                            tabla_widgets["entries"][i][j].delete(0, tk.END)
                            tabla_widgets["entries"][i][j].insert(0, str(int(valor_num) if valor_num.is_integer() else valor_num))
                        except (ValueError, TypeError):
                            messagebox.showwarning("Advertencia",
                                f"Valor no numérico en fila {i+1}, columna {j+1}. Se establecerá a 0.")
                            tabla_widgets["entries"][i][j].delete(0, tk.END)
                            tabla_widgets["entries"][i][j].insert(0, "0")

                messagebox.showinfo("Éxito", f"Datos importados correctamente:\n{n_filas} filas × {n_cols} columnas")

            except Exception as e:
                messagebox.showerror("Error al importar", f"No se pudo importar el archivo:\n{str(e)}")

        def calcular_chi_cuadrado():
            try:
                import numpy as np
                from scipy.stats import chi2

                # Obtener datos
                n_filas = len(tabla_widgets["entries"])
                n_cols = len(tabla_widgets["entries"][0]) if n_filas > 0 else 0

                if n_filas == 0 or n_cols == 0:
                    messagebox.showwarning("Advertencia", "Primero crea la tabla")
                    return

                # Leer datos observados
                datos = []
                for i in range(n_filas):
                    fila = []
                    for j in range(n_cols):
                        valor = float(tabla_widgets["entries"][i][j].get())
                        if valor < 0:
                            raise ValueError("Los valores deben ser no negativos")
                        fila.append(valor)
                    datos.append(fila)

                datos = np.array(datos)

                # Calcular totales
                total_filas = datos.sum(axis=1)
                total_columnas = datos.sum(axis=0)
                total_general = datos.sum()

                if total_general == 0:
                    raise ValueError("El total general no puede ser 0")

                # Calcular frecuencias esperadas
                frecuencias_esperadas = np.zeros_like(datos, dtype=float)
                for i in range(n_filas):
                    for j in range(n_cols):
                        frecuencias_esperadas[i, j] = (total_filas[i] * total_columnas[j]) / total_general

                # Calcular estadístico Chi cuadrado
                chi_cuadrado_calc = 0
                detalles = []
                for i in range(n_filas):
                    for j in range(n_cols):
                        fo = datos[i, j]
                        fe = frecuencias_esperadas[i, j]
                        if fe > 0:
                            contribucion = ((fo - fe) ** 2) / fe
                            chi_cuadrado_calc += contribucion
                            detalles.append({
                                'fila': i, 'col': j,
                                'fo': fo, 'fe': fe,
                                'diff': fo - fe,
                                'diff2': (fo - fe) ** 2,
                                'contribucion': contribucion
                            })

                # Grados de libertad
                grados_libertad = (n_filas - 1) * (n_cols - 1)

                # Nivel de significancia
                alpha = float(alpha_entry.get())
                if not (0 < alpha < 1):
                    raise ValueError("α debe estar entre 0 y 1")

                # Valor crítico
                valor_critico = chi2.ppf(1 - alpha, grados_libertad)

                # P-value
                p_value = 1 - chi2.cdf(chi_cuadrado_calc, grados_libertad)

                # Decisión
                if chi_cuadrado_calc > valor_critico:
                    decision = "RECHAZAR"
                    conclusion = "SÍ existe relación entre las variables"
                else:
                    decision = "ACEPTAR"
                    conclusion = "NO existe relación entre las variables"

                # Mostrar resultados en ventana nueva
                resultado_win = tk.Toplevel(root)
                resultado_win.title("Resultados - Prueba Chi Cuadrado de Independencia")
                resultado_win.geometry("900x700")

                # Frame con scroll
                resultado_canvas = tk.Canvas(resultado_win)
                resultado_scroll = tk.Scrollbar(resultado_win, orient="vertical", command=resultado_canvas.yview)
                resultado_frame = tk.Frame(resultado_canvas, bg="white")

                resultado_frame.bind("<Configure>", lambda e: resultado_canvas.configure(scrollregion=resultado_canvas.bbox("all")))
                resultado_canvas.create_window((0, 0), window=resultado_frame, anchor="nw")
                resultado_canvas.configure(yscrollcommand=resultado_scroll.set)

                resultado_canvas.pack(side="left", fill="both", expand=True)
                resultado_scroll.pack(side="right", fill="y")

                # Contenido
                texto = tk.Text(resultado_frame, wrap="word", font=("Courier", 10), bg="white")
                texto.pack(fill="both", expand=True, padx=10, pady=10)

                # Escribir resultados
                texto.insert(tk.END, "=" * 90 + "\n")
                texto.insert(tk.END, " " * 20 + "PRUEBA CHI CUADRADO DE INDEPENDENCIA\n")
                texto.insert(tk.END, "=" * 90 + "\n\n")

                # Hipótesis
                texto.insert(tk.END, "HIPÓTESIS:\n")
                texto.insert(tk.END, "-" * 90 + "\n")
                texto.insert(tk.END, "H₀ (Hipótesis Nula):\n")
                texto.insert(tk.END, "   No existe relación entre las variables de fila y columna.\n")
                texto.insert(tk.END, "   (Las variables son independientes)\n\n")
                texto.insert(tk.END, "H₁ (Hipótesis Alternativa):\n")
                texto.insert(tk.END, "   Sí existe relación entre las variables de fila y columna.\n")
                texto.insert(tk.END, "   (Las variables NO son independientes)\n\n")

                # Tabla de frecuencias observadas
                texto.insert(tk.END, "FRECUENCIAS OBSERVADAS (fo):\n")
                texto.insert(tk.END, "-" * 90 + "\n")
                texto.insert(tk.END, f"{'':20s}")
                for j in range(n_cols):
                    texto.insert(tk.END, f"{tabla_widgets['labels_columna'][j].get():>12s}")
                texto.insert(tk.END, f"{'Total':>12s}\n")

                for i in range(n_filas):
                    texto.insert(tk.END, f"{tabla_widgets['labels_fila'][i].get():20s}")
                    for j in range(n_cols):
                        texto.insert(tk.END, f"{datos[i,j]:12.0f}")
                    texto.insert(tk.END, f"{total_filas[i]:12.0f}\n")

                texto.insert(tk.END, f"{'Total':20s}")
                for j in range(n_cols):
                    texto.insert(tk.END, f"{total_columnas[j]:12.0f}")
                texto.insert(tk.END, f"{total_general:12.0f}\n\n")

                # Tabla de frecuencias esperadas
                texto.insert(tk.END, "FRECUENCIAS ESPERADAS (fe):\n")
                texto.insert(tk.END, "-" * 90 + "\n")
                texto.insert(tk.END, f"{'':20s}")
                for j in range(n_cols):
                    texto.insert(tk.END, f"{tabla_widgets['labels_columna'][j].get():>12s}")
                texto.insert(tk.END, "\n")

                for i in range(n_filas):
                    texto.insert(tk.END, f"{tabla_widgets['labels_fila'][i].get():20s}")
                    for j in range(n_cols):
                        texto.insert(tk.END, f"{frecuencias_esperadas[i,j]:12.4f}")
                    texto.insert(tk.END, "\n")
                texto.insert(tk.END, "\n")

                # Cálculos detallados
                texto.insert(tk.END, "CÁLCULOS DETALLADOS:\n")
                texto.insert(tk.END, "-" * 90 + "\n")
                texto.insert(tk.END, f"{'Celda':15s} {'fo':>10s} {'fe':>10s} {'fo-fe':>10s} {'(fo-fe)²':>12s} {'(fo-fe)²/fe':>15s}\n")
                texto.insert(tk.END, "-" * 90 + "\n")

                for detalle in detalles:
                    i, j = detalle['fila'], detalle['col']
                    celda = f"[{tabla_widgets['labels_fila'][i].get()[:8]},{tabla_widgets['labels_columna'][j].get()[:8]}]"
                    texto.insert(tk.END, f"{celda:15s} {detalle['fo']:10.2f} {detalle['fe']:10.4f} "
                                       f"{detalle['diff']:10.4f} {detalle['diff2']:12.6f} "
                                       f"{detalle['contribucion']:15.6f}\n")

                texto.insert(tk.END, "\n")

                # Resultados estadísticos
                texto.insert(tk.END, "RESULTADOS ESTADÍSTICOS:\n")
                texto.insert(tk.END, "=" * 90 + "\n")
                texto.insert(tk.END, f"Chi Cuadrado Calculado (χ²):     {chi_cuadrado_calc:12.6f}\n")
                texto.insert(tk.END, f"Grados de Libertad:              {grados_libertad:12d}  [(filas-1) × (columnas-1) = ({n_filas}-1) × ({n_cols}-1)]\n")
                texto.insert(tk.END, f"Nivel de Significancia (α):      {alpha:12.4f}\n")
                texto.insert(tk.END, f"Nivel de Confianza (1-α):        {1-alpha:12.4f}  ({(1-alpha)*100:.2f}%)\n")
                texto.insert(tk.END, f"Valor Crítico de χ²:             {valor_critico:12.6f}\n")
                texto.insert(tk.END, f"P-value:                         {p_value:12.6f}\n")
                texto.insert(tk.END, "=" * 90 + "\n\n")

                # Regla de decisión
                texto.insert(tk.END, "REGLA DE DECISIÓN:\n")
                texto.insert(tk.END, "-" * 90 + "\n")
                texto.insert(tk.END, "Si χ² calculado > χ² crítico → RECHAZAR H₀\n")
                texto.insert(tk.END, "Si χ² calculado ≤ χ² crítico → ACEPTAR H₀\n\n")

                # Decisión
                texto.insert(tk.END, "DECISIÓN:\n")
                texto.insert(tk.END, "=" * 90 + "\n")
                texto.insert(tk.END, f"χ² calculado ({chi_cuadrado_calc:.6f}) ")
                if chi_cuadrado_calc > valor_critico:
                    texto.insert(tk.END, f"> χ² crítico ({valor_critico:.6f})\n")
                else:
                    texto.insert(tk.END, f"≤ χ² crítico ({valor_critico:.6f})\n")
                texto.insert(tk.END, f"\n>>> {decision} la Hipótesis Nula <<<\n\n")
                texto.insert(tk.END, f"CONCLUSIÓN:\n{conclusion}\n")
                texto.insert(tk.END, "=" * 90 + "\n")

                texto.config(state="disabled")

            except ValueError as e:
                messagebox.showerror("Error", f"Error en los datos: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al calcular: {e}")

        # Botones
        botones_frame = tk.Frame(config_frame, bg="black")
        botones_frame.pack(padx=10, pady=5, fill="x")

        tk.Button(botones_frame, text="Crear Tabla", command=crear_tabla,
                 font=("Arial", 10, "bold"), bg="lightblue").pack(side="left", padx=5)

        # Menubutton para importar datos
        importar_btn = tk.Menubutton(botones_frame, text="Importar Datos ▼",
                                     font=("Arial", 10, "bold"), bg="lightgreen",
                                     relief="raised", borderwidth=2)
        importar_menu = tk.Menu(importar_btn, tearoff=False)
        importar_menu.add_command(label="📊 Ejemplo (Disco Duro)", command=cargar_ejemplo)
        importar_menu.add_command(label="📁 Desde archivo Excel...", command=importar_desde_excel)
        importar_btn.config(menu=importar_menu)
        importar_btn.pack(side="left", padx=5)

        tk.Button(botones_frame, text="Calcular χ²", command=calcular_chi_cuadrado,
                 font=("Arial", 10, "bold"), bg="lightyellow").pack(side="left", padx=5)

        # Crear tabla inicial
        crear_tabla()

    def gamma_self_window(self, root):
        self.clear_frame(root)

        lf = tk.LabelFrame(root, text="Distribución Gamma", bg="black", fg="white", font=("Arial", 12, "bold"))
        lf.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        lf.columnconfigure(1, weight=1)

        # Parámetros de la distribución
        tk.Label(lf, text="Parámetro de forma α (alpha):").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        alpha_entry = tk.Entry(lf)
        alpha_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(lf, text="Parámetro de escala β (beta):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        beta_entry = tk.Entry(lf)
        beta_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        # Tipo de cálculo
        tk.Label(lf, text="Tipo de cálculo:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        tipo_var = tk.StringVar(value="menor_igual")
        frame_tipo = tk.Frame(lf, bg="black")
        frame_tipo.grid(row=2, column=1, sticky="w", pady=5, padx=5)
        tk.Radiobutton(frame_tipo, text="P(X ≤ x)", variable=tipo_var, value="menor_igual", bg="black").pack(side="left", padx=5)
        tk.Radiobutton(frame_tipo, text="P(X > x)", variable=tipo_var, value="mayor", bg="black").pack(side="left", padx=5)
        tk.Radiobutton(frame_tipo, text="P(a ≤ X ≤ b)", variable=tipo_var, value="entre", bg="black").pack(side="left", padx=5)

        # Valores
        tk.Label(lf, text="Valor x (o valor a):").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        x_entry = tk.Entry(lf)
        x_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(lf, text="Valor b (solo para 'entre'):").grid(row=4, column=0, sticky="w", pady=5, padx=5)
        b_entry = tk.Entry(lf)
        b_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=5)

        # Frame para resultados
        resultado_frame = tk.Frame(lf, bg="white", relief="sunken", borderwidth=2)
        resultado_frame.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        lf.rowconfigure(6, weight=1)

        resultado_text = tk.Text(resultado_frame, height=8, wrap="word", font=("Courier", 10))
        resultado_text.pack(fill="both", expand=True)

        def calcular():
            try:
                alpha = float(alpha_entry.get())
                beta = float(beta_entry.get())

                if alpha <= 0:
                    raise ValueError("α debe ser mayor que 0")
                if beta <= 0:
                    raise ValueError("β debe ser mayor que 0")

                tipo = tipo_var.get()
                x = float(x_entry.get())

                if x < 0:
                    raise ValueError("x debe ser no negativo")

                resultado_text.delete(1.0, tk.END)
                resultado_text.insert(tk.END, "=" * 50 + "\n")
                resultado_text.insert(tk.END, "  DISTRIBUCIÓN GAMMA\n")
                resultado_text.insert(tk.END, "=" * 50 + "\n\n")
                resultado_text.insert(tk.END, f"Parámetros:\n")
                resultado_text.insert(tk.END, f"  α (forma) = {alpha}\n")
                resultado_text.insert(tk.END, f"  β (escala) = {beta}\n\n")

                from scipy.stats import gamma

                if tipo == "menor_igual":
                    # P(X ≤ x)
                    prob = gamma.cdf(x, alpha, scale=beta)
                    resultado_text.insert(tk.END, f"Cálculo: P(X ≤ {x})\n\n")
                    resultado_text.insert(tk.END, f"Resultado:\n")
                    resultado_text.insert(tk.END, f"  P(X ≤ {x}) = {prob:.6f}\n")
                    resultado_text.insert(tk.END, f"  P(X ≤ {x}) = {prob * 100:.4f}%\n")

                elif tipo == "mayor":
                    # P(X > x)
                    prob = 1 - gamma.cdf(x, alpha, scale=beta)
                    resultado_text.insert(tk.END, f"Cálculo: P(X > {x})\n\n")
                    resultado_text.insert(tk.END, f"Resultado:\n")
                    resultado_text.insert(tk.END, f"  P(X > {x}) = {prob:.6f}\n")
                    resultado_text.insert(tk.END, f"  P(X > {x}) = {prob * 100:.4f}%\n")

                elif tipo == "entre":
                    # P(a ≤ X ≤ b)
                    b = float(b_entry.get())
                    if b <= x:
                        raise ValueError("b debe ser mayor que a")
                    if b < 0:
                        raise ValueError("b debe ser no negativo")

                    prob = gamma.cdf(b, alpha, scale=beta) - gamma.cdf(x, alpha, scale=beta)

                    resultado_text.insert(tk.END, f"Cálculo: P({x} ≤ X ≤ {b})\n\n")
                    resultado_text.insert(tk.END, f"Resultado:\n")
                    resultado_text.insert(tk.END, f"  P({x} ≤ X ≤ {b}) = {prob:.6f}\n")
                    resultado_text.insert(tk.END, f"  P({x} ≤ X ≤ {b}) = {prob * 100:.4f}%\n")

                # Agregar información adicional
                media = alpha * beta
                varianza = alpha * (beta ** 2)
                resultado_text.insert(tk.END, f"\nInformación adicional:\n")
                resultado_text.insert(tk.END, f"  Media (E[X]) = {media:.4f}\n")
                resultado_text.insert(tk.END, f"  Varianza (Var[X]) = {varianza:.4f}\n")

                resultado_text.insert(tk.END, "\n" + "=" * 50 + "\n")

            except ValueError as e:
                messagebox.showerror("Error", f"Entrada inválida: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al calcular: {e}")

        tk.Button(lf, text="Calcular Probabilidad", command=calcular,
                 font=("Arial", 10, "bold")).grid(row=5, column=0, columnspan=2, pady=10)

    def exponential_self_window(self, root):
        self.clear_frame(root)

        lf = tk.LabelFrame(root, text="Distribución Exponencial", bg="black", fg="white", font=("Arial", 12, "bold"))
        lf.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        lf.columnconfigure(1, weight=1)

        # Parámetros de la distribución
        tk.Label(lf, text="Tasa λ (lambda):").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        lambda_entry = tk.Entry(lf)
        lambda_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        # Tipo de cálculo
        tk.Label(lf, text="Tipo de cálculo:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        tipo_var = tk.StringVar(value="menor_igual")
        frame_tipo = tk.Frame(lf, bg="black")
        frame_tipo.grid(row=1, column=1, sticky="w", pady=5, padx=5)
        tk.Radiobutton(frame_tipo, text="P(X ≤ x)", variable=tipo_var, value="menor_igual", bg="black").pack(side="left", padx=5)
        tk.Radiobutton(frame_tipo, text="P(X > x)", variable=tipo_var, value="mayor", bg="black").pack(side="left", padx=5)
        tk.Radiobutton(frame_tipo, text="P(a ≤ X ≤ b)", variable=tipo_var, value="entre", bg="black").pack(side="left", padx=5)

        # Valores
        tk.Label(lf, text="Valor x (o valor a):").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        x_entry = tk.Entry(lf)
        x_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

        tk.Label(lf, text="Valor b (solo para 'entre'):").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        b_entry = tk.Entry(lf)
        b_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=5)

        # Frame para resultados
        resultado_frame = tk.Frame(lf, bg="white", relief="sunken", borderwidth=2)
        resultado_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        lf.rowconfigure(5, weight=1)

        resultado_text = tk.Text(resultado_frame, height=8, wrap="word", font=("Courier", 10))
        resultado_text.pack(fill="both", expand=True)

        def calcular():
            try:
                lmbda = float(lambda_entry.get())

                if lmbda <= 0:
                    raise ValueError("λ debe ser mayor que 0")

                tipo = tipo_var.get()
                x = float(x_entry.get())

                if x < 0:
                    raise ValueError("x debe ser no negativo")

                resultado_text.delete(1.0, tk.END)
                resultado_text.insert(tk.END, "=" * 50 + "\n")
                resultado_text.insert(tk.END, "  DISTRIBUCIÓN EXPONENCIAL\n")
                resultado_text.insert(tk.END, "=" * 50 + "\n\n")
                resultado_text.insert(tk.END, f"Parámetros:\n")
                resultado_text.insert(tk.END, f"  λ (tasa) = {lmbda}\n\n")

                from scipy.stats import expon

                # scipy.stats.expon usa scale = 1/λ
                scale = 1 / lmbda

                if tipo == "menor_igual":
                    # P(X ≤ x)
                    prob = expon.cdf(x, scale=scale)
                    resultado_text.insert(tk.END, f"Cálculo: P(X ≤ {x})\n\n")
                    resultado_text.insert(tk.END, f"Resultado:\n")
                    resultado_text.insert(tk.END, f"  P(X ≤ {x}) = {prob:.6f}\n")
                    resultado_text.insert(tk.END, f"  P(X ≤ {x}) = {prob * 100:.4f}%\n")

                elif tipo == "mayor":
                    # P(X > x)
                    prob = 1 - expon.cdf(x, scale=scale)
                    resultado_text.insert(tk.END, f"Cálculo: P(X > {x})\n\n")
                    resultado_text.insert(tk.END, f"Resultado:\n")
                    resultado_text.insert(tk.END, f"  P(X > {x}) = {prob:.6f}\n")
                    resultado_text.insert(tk.END, f"  P(X > {x}) = {prob * 100:.4f}%\n")

                elif tipo == "entre":
                    # P(a ≤ X ≤ b)
                    b = float(b_entry.get())
                    if b <= x:
                        raise ValueError("b debe ser mayor que a")
                    if b < 0:
                        raise ValueError("b debe ser no negativo")

                    prob = expon.cdf(b, scale=scale) - expon.cdf(x, scale=scale)

                    resultado_text.insert(tk.END, f"Cálculo: P({x} ≤ X ≤ {b})\n\n")
                    resultado_text.insert(tk.END, f"Resultado:\n")
                    resultado_text.insert(tk.END, f"  P({x} ≤ X ≤ {b}) = {prob:.6f}\n")
                    resultado_text.insert(tk.END, f"  P({x} ≤ X ≤ {b}) = {prob * 100:.4f}%\n")

                # Agregar información adicional
                media = 1 / lmbda
                varianza = 1 / (lmbda ** 2)
                resultado_text.insert(tk.END, f"\nInformación adicional:\n")
                resultado_text.insert(tk.END, f"  Media (E[X]) = {media:.4f}\n")
                resultado_text.insert(tk.END, f"  Varianza (Var[X]) = {varianza:.4f}\n")

                resultado_text.insert(tk.END, "\n" + "=" * 50 + "\n")

            except ValueError as e:
                messagebox.showerror("Error", f"Entrada inválida: {e}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al calcular: {e}")

        tk.Button(lf, text="Calcular Probabilidad", command=calcular,
                 font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=2, pady=10)

    def running(self):
        if self.is_embedded:
            # === Toolbar pegada arriba ===
            self.toolbar = tk.Frame(self.sub_window, bg="black")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
            self.toolbar.grid(row=0, column=0, sticky="ew")

            # Menubuttons en la barra (grid ya está aplicado en init)
            btn_simple = tk.Menubutton(self.toolbar, text="Probabilidad Elemental")
            menu_simple = tk.Menu(btn_simple, tearoff=False)
            menu_simple.add_command(label="Sucesos Simples", command=lambda: self.simple_success(self.principle_frame))
            menu_simple.add_command(label="Sucesos Excluyentes", command=lambda: self.exclusive_success(self.principle_frame))
            menu_simple.add_command(label="Sucesos Dependientes", command=lambda: self.dependant_success(self.principle_frame))
            menu_simple.add_command(label="Sucesos Independientes", command=lambda: self.independent_success(self.principle_frame))
            menu_simple.add_command(label="Sucesos No Excluyentes", command=lambda: self.non_exclusive_success(self.principle_frame))
            btn_simple.config(menu=menu_simple)
            btn_simple.pack(side="left", padx=5, pady=2)

            btn_tree = tk.Menubutton(self.toolbar, text="Diagramas de Árbol")
            menu_tree = tk.Menu(btn_tree, tearoff=False)
            menu_tree.add_command(label="Diagrama de Árbol", command=lambda: self.tree_diagram_self_window(self.principle_frame))
            btn_tree.config(menu=menu_tree)
            btn_tree.pack(side="left", padx=5, pady=2)

            btn_dist = tk.Menubutton(self.toolbar, text="Distribuciones")
            menu_dist = tk.Menu(btn_dist, tearoff=False)
            menu_dist.add_command(label="Bernoulli", command=lambda: self.bernoulli_self_window(self.principle_frame))
            menu_dist.add_command(label="Binomial", command=lambda: self.binomial_self_window(self.principle_frame))
            menu_dist.add_command(label="Poisson", command=lambda: self.poisson_self_window(self.principle_frame))
<<<<<<< HEAD
=======
            menu_dist.add_command(label="Normal", command=lambda: self.normal_self_window(self.principle_frame))
            menu_dist.add_command(label="Chi Cuadrado - Prueba de Independencia", command=lambda: self.chi_square_self_window(self.principle_frame))
            menu_dist.add_command(label="Gamma", command=lambda: self.gamma_self_window(self.principle_frame))
            menu_dist.add_command(label="Exponencial", command=lambda: self.exponential_self_window(self.principle_frame))
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
            btn_dist.config(menu=menu_dist)
            btn_dist.pack(side="left", padx=5, pady=2)

        else:
            # === Menú clásico ===
            menu_bar = tk.Menu(self.sub_window)
            self.sub_window.configure(menu=menu_bar)
