import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class Graphs:
    """Clase para generar gráficos estadísticos"""

    def __init__(
        self, root, tabla_obj, x=0, y=0, width=800, height=600, parent_frame=None
    ):
        self.tabla_obj = tabla_obj
        self.is_embedded = parent_frame is not None

        if self.is_embedded:
            # Modo embebido dentro de un frame
            self.sub_window = tk.Frame(parent_frame, bg="black")
            self.sub_window.grid(row=0, column=0, sticky="nsew")
            parent_frame.rowconfigure(0, weight=1)
            parent_frame.columnconfigure(0, weight=1)
        else:
            # Modo ventana independiente
            self.sub_window = tk.Toplevel(root)
            self.sub_window.title("Gráficos Estadísticos")
            self.sub_window.geometry(f"{width}x{height}+{x}+{y}")
            self.sub_window.configure(bg="black")

        # Frame principal
        self.principle_frame = tk.Frame(self.sub_window, bg="black")
        if self.is_embedded:
            self.principle_frame.grid(row=1, column=0, sticky="nsew")
            self.sub_window.rowconfigure(1, weight=1)
            self.sub_window.columnconfigure(0, weight=1)
        else:
            self.principle_frame.grid(row=0, column=0, sticky="nsew")
            self.sub_window.rowconfigure(0, weight=1)
            self.sub_window.columnconfigure(0, weight=1)

    def clear_frame(self, frame):
        """Limpiar todos los widgets de un frame"""
        for widget in frame.winfo_children():
            widget.destroy()

    def obtener_datos_numericos(self, variable):
        """Obtener datos numéricos de una variable"""
        datos = self.tabla_obj.obtener_columna(variable)
        datos_numericos = []
        for valor in datos:
            try:
                if valor != "-":
                    datos_numericos.append(float(valor))
            except (ValueError, TypeError):
                pass
        return datos_numericos

    def crear_figura_en_frame(self, parent_frame):
        """Crear figura de matplotlib embebida en tkinter"""
        # Frame para el gráfico
        graph_frame = tk.Frame(parent_frame, bg="white")
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Crear figura
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)

        # Canvas para mostrar el gráfico
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Toolbar de matplotlib
        toolbar = NavigationToolbar2Tk(canvas, graph_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        return fig, ax, canvas

    def histograma(self, root):
        """Generar histograma"""
        self.clear_frame(root)

        # Frame de controles
        control_frame = tk.Frame(root, bg="black")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(
            control_frame,
            text="Variable:",
            bg="black",
            fg="white",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)

        columnas = self.tabla_obj.columnas
        variable_combo = ttk.Combobox(
            control_frame, values=columnas, state="readonly", width=20
        )
        if columnas:
            variable_combo.set(columnas[0])
        variable_combo.pack(side=tk.LEFT, padx=5)

        tk.Label(
            control_frame, text="Bins:", bg="black", fg="white", font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        bins_entry = tk.Entry(control_frame, width=10)
        bins_entry.insert(0, "10")
        bins_entry.pack(side=tk.LEFT, padx=5)

        # Frame para el gráfico
        graph_container = tk.Frame(root, bg="black")
        graph_container.pack(fill=tk.BOTH, expand=True)

        def generar():
            try:
                variable = variable_combo.get()
                datos = self.obtener_datos_numericos(variable)

                if len(datos) == 0:
                    messagebox.showerror("Error", "No hay datos numéricos disponibles")
                    return

                bins = int(bins_entry.get())

                # Limpiar frame
                self.clear_frame(graph_container)

                # Crear gráfico
                fig, ax, canvas = self.crear_figura_en_frame(graph_container)

                ax.hist(datos, bins=bins, color="skyblue", edgecolor="black", alpha=0.7)
                ax.set_xlabel("Valores", fontsize=12)
                ax.set_ylabel("Frecuencia", fontsize=12)
                ax.set_title(
                    f"Histograma de {variable}", fontsize=14, fontweight="bold"
                )
                ax.grid(True, alpha=0.3)

                canvas.draw()

            except ValueError:
                messagebox.showerror("Error", "Número de bins inválido")
            except Exception as e:
                messagebox.showerror("Error", f"Error al generar histograma: {str(e)}")

        tk.Button(
            control_frame,
            text="Generar Histograma",
            command=generar,
            font=("Arial", 10, "bold"),
            bg="lightblue",
        ).pack(side=tk.LEFT, padx=10)

    def poligono_frecuencia(self, root):
        """Generar polígono de frecuencia"""
        self.clear_frame(root)

        # Frame de controles
        control_frame = tk.Frame(root, bg="black")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(
            control_frame,
            text="Variable:",
            bg="black",
            fg="white",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)

        columnas = self.tabla_obj.columnas
        variable_combo = ttk.Combobox(
            control_frame, values=columnas, state="readonly", width=20
        )
        if columnas:
            variable_combo.set(columnas[0])
        variable_combo.pack(side=tk.LEFT, padx=5)

        tk.Label(
            control_frame, text="Bins:", bg="black", fg="white", font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        bins_entry = tk.Entry(control_frame, width=10)
        bins_entry.insert(0, "10")
        bins_entry.pack(side=tk.LEFT, padx=5)

        # Frame para el gráfico
        graph_container = tk.Frame(root, bg="black")
        graph_container.pack(fill=tk.BOTH, expand=True)

        def generar():
            try:
                variable = variable_combo.get()
                datos = self.obtener_datos_numericos(variable)

                if len(datos) == 0:
                    messagebox.showerror("Error", "No hay datos numéricos disponibles")
                    return

                bins = int(bins_entry.get())

                # Calcular frecuencias
                hist, bin_edges = np.histogram(datos, bins=bins)
                bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

                # Limpiar frame
                self.clear_frame(graph_container)

                # Crear gráfico
                fig, ax, canvas = self.crear_figura_en_frame(graph_container)

                ax.plot(
                    bin_centers,
                    hist,
                    marker="o",
                    color="blue",
                    linewidth=2,
                    markersize=8,
                )
                ax.fill_between(bin_centers, hist, alpha=0.3, color="skyblue")
                ax.set_xlabel("Valores", fontsize=12)
                ax.set_ylabel("Frecuencia", fontsize=12)
                ax.set_title(
                    f"Polígono de Frecuencia de {variable}",
                    fontsize=14,
                    fontweight="bold",
                )
                ax.grid(True, alpha=0.3)

                canvas.draw()

            except ValueError:
                messagebox.showerror("Error", "Número de bins inválido")
            except Exception as e:
                messagebox.showerror("Error", f"Error al generar polígono: {str(e)}")

        tk.Button(
            control_frame,
            text="Generar Polígono",
            command=generar,
            font=("Arial", 10, "bold"),
            bg="lightblue",
        ).pack(side=tk.LEFT, padx=10)

    def ojiva(self, root):
        """Generar ojiva (frecuencia acumulada)"""
        self.clear_frame(root)

        # Frame de controles
        control_frame = tk.Frame(root, bg="black")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(
            control_frame,
            text="Variable:",
            bg="black",
            fg="white",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)

        columnas = self.tabla_obj.columnas
        variable_combo = ttk.Combobox(
            control_frame, values=columnas, state="readonly", width=20
        )
        if columnas:
            variable_combo.set(columnas[0])
        variable_combo.pack(side=tk.LEFT, padx=5)

        tk.Label(
            control_frame, text="Tipo:", bg="black", fg="white", font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        tipo_combo = ttk.Combobox(
            control_frame,
            values=["Ascendente", "Descendente"],
            state="readonly",
            width=15,
        )
        tipo_combo.set("Ascendente")
        tipo_combo.pack(side=tk.LEFT, padx=5)

        # Frame para el gráfico
        graph_container = tk.Frame(root, bg="black")
        graph_container.pack(fill=tk.BOTH, expand=True)

        def generar():
            try:
                variable = variable_combo.get()
                datos = self.obtener_datos_numericos(variable)

                if len(datos) == 0:
                    messagebox.showerror("Error", "No hay datos numéricos disponibles")
                    return

                tipo = tipo_combo.get()
                datos_sorted = np.sort(datos)
                n = len(datos_sorted)

                if tipo == "Ascendente":
                    y_values = np.arange(1, n + 1) / n * 100
                    titulo = "Ojiva Ascendente (Menor que)"
                else:
                    y_values = np.arange(n, 0, -1) / n * 100
                    titulo = "Ojiva Descendente (Mayor que)"

                # Limpiar frame
                self.clear_frame(graph_container)

                # Crear gráfico
                fig, ax, canvas = self.crear_figura_en_frame(graph_container)

                ax.plot(
                    datos_sorted,
                    y_values,
                    marker="o",
                    color="green",
                    linewidth=2,
                    markersize=6,
                )
                ax.set_xlabel("Valores", fontsize=12)
                ax.set_ylabel("Frecuencia Acumulada (%)", fontsize=12)
                ax.set_title(f"{titulo} - {variable}", fontsize=14, fontweight="bold")
                ax.grid(True, alpha=0.3)

                canvas.draw()

            except Exception as e:
                messagebox.showerror("Error", f"Error al generar ojiva: {str(e)}")

        tk.Button(
            control_frame,
            text="Generar Ojiva",
            command=generar,
            font=("Arial", 10, "bold"),
            bg="lightblue",
        ).pack(side=tk.LEFT, padx=10)

    def grafico_barras(self, root):
        """Generar gráfico de barras"""
        self.clear_frame(root)

        # Frame de controles
        control_frame = tk.Frame(root, bg="black")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(
            control_frame,
            text="Variable:",
            bg="black",
            fg="white",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)

        columnas = self.tabla_obj.columnas
        variable_combo = ttk.Combobox(
            control_frame, values=columnas, state="readonly", width=20
        )
        if columnas:
            variable_combo.set(columnas[0])
        variable_combo.pack(side=tk.LEFT, padx=5)

        # Frame para el gráfico
        graph_container = tk.Frame(root, bg="black")
        graph_container.pack(fill=tk.BOTH, expand=True)

        def generar():
            try:
                variable = variable_combo.get()
                datos = self.tabla_obj.obtener_columna(variable)

                # Contar frecuencias
                df = pd.DataFrame({variable: datos})
                frecuencias = df[variable].value_counts().sort_index()

                if len(frecuencias) == 0:
                    messagebox.showerror("Error", "No hay datos disponibles")
                    return

                if len(frecuencias) > 50:
                    messagebox.showwarning(
                        "Advertencia",
                        "Demasiadas categorías (>50). El gráfico puede no ser legible.",
                    )

                # Limpiar frame
                self.clear_frame(graph_container)

                # Crear gráfico
                fig, ax, canvas = self.crear_figura_en_frame(graph_container)

                x = range(len(frecuencias))
                ax.bar(
                    x, frecuencias.values, color="coral", edgecolor="black", alpha=0.7
                )
                ax.set_xticks(x)
                ax.set_xticklabels(frecuencias.index, rotation=45, ha="right")
                ax.set_xlabel("Categorías", fontsize=12)
                ax.set_ylabel("Frecuencia", fontsize=12)
                ax.set_title(
                    f"Gráfico de Barras - {variable}", fontsize=14, fontweight="bold"
                )
                ax.grid(True, alpha=0.3, axis="y")

                fig.tight_layout()
                canvas.draw()

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Error al generar gráfico de barras: {str(e)}"
                )

        tk.Button(
            control_frame,
            text="Generar Gráfico de Barras",
            command=generar,
            font=("Arial", 10, "bold"),
            bg="lightblue",
        ).pack(side=tk.LEFT, padx=10)

    def grafico_circular(self, root):
        """Generar gráfico circular (pie chart)"""
        self.clear_frame(root)

        # Frame de controles
        control_frame = tk.Frame(root, bg="black")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(
            control_frame,
            text="Variable:",
            bg="black",
            fg="white",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)

        columnas = self.tabla_obj.columnas
        variable_combo = ttk.Combobox(
            control_frame, values=columnas, state="readonly", width=20
        )
        if columnas:
            variable_combo.set(columnas[0])
        variable_combo.pack(side=tk.LEFT, padx=5)

        tk.Label(
            control_frame,
            text="Máx. categorías:",
            bg="black",
            fg="white",
            font=("Arial", 10),
        ).pack(side=tk.LEFT, padx=5)
        max_cat_entry = tk.Entry(control_frame, width=10)
        max_cat_entry.insert(0, "10")
        max_cat_entry.pack(side=tk.LEFT, padx=5)

        # Frame para el gráfico
        graph_container = tk.Frame(root, bg="black")
        graph_container.pack(fill=tk.BOTH, expand=True)

        def generar():
            try:
                variable = variable_combo.get()
                datos = self.tabla_obj.obtener_columna(variable)
                max_cat = int(max_cat_entry.get())

                # Contar frecuencias
                df = pd.DataFrame({variable: datos})
                frecuencias = df[variable].value_counts()

                if len(frecuencias) == 0:
                    messagebox.showerror("Error", "No hay datos disponibles")
                    return

                # Limitar número de categorías
                if len(frecuencias) > max_cat:
                    frecuencias = frecuencias.head(max_cat)
                    otros = df[variable].value_counts().iloc[max_cat:].sum()
                    if otros > 0:
                        frecuencias["Otros"] = otros

                # Limpiar frame
                self.clear_frame(graph_container)

                # Crear gráfico
                fig, ax, canvas = self.crear_figura_en_frame(graph_container)

                colors = plt.cm.Set3(range(len(frecuencias)))
                wedges, texts, autotexts = ax.pie(
                    frecuencias.values,
                    labels=frecuencias.index,
                    autopct="%1.1f%%",
                    colors=colors,
                    startangle=90,
                )

                # Mejorar legibilidad
                for text in texts:
                    text.set_fontsize(10)
                for autotext in autotexts:
                    autotext.set_color("white")
                    autotext.set_fontweight("bold")
                    autotext.set_fontsize(9)

                ax.set_title(
                    f"Gráfico Circular - {variable}", fontsize=14, fontweight="bold"
                )

                canvas.draw()

            except ValueError:
                messagebox.showerror("Error", "Número máximo de categorías inválido")
            except Exception as e:
                messagebox.showerror(
                    "Error", f"Error al generar gráfico circular: {str(e)}"
                )

        tk.Button(
            control_frame,
            text="Generar Gráfico Circular",
            command=generar,
            font=("Arial", 10, "bold"),
            bg="lightblue",
        ).pack(side=tk.LEFT, padx=10)

    def diagrama_caja(self, root):
        """Generar diagrama de caja (boxplot)"""
        self.clear_frame(root)

        # Frame de controles
        control_frame = tk.Frame(root, bg="black")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(
            control_frame, text="Variable(s):", bg="black", font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)

        columnas = self.tabla_obj.columnas

        # Listbox para selección múltiple
        listbox_frame = tk.Frame(control_frame, bg="black")
        listbox_frame.pack(side=tk.LEFT, padx=5)

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(
            listbox_frame,
            selectmode=tk.MULTIPLE,
            height=5,
            yscrollcommand=scrollbar.set,
        )
        for col in columnas:
            listbox.insert(tk.END, col)
        listbox.pack(side=tk.LEFT)
        scrollbar.config(command=listbox.yview)

        # Frame para el gráfico
        graph_container = tk.Frame(root, bg="black")
        graph_container.pack(fill=tk.BOTH, expand=True)

        def generar():
            try:
                indices_seleccionados = listbox.curselection()
                if not indices_seleccionados:
                    messagebox.showwarning(
                        "Advertencia", "Selecciona al menos una variable"
                    )
                    return

                variables_seleccionadas = [columnas[i] for i in indices_seleccionados]
                datos_lista = []
                etiquetas = []

                for var in variables_seleccionadas:
                    datos_num = self.obtener_datos_numericos(var)
                    if len(datos_num) > 0:
                        datos_lista.append(datos_num)
                        etiquetas.append(var)

                if len(datos_lista) == 0:
                    messagebox.showerror("Error", "No hay datos numéricos disponibles")
                    return

                # Limpiar frame
                self.clear_frame(graph_container)

                # Crear gráfico
                fig, ax, canvas = self.crear_figura_en_frame(graph_container)

                bp = ax.boxplot(
                    datos_lista,
                    labels=etiquetas,
                    patch_artist=True,
                    showmeans=True,
                    meanline=True,
                )

                # Personalizar colores
                for patch in bp["boxes"]:
                    patch.set_facecolor("lightblue")
                    patch.set_alpha(0.7)

                for median in bp["medians"]:
                    median.set_color("red")
                    median.set_linewidth(2)

                for mean in bp["means"]:
                    mean.set_color("green")
                    mean.set_linewidth(2)

                ax.set_xlabel("Variables", fontsize=12)
                ax.set_ylabel("Valores", fontsize=12)
                ax.set_title("Diagrama de Caja", fontsize=14, fontweight="bold")
                ax.grid(True, alpha=0.3, axis="y")

                fig.tight_layout()
                canvas.draw()

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Error al generar diagrama de caja: {str(e)}"
                )

        tk.Button(
            control_frame,
            text="Generar Diagrama de Caja",
            command=generar,
            font=("Arial", 10, "bold"),
            bg="lightblue",
        ).pack(side=tk.LEFT, padx=10)

    def diagrama_dispersion(self, root):
        """Generar diagrama de dispersión"""
        self.clear_frame(root)

        # Frame de controles
        control_frame = tk.Frame(root, bg="black")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(
            control_frame,
            text="Variable X:",
            bg="black",
            fg="white",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)

        columnas = self.tabla_obj.columnas
        variable_x_combo = ttk.Combobox(
            control_frame, values=columnas, state="readonly", width=15
        )
        if columnas:
            variable_x_combo.set(columnas[0])
        variable_x_combo.pack(side=tk.LEFT, padx=5)

        tk.Label(
            control_frame,
            text="Variable Y:",
            bg="black",
            fg="white",
            font=("Arial", 10, "bold"),
        ).pack(side=tk.LEFT, padx=5)

        variable_y_combo = ttk.Combobox(
            control_frame, values=columnas, state="readonly", width=15
        )
        if len(columnas) > 1:
            variable_y_combo.set(columnas[1])
        elif columnas:
            variable_y_combo.set(columnas[0])
        variable_y_combo.pack(side=tk.LEFT, padx=5)

        # Frame para el gráfico
        graph_container = tk.Frame(root, bg="black")
        graph_container.pack(fill=tk.BOTH, expand=True)

        def generar():
            try:
                var_x = variable_x_combo.get()
                var_y = variable_y_combo.get()

                datos_x = self.obtener_datos_numericos(var_x)
                datos_y = self.obtener_datos_numericos(var_y)

                if len(datos_x) == 0 or len(datos_y) == 0:
                    messagebox.showerror("Error", "No hay datos numéricos disponibles")
                    return

                # Emparejar datos (tomar el mínimo de longitudes)
                min_len = min(len(datos_x), len(datos_y))
                datos_x = datos_x[:min_len]
                datos_y = datos_y[:min_len]

                # Limpiar frame
                self.clear_frame(graph_container)

                # Crear gráfico
                fig, ax, canvas = self.crear_figura_en_frame(graph_container)

                ax.scatter(
                    datos_x,
                    datos_y,
                    color="purple",
                    alpha=0.6,
                    s=50,
                    edgecolors="black",
                )
                ax.set_xlabel(var_x, fontsize=12)
                ax.set_ylabel(var_y, fontsize=12)
                ax.set_title(
                    f"Diagrama de Dispersión: {var_x} vs {var_y}",
                    fontsize=14,
                    fontweight="bold",
                )
                ax.grid(True, alpha=0.3)

                canvas.draw()

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Error al generar diagrama de dispersión: {str(e)}"
                )

        tk.Button(
            control_frame,
            text="Generar Diagrama",
            command=generar,
            font=("Arial", 10, "bold"),
            bg="lightblue",
        ).pack(side=tk.LEFT, padx=10)

    def running(self):
        """Inicializar la interfaz con menús"""
        if self.is_embedded:
            # Toolbar pegada arriba
            self.toolbar = tk.Frame(self.sub_window, bg="black")
            self.toolbar.grid(row=0, column=0, sticky="ew")

            # Menubuttons en la barra
            btn_freq = tk.Menubutton(
                self.toolbar, text="Gráficos de Frecuencia", font=("Arial", 10)
            )
            menu_freq = tk.Menu(btn_freq, tearoff=False)
            menu_freq.add_command(
                label="Histograma",
                command=lambda: self.histograma(self.principle_frame),
            )
            menu_freq.add_command(
                label="Polígono de Frecuencia",
                command=lambda: self.poligono_frecuencia(self.principle_frame),
            )
            menu_freq.add_command(
                label="Ojiva", command=lambda: self.ojiva(self.principle_frame)
            )
            btn_freq.config(menu=menu_freq)
            btn_freq.pack(side="left", padx=5, pady=2)

            btn_cat = tk.Menubutton(
                self.toolbar, text="Gráficos Categóricos", font=("Arial", 10)
            )
            menu_cat = tk.Menu(btn_cat, tearoff=False)
            menu_cat.add_command(
                label="Gráfico de Barras",
                command=lambda: self.grafico_barras(self.principle_frame),
            )
            menu_cat.add_command(
                label="Gráfico Circular",
                command=lambda: self.grafico_circular(self.principle_frame),
            )
            btn_cat.config(menu=menu_cat)
            btn_cat.pack(side="left", padx=5, pady=2)

            btn_comp = tk.Menubutton(
                self.toolbar, text="Gráficos Comparativos", font=("Arial", 10)
            )
            menu_comp = tk.Menu(btn_comp, tearoff=False)
            menu_comp.add_command(
                label="Diagrama de Caja",
                command=lambda: self.diagrama_caja(self.principle_frame),
            )
            menu_comp.add_command(
                label="Diagrama de Dispersión",
                command=lambda: self.diagrama_dispersion(self.principle_frame),
            )
            btn_comp.config(menu=menu_comp)
            btn_comp.pack(side="left", padx=5, pady=2)

        else:
            # Menú clásico para ventana independiente
            menu_bar = tk.Menu(self.sub_window)
            self.sub_window.configure(menu=menu_bar)

            menu_freq = tk.Menu(menu_bar, tearoff=False)
            menu_bar.add_cascade(label="Gráficos de Frecuencia", menu=menu_freq)
            menu_freq.add_command(
                label="Histograma",
                command=lambda: self.histograma(self.principle_frame),
            )
            menu_freq.add_command(
                label="Polígono de Frecuencia",
                command=lambda: self.poligono_frecuencia(self.principle_frame),
            )
            menu_freq.add_command(
                label="Ojiva", command=lambda: self.ojiva(self.principle_frame)
            )

            menu_cat = tk.Menu(menu_bar, tearoff=False)
            menu_bar.add_cascade(label="Gráficos Categóricos", menu=menu_cat)
            menu_cat.add_command(
                label="Gráfico de Barras",
                command=lambda: self.grafico_barras(self.principle_frame),
            )
            menu_cat.add_command(
                label="Gráfico Circular",
                command=lambda: self.grafico_circular(self.principle_frame),
            )

            menu_comp = tk.Menu(menu_bar, tearoff=False)
            menu_bar.add_cascade(label="Gráficos Comparativos", menu=menu_comp)
            menu_comp.add_command(
                label="Diagrama de Caja",
                command=lambda: self.diagrama_caja(self.principle_frame),
            )
            menu_comp.add_command(
                label="Diagrama de Dispersión",
                command=lambda: self.diagrama_dispersion(self.principle_frame),
            )
