import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class Regression:
    """Clase para análisis de correlación y regresión"""

    def __init__(self, root, tabla_obj, x=0, y=0, width=900, height=700, parent_frame=None):
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
            self.sub_window.title("Correlación y Regresión")
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
                if valor != '-':
                    datos_numericos.append(float(valor))
            except (ValueError, TypeError):
                pass
        return datos_numericos

    def crear_figura_en_frame(self, parent_frame):
        """Crear figura de matplotlib embebida en tkinter"""
        graph_frame = tk.Frame(parent_frame, bg="white")
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, graph_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        return fig, ax, canvas

    def correlacion_simple(self, root):
        """Calcular correlación entre dos variables"""
        self.clear_frame(root)

        # Frame de controles
        control_frame = tk.Frame(root, bg="black")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(control_frame, text="Variable X:", bg="black", fg="white",
                font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)

        columnas = self.tabla_obj.columnas
        var_x_combo = ttk.Combobox(control_frame, values=columnas, state="readonly", width=15)
        if columnas:
            var_x_combo.set(columnas[0])
        var_x_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(control_frame, text="Variable Y:", bg="black", fg="white",
                font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)

        var_y_combo = ttk.Combobox(control_frame, values=columnas, state="readonly", width=15)
        if len(columnas) > 1:
            var_y_combo.set(columnas[1])
        elif columnas:
            var_y_combo.set(columnas[0])
        var_y_combo.grid(row=0, column=3, padx=5, pady=5)

        # Frame para resultados
        resultado_frame = tk.Frame(root, bg="white", relief="sunken", borderwidth=2)
        resultado_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(resultado_frame)
        scrollbar.pack(side="right", fill="y")

        resultado_text = tk.Text(resultado_frame, wrap="word", font=("Courier", 10),
                                yscrollcommand=scrollbar.set)
        resultado_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=resultado_text.yview)

        def calcular():
            try:
                var_x = var_x_combo.get()
                var_y = var_y_combo.get()

                datos_x = np.array(self.obtener_datos_numericos(var_x))
                datos_y = np.array(self.obtener_datos_numericos(var_y))

                if len(datos_x) == 0 or len(datos_y) == 0:
                    messagebox.showerror("Error", "No hay datos numéricos disponibles")
                    return

                # Emparejar datos
                min_len = min(len(datos_x), len(datos_y))
                datos_x = datos_x[:min_len]
                datos_y = datos_y[:min_len]

                if min_len < 3:
                    messagebox.showerror("Error", "Se necesitan al menos 3 pares de datos")
                    return

                # Calcular correlaciones
                pearson_r, pearson_p = stats.pearsonr(datos_x, datos_y)
                spearman_r, spearman_p = stats.spearmanr(datos_x, datos_y)

                # Coeficiente de determinación
                r_squared = pearson_r ** 2

                # Mostrar resultados
                resultado_text.delete(1.0, tk.END)
                resultado_text.insert(tk.END, "=" * 70 + "\n")
                resultado_text.insert(tk.END, "  ANÁLISIS DE CORRELACIÓN\n")
                resultado_text.insert(tk.END, "=" * 70 + "\n\n")

                resultado_text.insert(tk.END, f"Variable X: {var_x}\n")
                resultado_text.insert(tk.END, f"Variable Y: {var_y}\n")
                resultado_text.insert(tk.END, f"Número de pares: {min_len}\n\n")

                resultado_text.insert(tk.END, "--- CORRELACIÓN DE PEARSON (lineal) ---\n")
                resultado_text.insert(tk.END, f"Coeficiente de correlación (r): {pearson_r:.6f}\n")
                resultado_text.insert(tk.END, f"Coeficiente de determinación (r²): {r_squared:.6f}\n")
                resultado_text.insert(tk.END, f"Valor p: {pearson_p:.6f}\n")

                # Interpretación de Pearson
                resultado_text.insert(tk.END, "\nInterpretación:\n")
                if abs(pearson_r) < 0.3:
                    resultado_text.insert(tk.END, "  → Correlación débil\n")
                elif abs(pearson_r) < 0.7:
                    resultado_text.insert(tk.END, "  → Correlación moderada\n")
                else:
                    resultado_text.insert(tk.END, "  → Correlación fuerte\n")

                if pearson_r > 0:
                    resultado_text.insert(tk.END, "  → Correlación positiva (directa)\n")
                elif pearson_r < 0:
                    resultado_text.insert(tk.END, "  → Correlación negativa (inversa)\n")
                else:
                    resultado_text.insert(tk.END, "  → Sin correlación\n")

                if pearson_p < 0.05:
                    resultado_text.insert(tk.END, "  → Estadísticamente significativa (p < 0.05)\n")
                else:
                    resultado_text.insert(tk.END, "  → No significativa (p >= 0.05)\n")

                resultado_text.insert(tk.END, f"\nr² indica que {r_squared*100:.2f}% de la variabilidad en Y\n")
                resultado_text.insert(tk.END, f"es explicada por X.\n\n")

                resultado_text.insert(tk.END, "--- CORRELACIÓN DE SPEARMAN (rangos) ---\n")
                resultado_text.insert(tk.END, f"Coeficiente de correlación (ρ): {spearman_r:.6f}\n")
                resultado_text.insert(tk.END, f"Valor p: {spearman_p:.6f}\n")

                # Interpretación de Spearman
                resultado_text.insert(tk.END, "\nInterpretación:\n")
                if abs(spearman_r) < 0.3:
                    resultado_text.insert(tk.END, "  → Correlación débil\n")
                elif abs(spearman_r) < 0.7:
                    resultado_text.insert(tk.END, "  → Correlación moderada\n")
                else:
                    resultado_text.insert(tk.END, "  → Correlación fuerte\n")

                if spearman_r > 0:
                    resultado_text.insert(tk.END, "  → Relación monótona creciente\n")
                elif spearman_r < 0:
                    resultado_text.insert(tk.END, "  → Relación monótona decreciente\n")

                resultado_text.insert(tk.END, "\n" + "=" * 70 + "\n")

                resultado_text.insert(tk.END, "\nNOTAS:\n")
                resultado_text.insert(tk.END, "• Pearson mide relaciones lineales\n")
                resultado_text.insert(tk.END, "• Spearman mide relaciones monótonas (lineales o no)\n")
                resultado_text.insert(tk.END, "• Si Spearman > Pearson: relación no lineal\n")

            except Exception as e:
                messagebox.showerror("Error", f"Error al calcular correlación: {str(e)}")

        tk.Button(control_frame, text="Calcular Correlación", command=calcular,
                 font=("Arial", 10, "bold"), bg="lightblue").grid(
            row=0, column=4, padx=10, pady=5)

    def regresion_lineal_simple(self, root):
        """Regresión lineal simple Y = a + bX (formato Excel detallado)"""
        self.clear_frame(root)

        # Frame de controles superior
        control_frame = tk.Frame(root, bg="black")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(control_frame, text="Variable X (independiente):", bg="black", fg="white",
                font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)

        columnas = self.tabla_obj.columnas
        var_x_combo = ttk.Combobox(control_frame, values=columnas, state="readonly", width=20)
        if columnas:
            var_x_combo.set(columnas[0])
        var_x_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(control_frame, text="Variable Y (dependiente):", bg="black", fg="white",
                font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)

        var_y_combo = ttk.Combobox(control_frame, values=columnas, state="readonly", width=20)
        if len(columnas) > 1:
            var_y_combo.set(columnas[1])
        elif columnas:
            var_y_combo.set(columnas[0])
        var_y_combo.grid(row=0, column=3, padx=5, pady=5)

        # Frame contenedor principal
        main_container = tk.Frame(root, bg="black")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Frame izquierdo para resultados textuales
        left_frame = tk.Frame(main_container, bg="black")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        resultado_frame = tk.Frame(left_frame, bg="white", relief="sunken", borderwidth=2)
        resultado_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(resultado_frame)
        scrollbar.pack(side="right", fill="y")

        resultado_text = tk.Text(resultado_frame, wrap="none", font=("Courier", 9),
                                yscrollcommand=scrollbar.set)
        resultado_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=resultado_text.yview)

        # Frame derecho para gráfico y predicción
        right_frame = tk.Frame(main_container, bg="black")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Frame para predicción
        pred_frame = tk.LabelFrame(right_frame, text="Predicción", bg="black", fg="white",
                                   font=("Arial", 11, "bold"))
        pred_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(pred_frame, text="Valor de X:", bg="black", fg="white").grid(row=0, column=0, padx=5, pady=5)
        pred_x_entry = tk.Entry(pred_frame, width=15)
        pred_x_entry.grid(row=0, column=1, padx=5, pady=5)

        pred_result_label = tk.Label(pred_frame, text="", bg="black", fg="yellow",
                                     font=("Arial", 10, "bold"))
        pred_result_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # Frame para gráfico
        graph_container = tk.Frame(right_frame, bg="black")
        graph_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        def calcular():
            try:
                var_x = var_x_combo.get()
                var_y = var_y_combo.get()

                datos_x = np.array(self.obtener_datos_numericos(var_x))
                datos_y = np.array(self.obtener_datos_numericos(var_y))

                if len(datos_x) == 0 or len(datos_y) == 0:
                    messagebox.showerror("Error", "No hay datos numéricos disponibles")
                    return

                n = min(len(datos_x), len(datos_y))
                datos_x = datos_x[:n]
                datos_y = datos_y[:n]

                if n < 2:
                    messagebox.showerror("Error", "Se necesitan al menos 2 pares de datos")
                    return

                # Calcular medias
                x_mean = np.mean(datos_x)
                y_mean = np.mean(datos_y)

                # Calcular desviaciones
                dx = datos_x - x_mean
                dy = datos_y - y_mean

                # Calcular cuadrados y productos
                dx2 = dx ** 2
                dy2 = dy ** 2
                dxdy = dx * dy

                # Sumas
                sum_dx2 = np.sum(dx2)
                sum_dy2 = np.sum(dy2)
                sum_dxdy = np.sum(dxdy)

                # Desviaciones estándar
                Sx = np.sqrt(sum_dx2 / (n - 1))
                Sy = np.sqrt(sum_dy2 / (n - 1))

                # Covarianza
                Sxy = sum_dxdy / (n - 1)

                # Coeficiente de correlación de Pearson
                r = Sxy / (Sx * Sy)

                # Coeficientes de regresión
                b = Sxy / (Sx ** 2)  # Pendiente
                a = y_mean - b * x_mean  # Intercepto

                # Predicciones
                y_pred = a + b * datos_x

                # Mostrar resultados
                resultado_text.delete(1.0, tk.END)
                resultado_text.insert(tk.END, "=" * 95 + "\n")
                resultado_text.insert(tk.END, " " * 25 + "REGRESIÓN LINEAL SIMPLE\n")
                resultado_text.insert(tk.END, "=" * 95 + "\n\n")

                resultado_text.insert(tk.END, f"Variable X: {var_x}\n")
                resultado_text.insert(tk.END, f"Variable Y: {var_y}\n\n")

                # Tabla de datos detallada
                resultado_text.insert(tk.END, "TABLA DE DATOS:\n")
                resultado_text.insert(tk.END, "-" * 95 + "\n")
                resultado_text.insert(tk.END, f"{'No':>4s} {'X':>10s} {'Y':>10s} {'dx':>12s} {'dy':>12s} {'dx²':>12s} {'dy²':>14s} {'dx*dy':>14s}\n")
                resultado_text.insert(tk.END, "-" * 95 + "\n")

                for i in range(n):
                    resultado_text.insert(tk.END,
                        f"{i+1:4d} {datos_x[i]:10.2f} {datos_y[i]:10.2f} {dx[i]:12.4f} {dy[i]:12.4f} "
                        f"{dx2[i]:12.4f} {dy2[i]:14.4f} {dxdy[i]:14.4f}\n")

                resultado_text.insert(tk.END, "-" * 95 + "\n")
                resultado_text.insert(tk.END,
                    f"{'Σ':>4s} {np.sum(datos_x):10.2f} {np.sum(datos_y):10.2f} {'':12s} {'':12s} "
                    f"{sum_dx2:12.4f} {sum_dy2:14.4f} {sum_dxdy:14.4f}\n")
                resultado_text.insert(tk.END, "=" * 95 + "\n\n")

                # Estadísticos
                resultado_text.insert(tk.END, "ESTADÍSTICOS BÁSICOS:\n")
                resultado_text.insert(tk.END, "-" * 50 + "\n")
                resultado_text.insert(tk.END, f"  n (tamaño de muestra) = {n}\n")
                resultado_text.insert(tk.END, f"  X̄ (media de X)         = {x_mean:.6f}\n")
                resultado_text.insert(tk.END, f"  Ȳ (media de Y)         = {y_mean:.6f}\n\n")
                resultado_text.insert(tk.END, f"  Sx (desv. estándar X)  = {Sx:.6f}\n")
                resultado_text.insert(tk.END, f"  Sy (desv. estándar Y)  = {Sy:.6f}\n")
                resultado_text.insert(tk.END, f"  Sxy (covarianza)       = {Sxy:.6f}\n")
                resultado_text.insert(tk.END, "-" * 50 + "\n\n")

                # Coeficiente de correlación
                resultado_text.insert(tk.END, "COEFICIENTE DE CORRELACIÓN DE PEARSON:\n")
                resultado_text.insert(tk.END, "-" * 50 + "\n")
                resultado_text.insert(tk.END, f"  r = Sxy / (Sx * Sy)\n")
                resultado_text.insert(tk.END, f"  r = {r:.6f}\n\n")

                # Grado de correlación
                resultado_text.insert(tk.END, "  Grado de correlación:\n")
                if abs(r) >= 0.7:
                    resultado_text.insert(tk.END, "    → Correlación ALTA (|r| ≥ 0.7)\n")
                elif abs(r) > 0.4:
                    resultado_text.insert(tk.END, "    → Correlación MEDIA (0.4 < |r| < 0.7)\n")
                else:
                    resultado_text.insert(tk.END, "    → Correlación BAJA (|r| ≤ 0.4)\n")

                # Forma de la correlación
                resultado_text.insert(tk.END, "\n  Forma de la correlación:\n")
                if r > 0:
                    resultado_text.insert(tk.END, "    → r es POSITIVO: Relación directa\n")
                    resultado_text.insert(tk.END, "      (X aumenta → Y aumenta / X disminuye → Y disminuye)\n")
                elif r < 0:
                    resultado_text.insert(tk.END, "    → r es NEGATIVO: Relación inversa\n")
                    resultado_text.insert(tk.END, "      (X aumenta → Y disminuye / X disminuye → Y aumenta)\n")
                else:
                    resultado_text.insert(tk.END, "    → r = 0: Sin correlación lineal\n")

                resultado_text.insert(tk.END, "-" * 50 + "\n\n")

                # Coeficientes de regresión
                resultado_text.insert(tk.END, "COEFICIENTES DE REGRESIÓN:\n")
                resultado_text.insert(tk.END, "-" * 50 + "\n")
                resultado_text.insert(tk.END, f"  b (pendiente)  = Sxy / Sx²\n")
                resultado_text.insert(tk.END, f"  b = {b:.6f}\n\n")
                resultado_text.insert(tk.END, f"  a (intercepto) = Ȳ - b*X̄\n")
                resultado_text.insert(tk.END, f"  a = {a:.6f}\n")
                resultado_text.insert(tk.END, "-" * 50 + "\n\n")

                # Ecuación de regresión
                resultado_text.insert(tk.END, "ECUACIÓN DE REGRESIÓN LINEAL:\n")
                resultado_text.insert(tk.END, "=" * 50 + "\n")
                if b >= 0:
                    resultado_text.insert(tk.END, f"  Y = {a:.2f} + {b:.2f}X\n")
                else:
                    resultado_text.insert(tk.END, f"  Y = {a:.2f} - {abs(b):.2f}X\n")
                resultado_text.insert(tk.END, "=" * 50 + "\n\n")

                # Interpretación
                resultado_text.insert(tk.END, "INTERPRETACIÓN:\n")
                resultado_text.insert(tk.END, "-" * 50 + "\n")
                if b > 0:
                    resultado_text.insert(tk.END, f"  Por cada unidad que aumenta X,\n")
                    resultado_text.insert(tk.END, f"  Y aumenta {b:.4f} unidades\n")
                else:
                    resultado_text.insert(tk.END, f"  Por cada unidad que aumenta X,\n")
                    resultado_text.insert(tk.END, f"  Y disminuye {abs(b):.4f} unidades\n")

                resultado_text.insert(tk.END, "=" * 95 + "\n")

                # Generar gráfico
                self.clear_frame(graph_container)
                fig, ax, canvas = self.crear_figura_en_frame(graph_container)

                ax.scatter(datos_x, datos_y, color='blue', alpha=0.6, s=60,
                          edgecolors='black', linewidth=1.5, label='Datos observados', zorder=3)
                ax.plot(datos_x, y_pred, color='red', linewidth=2.5,
                       label=f'Y = {a:.2f} + {b:.2f}X', zorder=2)

                ax.set_xlabel(var_x, fontsize=12, fontweight='bold')
                ax.set_ylabel(var_y, fontsize=12, fontweight='bold')
                ax.set_title(f'Regresión Lineal Simple\nr = {r:.4f}',
                           fontsize=13, fontweight='bold')
                ax.legend(fontsize=10)
                ax.grid(True, alpha=0.3, linestyle='--')

                canvas.draw()

                # Función para predicción
                def predecir():
                    try:
                        x_nuevo = float(pred_x_entry.get())
                        y_nuevo = a + b * x_nuevo
                        pred_result_label.config(
                            text=f"Para X = {x_nuevo:.2f}  →  Y = {y_nuevo:.2f}"
                        )
                    except ValueError:
                        pred_result_label.config(text="Ingrese un valor numérico válido")

                # Botón de predicción
                for widget in pred_frame.winfo_children():
                    if isinstance(widget, tk.Button):
                        widget.destroy()

                tk.Button(pred_frame, text="Calcular Y", command=predecir,
                         font=("Arial", 9, "bold"), bg="lightblue").grid(
                    row=0, column=2, padx=5, pady=5)

            except Exception as e:
                messagebox.showerror("Error", f"Error al calcular regresión: {str(e)}")

        tk.Button(control_frame, text="Calcular Regresión Lineal", command=calcular,
                 font=("Arial", 10, "bold"), bg="lightgreen").grid(
            row=0, column=4, padx=10, pady=5)

    def regresion_no_lineal(self, root):
        """Regresión no lineal (exponencial y logarítmica)"""
        self.clear_frame(root)

        # Frame de controles
        control_frame = tk.Frame(root, bg="black")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(control_frame, text="Variable X:", bg="black", fg="white",
                font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        columnas = self.tabla_obj.columnas
        var_x_combo = ttk.Combobox(control_frame, values=columnas, state="readonly", width=15)
        if columnas:
            var_x_combo.set(columnas[0])
        var_x_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(control_frame, text="Variable Y:", bg="black", fg="white",
                font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="e")

        var_y_combo = ttk.Combobox(control_frame, values=columnas, state="readonly", width=15)
        if len(columnas) > 1:
            var_y_combo.set(columnas[1])
        elif columnas:
            var_y_combo.set(columnas[0])
        var_y_combo.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(control_frame, text="Tipo:", bg="black", fg="white",
                font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5, pady=5, sticky="e")

        tipo_combo = ttk.Combobox(control_frame, values=["Exponencial", "Logarítmica"],
                                 state="readonly", width=15)
        tipo_combo.set("Exponencial")
        tipo_combo.grid(row=0, column=5, padx=5, pady=5)

        # Frame contenedor
        content_frame = tk.Frame(root, bg="black")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Frame para resultados
        resultado_frame = tk.Frame(content_frame, bg="white", relief="sunken", borderwidth=2)
        resultado_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        scrollbar = tk.Scrollbar(resultado_frame)
        scrollbar.pack(side="right", fill="y")

        resultado_text = tk.Text(resultado_frame, wrap="word", font=("Courier", 9),
                                yscrollcommand=scrollbar.set, width=40)
        resultado_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=resultado_text.yview)

        # Frame para gráfico
        graph_container = tk.Frame(content_frame, bg="black")
        graph_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        def calcular():
            try:
                var_x = var_x_combo.get()
                var_y = var_y_combo.get()
                tipo = tipo_combo.get()

                datos_x = np.array(self.obtener_datos_numericos(var_x))
                datos_y = np.array(self.obtener_datos_numericos(var_y))

                if len(datos_x) == 0 or len(datos_y) == 0:
                    messagebox.showerror("Error", "No hay datos numéricos disponibles")
                    return

                min_len = min(len(datos_x), len(datos_y))
                datos_x = datos_x[:min_len]
                datos_y = datos_y[:min_len]

                if min_len < 3:
                    messagebox.showerror("Error", "Se necesitan al menos 3 pares de datos")
                    return

                # Verificar valores positivos según el tipo
                if tipo == "Exponencial":
                    if np.any(datos_y <= 0):
                        messagebox.showerror("Error",
                            "Para regresión exponencial, Y debe ser positivo")
                        return
                    # Y = a * e^(b*X) -> ln(Y) = ln(a) + b*X
                    y_transform = np.log(datos_y)
                    slope, intercept, r_value, p_value, std_err = stats.linregress(datos_x, y_transform)
                    a = np.exp(intercept)
                    b = slope
                    y_pred = a * np.exp(b * datos_x)
                    ecuacion = f"Y = {a:.6f} * e^({b:.6f}X)"

                else:  # Logarítmica
                    if np.any(datos_x <= 0):
                        messagebox.showerror("Error",
                            "Para regresión logarítmica, X debe ser positivo")
                        return
                    # Y = a + b*ln(X)
                    x_transform = np.log(datos_x)
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x_transform, datos_y)
                    a = intercept
                    b = slope
                    y_pred = a + b * np.log(datos_x)
                    ecuacion = f"Y = {a:.6f} + {b:.6f}*ln(X)"

                r_squared = r_value ** 2
                residuos = datos_y - y_pred
                sse = np.sum(residuos ** 2)
                mse = sse / len(datos_y)
                rmse = np.sqrt(mse)

                # Mostrar resultados
                resultado_text.delete(1.0, tk.END)
                resultado_text.insert(tk.END, "=" * 50 + "\n")
                resultado_text.insert(tk.END, f" REGRESIÓN {tipo.upper()}\n")
                resultado_text.insert(tk.END, "=" * 50 + "\n\n")

                resultado_text.insert(tk.END, f"Variable X: {var_x}\n")
                resultado_text.insert(tk.END, f"Variable Y: {var_y}\n")
                resultado_text.insert(tk.END, f"Observaciones: {min_len}\n\n")

                resultado_text.insert(tk.END, "--- ECUACIÓN ---\n")
                resultado_text.insert(tk.END, f"{ecuacion}\n\n")

                if tipo == "Exponencial":
                    resultado_text.insert(tk.END, f"Parámetro a: {a:.6f}\n")
                    resultado_text.insert(tk.END, f"Parámetro b: {b:.6f}\n\n")
                else:
                    resultado_text.insert(tk.END, f"Intercepto a: {a:.6f}\n")
                    resultado_text.insert(tk.END, f"Pendiente b: {b:.6f}\n\n")

                resultado_text.insert(tk.END, "--- BONDAD DE AJUSTE ---\n")
                resultado_text.insert(tk.END, f"r²: {r_squared:.6f}\n")
                resultado_text.insert(tk.END, f"RMSE: {rmse:.6f}\n")
                resultado_text.insert(tk.END, f"Valor p: {p_value:.6f}\n\n")

                resultado_text.insert(tk.END, f"El modelo explica\n")
                resultado_text.insert(tk.END, f"{r_squared*100:.2f}% de la\n")
                resultado_text.insert(tk.END, f"variabilidad en Y\n")

                # Generar gráfico
                self.clear_frame(graph_container)
                fig, ax, canvas = self.crear_figura_en_frame(graph_container)

                # Ordenar para graficar la curva correctamente
                sort_idx = np.argsort(datos_x)
                x_sorted = datos_x[sort_idx]
                y_pred_sorted = y_pred[sort_idx]

                ax.scatter(datos_x, datos_y, color='blue', alpha=0.6, s=50,
                          edgecolors='black', label='Datos observados')
                ax.plot(x_sorted, y_pred_sorted, color='red', linewidth=2,
                       label=f'Regresión {tipo}')

                ax.set_xlabel(var_x, fontsize=12)
                ax.set_ylabel(var_y, fontsize=12)
                ax.set_title(f'Regresión {tipo}\nr² = {r_squared:.4f}',
                           fontsize=14, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)

                canvas.draw()

            except Exception as e:
                messagebox.showerror("Error", f"Error: {str(e)}")

        tk.Button(control_frame, text="Calcular Regresión", command=calcular,
                 font=("Arial", 10, "bold"), bg="lightgreen").grid(
            row=0, column=6, padx=10, pady=5)

    def regresion_multiple(self, root):
        """Regresión lineal múltiple"""
        self.clear_frame(root)

        # Frame de controles
        control_frame = tk.Frame(root, bg="black")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(control_frame, text="Variable Y (dependiente):", bg="black",
                font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        columnas = self.tabla_obj.columnas
        var_y_combo = ttk.Combobox(control_frame, values=columnas, state="readonly", width=15)
        if columnas:
            var_y_combo.set(columnas[0])
        var_y_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(control_frame, text="Variables X (independientes):", bg="black",
                font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="ne")

        # Listbox para selección múltiple
        listbox_frame = tk.Frame(control_frame, bg="black")
        listbox_frame.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, height=5,
                            yscrollcommand=scrollbar.set, width=20)
        for col in columnas:
            listbox.insert(tk.END, col)
        listbox.pack(side=tk.LEFT)
        scrollbar.config(command=listbox.yview)

        # Frame para resultados
        resultado_frame = tk.Frame(root, bg="white", relief="sunken", borderwidth=2)
        resultado_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar_res = tk.Scrollbar(resultado_frame)
        scrollbar_res.pack(side="right", fill="y")

        resultado_text = tk.Text(resultado_frame, wrap="word", font=("Courier", 9),
                                yscrollcommand=scrollbar_res.set)
        resultado_text.pack(side="left", fill="both", expand=True)
        scrollbar_res.config(command=resultado_text.yview)

        def calcular():
            try:
                var_y = var_y_combo.get()
                indices_x = listbox.curselection()

                if not indices_x:
                    messagebox.showwarning("Advertencia",
                        "Selecciona al menos una variable independiente")
                    return

                vars_x = [columnas[i] for i in indices_x]

                # Obtener datos Y
                datos_y = np.array(self.obtener_datos_numericos(var_y))

                if len(datos_y) == 0:
                    messagebox.showerror("Error", "No hay datos numéricos en Y")
                    return

                # Obtener datos X (matriz)
                datos_x_list = []
                for var_x in vars_x:
                    datos_x_var = self.obtener_datos_numericos(var_x)
                    if len(datos_x_var) == 0:
                        messagebox.showerror("Error", f"No hay datos en {var_x}")
                        return
                    datos_x_list.append(datos_x_var)

                # Encontrar longitud mínima
                min_len = min(len(datos_y), *[len(dx) for dx in datos_x_list])

                if min_len < len(vars_x) + 2:
                    messagebox.showerror("Error",
                        f"Se necesitan al menos {len(vars_x) + 2} observaciones")
                    return

                # Construir matriz X
                datos_y = datos_y[:min_len]
                X = np.column_stack([dx[:min_len] for dx in datos_x_list])

                # Agregar columna de unos para el intercepto
                X_con_intercepto = np.column_stack([np.ones(min_len), X])

                # Calcular coeficientes usando mínimos cuadrados
                # β = (X'X)^(-1) X'Y
                XtX = X_con_intercepto.T @ X_con_intercepto
                XtY = X_con_intercepto.T @ datos_y
                coeficientes = np.linalg.solve(XtX, XtY)

                intercepto = coeficientes[0]
                betas = coeficientes[1:]

                # Predicciones
                y_pred = X_con_intercepto @ coeficientes

                # Métricas
                residuos = datos_y - y_pred
                sse = np.sum(residuos ** 2)
                sst = np.sum((datos_y - np.mean(datos_y)) ** 2)
                r_squared = 1 - (sse / sst)

                # R² ajustado
                n = len(datos_y)
                k = len(vars_x)
                r_squared_adj = 1 - ((1 - r_squared) * (n - 1) / (n - k - 1))

                mse = sse / (n - k - 1)
                rmse = np.sqrt(mse)

                # Mostrar resultados
                resultado_text.delete(1.0, tk.END)
                resultado_text.insert(tk.END, "=" * 70 + "\n")
                resultado_text.insert(tk.END, "  REGRESIÓN LINEAL MÚLTIPLE\n")
                resultado_text.insert(tk.END, "=" * 70 + "\n\n")

                resultado_text.insert(tk.END, f"Variable dependiente (Y): {var_y}\n")
                resultado_text.insert(tk.END, f"Variables independientes (X): {', '.join(vars_x)}\n")
                resultado_text.insert(tk.END, f"Número de observaciones: {n}\n")
                resultado_text.insert(tk.END, f"Número de variables: {k}\n\n")

                resultado_text.insert(tk.END, "--- ECUACIÓN DE REGRESIÓN ---\n")
                ecuacion = f"Y = {intercepto:.6f}"
                for i, var in enumerate(vars_x):
                    signo = "+" if betas[i] >= 0 else ""
                    ecuacion += f" {signo} {betas[i]:.6f}*{var}"
                resultado_text.insert(tk.END, f"{ecuacion}\n\n")

                resultado_text.insert(tk.END, "--- COEFICIENTES ---\n")
                resultado_text.insert(tk.END, f"Intercepto (β₀): {intercepto:.6f}\n")
                for i, var in enumerate(vars_x):
                    resultado_text.insert(tk.END, f"β{i+1} ({var}): {betas[i]:.6f}\n")
                resultado_text.insert(tk.END, "\n")

                resultado_text.insert(tk.END, "--- BONDAD DE AJUSTE ---\n")
                resultado_text.insert(tk.END, f"R² (coef. determinación): {r_squared:.6f}\n")
                resultado_text.insert(tk.END, f"R² ajustado: {r_squared_adj:.6f}\n")
                resultado_text.insert(tk.END, f"RMSE: {rmse:.6f}\n")
                resultado_text.insert(tk.END, f"MSE: {mse:.6f}\n\n")

                resultado_text.insert(tk.END, f"El modelo explica {r_squared*100:.2f}% de la\n")
                resultado_text.insert(tk.END, f"variabilidad en {var_y}\n\n")

                resultado_text.insert(tk.END, "--- INTERPRETACIÓN ---\n")
                for i, var in enumerate(vars_x):
                    resultado_text.insert(tk.END, f"\n• {var}:\n")
                    if betas[i] > 0:
                        resultado_text.insert(tk.END, f"  Por cada unidad que aumenta {var},\n")
                        resultado_text.insert(tk.END, f"  {var_y} aumenta {betas[i]:.4f} unidades\n")
                        resultado_text.insert(tk.END, f"  (manteniendo otras variables constantes)\n")
                    else:
                        resultado_text.insert(tk.END, f"  Por cada unidad que aumenta {var},\n")
                        resultado_text.insert(tk.END, f"  {var_y} disminuye {abs(betas[i]):.4f} unidades\n")
                        resultado_text.insert(tk.END, f"  (manteniendo otras variables constantes)\n")

                resultado_text.insert(tk.END, "\n" + "=" * 70 + "\n")

            except np.linalg.LinAlgError:
                messagebox.showerror("Error",
                    "Error en el cálculo. Puede haber multicolinealidad.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al calcular regresión: {str(e)}")

        tk.Button(control_frame, text="Calcular Regresión Múltiple", command=calcular,
                 font=("Arial", 10, "bold"), bg="lightgreen").grid(
            row=0, column=2, padx=10, pady=5, rowspan=2)

    def running(self):
        """Inicializar la interfaz con menús"""
        if self.is_embedded:
            # Toolbar pegada arriba
            self.toolbar = tk.Frame(self.sub_window, bg="black")
            self.toolbar.grid(row=0, column=0, sticky="ew")

            # Menubuttons en la barra
            btn_corr = tk.Menubutton(self.toolbar, text="Correlación", font=("Arial", 10))
            menu_corr = tk.Menu(btn_corr, tearoff=False)
            menu_corr.add_command(label="Análisis de Correlación",
                                 command=lambda: self.correlacion_simple(self.principle_frame))
            btn_corr.config(menu=menu_corr)
            btn_corr.pack(side="left", padx=5, pady=2)

            btn_reg_simple = tk.Menubutton(self.toolbar, text="Regresión Simple",
                                          font=("Arial", 10))
            menu_reg_simple = tk.Menu(btn_reg_simple, tearoff=False)
            menu_reg_simple.add_command(label="Regresión Lineal",
                                       command=lambda: self.regresion_lineal_simple(self.principle_frame))
            menu_reg_simple.add_command(label="Regresión No Lineal",
                                       command=lambda: self.regresion_no_lineal(self.principle_frame))
            btn_reg_simple.config(menu=menu_reg_simple)
            btn_reg_simple.pack(side="left", padx=5, pady=2)

            btn_reg_multiple = tk.Menubutton(self.toolbar, text="Regresión Múltiple",
                                            font=("Arial", 10))
            menu_reg_multiple = tk.Menu(btn_reg_multiple, tearoff=False)
            menu_reg_multiple.add_command(label="Regresión Lineal Múltiple",
                                         command=lambda: self.regresion_multiple(self.principle_frame))
            btn_reg_multiple.config(menu=menu_reg_multiple)
            btn_reg_multiple.pack(side="left", padx=5, pady=2)

        else:
            # Menú clásico para ventana independiente
            menu_bar = tk.Menu(self.sub_window)
            self.sub_window.configure(menu=menu_bar)

            menu_corr = tk.Menu(menu_bar, tearoff=False)
            menu_bar.add_cascade(label="Correlación", menu=menu_corr)
            menu_corr.add_command(label="Análisis de Correlación",
                                 command=lambda: self.correlacion_simple(self.principle_frame))

            menu_reg_simple = tk.Menu(menu_bar, tearoff=False)
            menu_bar.add_cascade(label="Regresión Simple", menu=menu_reg_simple)
            menu_reg_simple.add_command(label="Regresión Lineal",
                                       command=lambda: self.regresion_lineal_simple(self.principle_frame))
            menu_reg_simple.add_command(label="Regresión No Lineal",
                                       command=lambda: self.regresion_no_lineal(self.principle_frame))

            menu_reg_multiple = tk.Menu(menu_bar, tearoff=False)
            menu_bar.add_cascade(label="Regresión Múltiple", menu=menu_reg_multiple)
            menu_reg_multiple.add_command(label="Regresión Lineal Múltiple",
                                         command=lambda: self.regresion_multiple(self.principle_frame))
