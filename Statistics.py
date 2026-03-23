import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from scipy import stats
import pandas as pd


class Statistics:
    """Clase para calcular y mostrar medidas de dispersión y forma"""

    def __init__(self, root, tabla_obj, x=0, y=0, width=600, height=400, parent_frame=None):
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
            self.sub_window.title("Estadísticas Avanzadas")
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

    def calcular_medidas_dispersion(self, datos):
        """Calcular medidas de dispersión"""
        datos_array = np.array(datos, dtype=float)
        n = len(datos_array)

        # Medidas básicas
        media = np.mean(datos_array)
        varianza_poblacional = np.var(datos_array, ddof=0)
        varianza_muestral = np.var(datos_array, ddof=1)
        desv_est_poblacional = np.std(datos_array, ddof=0)
        desv_est_muestral = np.std(datos_array, ddof=1)
        rango = np.max(datos_array) - np.min(datos_array)

        # Cuartiles y rango intercuartílico
        q1 = np.percentile(datos_array, 25)
        q3 = np.percentile(datos_array, 75)
        rango_intercuartilico = q3 - q1

        # Coeficiente de variación
        cv = (desv_est_muestral / media * 100) if media != 0 else 0

        return {
            'n': n,
            'media': media,
            'varianza_poblacional': varianza_poblacional,
            'varianza_muestral': varianza_muestral,
            'desv_est_poblacional': desv_est_poblacional,
            'desv_est_muestral': desv_est_muestral,
            'rango': rango,
            'minimo': np.min(datos_array),
            'maximo': np.max(datos_array),
            'q1': q1,
            'q3': q3,
            'rango_intercuartilico': rango_intercuartilico,
            'cv': cv
        }

    def calcular_medidas_forma(self, datos):
        """Calcular medidas de forma (asimetría y curtosis)"""
        datos_array = np.array(datos, dtype=float)

        # Asimetría (skewness)
        asimetria = stats.skew(datos_array, bias=False)

        # Curtosis (kurtosis) - usando el método de Fisher (exceso de curtosis)
        curtosis = stats.kurtosis(datos_array, bias=False)

        # Interpretación de asimetría
        if abs(asimetria) < 0.5:
            interpretacion_asimetria = "Aproximadamente simétrica"
        elif asimetria > 0:
            interpretacion_asimetria = "Asimétrica positiva (cola derecha)"
        else:
            interpretacion_asimetria = "Asimétrica negativa (cola izquierda)"

        # Interpretación de curtosis
        if abs(curtosis) < 0.5:
            interpretacion_curtosis = "Mesocúrtica (normal)"
        elif curtosis > 0:
            interpretacion_curtosis = "Leptocúrtica (más puntiaguda)"
        else:
            interpretacion_curtosis = "Platicúrtica (más achatada)"

        return {
            'asimetria': asimetria,
            'curtosis': curtosis,
            'interpretacion_asimetria': interpretacion_asimetria,
            'interpretacion_curtosis': interpretacion_curtosis
        }

    def mostrar_medidas_dispersion(self, root):
        """Mostrar interfaz para calcular medidas de dispersión"""
        self.clear_frame(root)

        lf = tk.LabelFrame(root, text="Medidas de Dispersión", bg="black", fg="white",
                          font=("Arial", 12, "bold"))
        lf.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        lf.rowconfigure(2, weight=1)
        lf.columnconfigure(0, weight=1)

        # Selector de variable
        tk.Label(lf, text="Seleccionar variable:", bg="black", fg="white",
                font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)

        columnas = self.tabla_obj.columnas
        variable_combo = ttk.Combobox(lf, values=columnas, state="readonly", width=30)
        if columnas:
            variable_combo.set(columnas[0])
        variable_combo.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Frame para resultados
        resultado_frame = tk.Frame(lf, bg="white", relief="sunken", borderwidth=2)
        resultado_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        lf.rowconfigure(2, weight=1)
        resultado_frame.columnconfigure(0, weight=1)

        # Scrollbar para resultados
        scrollbar = tk.Scrollbar(resultado_frame)
        scrollbar.pack(side="right", fill="y")

        resultado_text = tk.Text(resultado_frame, wrap="word", font=("Courier", 10),
                                yscrollcommand=scrollbar.set, bg="white")
        resultado_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=resultado_text.yview)

        def calcular():
            try:
                variable = variable_combo.get()
                datos = self.tabla_obj.obtener_columna(variable)

                # Filtrar valores no numéricos
                datos_numericos = []
                for valor in datos:
                    try:
                        if valor != '-':
                            datos_numericos.append(float(valor))
                    except (ValueError, TypeError):
                        pass

                if len(datos_numericos) < 2:
                    messagebox.showerror("Error", "Se necesitan al menos 2 valores numéricos")
                    return

                # Calcular medidas
                medidas = self.calcular_medidas_dispersion(datos_numericos)

                # Mostrar resultados
                resultado_text.delete(1.0, tk.END)
                resultado_text.insert(tk.END, "=" * 60 + "\n")
                resultado_text.insert(tk.END, "  MEDIDAS DE DISPERSIÓN\n")
                resultado_text.insert(tk.END, "=" * 60 + "\n\n")

                resultado_text.insert(tk.END, f"Variable: {variable}\n")
                resultado_text.insert(tk.END, f"Tamaño de la muestra (n): {medidas['n']}\n\n")

                resultado_text.insert(tk.END, "--- Medidas de Tendencia Central ---\n")
                resultado_text.insert(tk.END, f"Media: {medidas['media']:.4f}\n\n")

                resultado_text.insert(tk.END, "--- Medidas de Dispersión Absoluta ---\n")
                resultado_text.insert(tk.END, f"Rango: {medidas['rango']:.4f}\n")
                resultado_text.insert(tk.END, f"  Mínimo: {medidas['minimo']:.4f}\n")
                resultado_text.insert(tk.END, f"  Máximo: {medidas['maximo']:.4f}\n\n")

                resultado_text.insert(tk.END, f"Rango Intercuartílico (IQR): {medidas['rango_intercuartilico']:.4f}\n")
                resultado_text.insert(tk.END, f"  Q1 (percentil 25): {medidas['q1']:.4f}\n")
                resultado_text.insert(tk.END, f"  Q3 (percentil 75): {medidas['q3']:.4f}\n\n")

                resultado_text.insert(tk.END, "--- Varianza ---\n")
                resultado_text.insert(tk.END, f"Varianza Poblacional (σ²): {medidas['varianza_poblacional']:.4f}\n")
                resultado_text.insert(tk.END, f"Varianza Muestral (s²): {medidas['varianza_muestral']:.4f}\n\n")

                resultado_text.insert(tk.END, "--- Desviación Estándar ---\n")
                resultado_text.insert(tk.END, f"Desviación Estándar Poblacional (σ): {medidas['desv_est_poblacional']:.4f}\n")
                resultado_text.insert(tk.END, f"Desviación Estándar Muestral (s): {medidas['desv_est_muestral']:.4f}\n\n")

                resultado_text.insert(tk.END, "--- Medidas de Dispersión Relativa ---\n")
                resultado_text.insert(tk.END, f"Coeficiente de Variación (CV): {medidas['cv']:.2f}%\n\n")

                # Interpretación del CV
                resultado_text.insert(tk.END, "Interpretación del CV:\n")
                if medidas['cv'] < 15:
                    resultado_text.insert(tk.END, "  → Baja dispersión (datos homogéneos)\n")
                elif medidas['cv'] < 30:
                    resultado_text.insert(tk.END, "  → Dispersión moderada\n")
                else:
                    resultado_text.insert(tk.END, "  → Alta dispersión (datos heterogéneos)\n")

                resultado_text.insert(tk.END, "\n" + "=" * 60 + "\n")

            except Exception as e:
                messagebox.showerror("Error", f"Error al calcular medidas: {str(e)}")

        # Botón calcular
        tk.Button(lf, text="Calcular Medidas de Dispersión", command=calcular,
                 font=("Arial", 10, "bold"), bg="lightblue").grid(
            row=1, column=0, columnspan=2, pady=10)

    def mostrar_medidas_forma(self, root):
        """Mostrar interfaz para calcular medidas de forma"""
        self.clear_frame(root)

        lf = tk.LabelFrame(root, text="Medidas de Forma", bg="black", fg="white",
                          font=("Arial", 12, "bold"))
        lf.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        lf.rowconfigure(2, weight=1)
        lf.columnconfigure(0, weight=1)

        # Selector de variable
        tk.Label(lf, text="Seleccionar variable:", bg="black", fg="white",
                font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)

        columnas = self.tabla_obj.columnas
        variable_combo = ttk.Combobox(lf, values=columnas, state="readonly", width=30)
        if columnas:
            variable_combo.set(columnas[0])
        variable_combo.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Frame para resultados
        resultado_frame = tk.Frame(lf, bg="white", relief="sunken", borderwidth=2)
        resultado_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        lf.rowconfigure(2, weight=1)
        resultado_frame.columnconfigure(0, weight=1)

        # Scrollbar para resultados
        scrollbar = tk.Scrollbar(resultado_frame)
        scrollbar.pack(side="right", fill="y")

        resultado_text = tk.Text(resultado_frame, wrap="word", font=("Courier", 10),
                                yscrollcommand=scrollbar.set, bg="white")
        resultado_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=resultado_text.yview)

        def calcular():
            try:
                variable = variable_combo.get()
                datos = self.tabla_obj.obtener_columna(variable)

                # Filtrar valores no numéricos
                datos_numericos = []
                for valor in datos:
                    try:
                        if valor != '-':
                            datos_numericos.append(float(valor))
                    except (ValueError, TypeError):
                        pass

                if len(datos_numericos) < 3:
                    messagebox.showerror("Error", "Se necesitan al menos 3 valores numéricos")
                    return

                # Calcular medidas de forma
                medidas_forma = self.calcular_medidas_forma(datos_numericos)
                medidas_dispersion = self.calcular_medidas_dispersion(datos_numericos)

                # Mostrar resultados
                resultado_text.delete(1.0, tk.END)
                resultado_text.insert(tk.END, "=" * 60 + "\n")
                resultado_text.insert(tk.END, "  MEDIDAS DE FORMA\n")
                resultado_text.insert(tk.END, "=" * 60 + "\n\n")

                resultado_text.insert(tk.END, f"Variable: {variable}\n")
                resultado_text.insert(tk.END, f"Tamaño de la muestra (n): {medidas_dispersion['n']}\n\n")

                resultado_text.insert(tk.END, "--- ASIMETRÍA (SKEWNESS) ---\n")
                resultado_text.insert(tk.END, f"Coeficiente de Asimetría: {medidas_forma['asimetria']:.4f}\n")
                resultado_text.insert(tk.END, f"Interpretación: {medidas_forma['interpretacion_asimetria']}\n\n")

                resultado_text.insert(tk.END, "Significado:\n")
                if medidas_forma['asimetria'] > 0:
                    resultado_text.insert(tk.END, "  → La distribución tiene cola más larga a la derecha\n")
                    resultado_text.insert(tk.END, "  → La media es mayor que la mediana\n")
                    resultado_text.insert(tk.END, "  → Hay valores extremos altos\n")
                elif medidas_forma['asimetria'] < 0:
                    resultado_text.insert(tk.END, "  → La distribución tiene cola más larga a la izquierda\n")
                    resultado_text.insert(tk.END, "  → La media es menor que la mediana\n")
                    resultado_text.insert(tk.END, "  → Hay valores extremos bajos\n")
                else:
                    resultado_text.insert(tk.END, "  → La distribución es simétrica\n")
                    resultado_text.insert(tk.END, "  → La media y mediana son similares\n")

                resultado_text.insert(tk.END, "\n--- CURTOSIS (KURTOSIS) ---\n")
                resultado_text.insert(tk.END, f"Coeficiente de Curtosis: {medidas_forma['curtosis']:.4f}\n")
                resultado_text.insert(tk.END, f"Interpretación: {medidas_forma['interpretacion_curtosis']}\n\n")

                resultado_text.insert(tk.END, "Significado:\n")
                if medidas_forma['curtosis'] > 0:
                    resultado_text.insert(tk.END, "  → La distribución es más puntiaguda que la normal\n")
                    resultado_text.insert(tk.END, "  → Mayor concentración de datos en el centro\n")
                    resultado_text.insert(tk.END, "  → Colas más pesadas (mayor probabilidad de valores extremos)\n")
                elif medidas_forma['curtosis'] < 0:
                    resultado_text.insert(tk.END, "  → La distribución es más achatada que la normal\n")
                    resultado_text.insert(tk.END, "  → Menor concentración de datos en el centro\n")
                    resultado_text.insert(tk.END, "  → Colas más ligeras (menor probabilidad de valores extremos)\n")
                else:
                    resultado_text.insert(tk.END, "  → La distribución tiene forma similar a la normal\n")

                resultado_text.insert(tk.END, "\n" + "=" * 60 + "\n")
                resultado_text.insert(tk.END, "\nNOTA: La curtosis se calcula como exceso respecto a la\n")
                resultado_text.insert(tk.END, "distribución normal (valor 0 = distribución normal)\n")

            except Exception as e:
                messagebox.showerror("Error", f"Error al calcular medidas: {str(e)}")

        # Botón calcular
        tk.Button(lf, text="Calcular Medidas de Forma", command=calcular,
                 font=("Arial", 10, "bold"), bg="lightblue").grid(
            row=1, column=0, columnspan=2, pady=10)

    def mostrar_resumen_completo(self, root):
        """Mostrar resumen completo con todas las medidas"""
        self.clear_frame(root)

        lf = tk.LabelFrame(root, text="Resumen Estadístico Completo", bg="black", fg="white",
                          font=("Arial", 12, "bold"))
        lf.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)
        lf.rowconfigure(2, weight=1)
        lf.columnconfigure(0, weight=1)

        # Selector de variable
        tk.Label(lf, text="Seleccionar variable:", bg="black", fg="white",
                font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)

        columnas = self.tabla_obj.columnas
        variable_combo = ttk.Combobox(lf, values=columnas, state="readonly", width=30)
        if columnas:
            variable_combo.set(columnas[0])
        variable_combo.grid(row=0, column=1, sticky="w", padx=10, pady=5)

        # Frame para resultados
        resultado_frame = tk.Frame(lf, bg="white", relief="sunken", borderwidth=2)
        resultado_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        lf.rowconfigure(2, weight=1)
        resultado_frame.columnconfigure(0, weight=1)

        # Scrollbar para resultados
        scrollbar = tk.Scrollbar(resultado_frame)
        scrollbar.pack(side="right", fill="y")

        resultado_text = tk.Text(resultado_frame, wrap="word", font=("Courier", 10),
                                yscrollcommand=scrollbar.set, bg="white")
        resultado_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=resultado_text.yview)

        def calcular():
            try:
                variable = variable_combo.get()
                datos = self.tabla_obj.obtener_columna(variable)

                # Filtrar valores no numéricos
                datos_numericos = []
                for valor in datos:
                    try:
                        if valor != '-':
                            datos_numericos.append(float(valor))
                    except (ValueError, TypeError):
                        pass

                if len(datos_numericos) < 3:
                    messagebox.showerror("Error", "Se necesitan al menos 3 valores numéricos")
                    return

                # Calcular todas las medidas
                medidas_disp = self.calcular_medidas_dispersion(datos_numericos)
                medidas_forma = self.calcular_medidas_forma(datos_numericos)

                # Mostrar resultados completos
                resultado_text.delete(1.0, tk.END)
                resultado_text.insert(tk.END, "╔" + "═" * 58 + "╗\n")
                resultado_text.insert(tk.END, "║" + " " * 15 + "RESUMEN ESTADÍSTICO COMPLETO" + " " * 15 + "║\n")
                resultado_text.insert(tk.END, "╚" + "═" * 58 + "╝\n\n")

                resultado_text.insert(tk.END, f"Variable: {variable}\n")
                resultado_text.insert(tk.END, f"Tamaño de muestra: {medidas_disp['n']} observaciones\n\n")

                resultado_text.insert(tk.END, "┌─ MEDIDAS DE TENDENCIA CENTRAL ─────────────────────┐\n")
                resultado_text.insert(tk.END, f"│ Media:                    {medidas_disp['media']:>20.4f} │\n")
                resultado_text.insert(tk.END, "└────────────────────────────────────────────────────┘\n\n")

                resultado_text.insert(tk.END, "┌─ MEDIDAS DE DISPERSIÓN ────────────────────────────┐\n")
                resultado_text.insert(tk.END, f"│ Rango:                    {medidas_disp['rango']:>20.4f} │\n")
                resultado_text.insert(tk.END, f"│   • Mínimo:               {medidas_disp['minimo']:>20.4f} │\n")
                resultado_text.insert(tk.END, f"│   • Máximo:               {medidas_disp['maximo']:>20.4f} │\n")
                resultado_text.insert(tk.END, f"│                                                    │\n")
                resultado_text.insert(tk.END, f"│ Rango Intercuartílico:    {medidas_disp['rango_intercuartilico']:>20.4f} │\n")
                resultado_text.insert(tk.END, f"│   • Q1:                   {medidas_disp['q1']:>20.4f} │\n")
                resultado_text.insert(tk.END, f"│   • Q3:                   {medidas_disp['q3']:>20.4f} │\n")
                resultado_text.insert(tk.END, f"│                                                    │\n")
                resultado_text.insert(tk.END, f"│ Varianza (s²):            {medidas_disp['varianza_muestral']:>20.4f} │\n")
                resultado_text.insert(tk.END, f"│ Desv. Estándar (s):       {medidas_disp['desv_est_muestral']:>20.4f} │\n")
                resultado_text.insert(tk.END, f"│ Coef. de Variación:       {medidas_disp['cv']:>19.2f}% │\n")
                resultado_text.insert(tk.END, "└────────────────────────────────────────────────────┘\n\n")

                resultado_text.insert(tk.END, "┌─ MEDIDAS DE FORMA ─────────────────────────────────┐\n")
                resultado_text.insert(tk.END, f"│ Asimetría:                {medidas_forma['asimetria']:>20.4f} │\n")
                resultado_text.insert(tk.END, f"│   → {medidas_forma['interpretacion_asimetria']:<45} │\n")
                resultado_text.insert(tk.END, f"│                                                    │\n")
                resultado_text.insert(tk.END, f"│ Curtosis:                 {medidas_forma['curtosis']:>20.4f} │\n")
                resultado_text.insert(tk.END, f"│   → {medidas_forma['interpretacion_curtosis']:<45} │\n")
                resultado_text.insert(tk.END, "└────────────────────────────────────────────────────┘\n")

            except Exception as e:
                messagebox.showerror("Error", f"Error al calcular resumen: {str(e)}")

        # Botón calcular
        tk.Button(lf, text="Generar Resumen Completo", command=calcular,
                 font=("Arial", 10, "bold"), bg="lightgreen").grid(
            row=1, column=0, columnspan=2, pady=10)

    def running(self):
        """Inicializar la interfaz con menús"""
        if self.is_embedded:
            # Toolbar pegada arriba
            self.toolbar = tk.Frame(self.sub_window, bg="black")
            self.toolbar.grid(row=0, column=0, sticky="ew")

            # Menubuttons en la barra
            btn_dispersion = tk.Menubutton(self.toolbar, text="Medidas de Dispersión",
                                          font=("Arial", 10))
            menu_dispersion = tk.Menu(btn_dispersion, tearoff=False)
            menu_dispersion.add_command(label="Calcular Dispersión",
                                       command=lambda: self.mostrar_medidas_dispersion(self.principle_frame))
            btn_dispersion.config(menu=menu_dispersion)
            btn_dispersion.pack(side="left", padx=5, pady=2)

            btn_forma = tk.Menubutton(self.toolbar, text="Medidas de Forma",
                                     font=("Arial", 10))
            menu_forma = tk.Menu(btn_forma, tearoff=False)
            menu_forma.add_command(label="Calcular Asimetría y Curtosis",
                                  command=lambda: self.mostrar_medidas_forma(self.principle_frame))
            btn_forma.config(menu=menu_forma)
            btn_forma.pack(side="left", padx=5, pady=2)

            btn_resumen = tk.Menubutton(self.toolbar, text="Resumen Completo",
                                       font=("Arial", 10))
            menu_resumen = tk.Menu(btn_resumen, tearoff=False)
            menu_resumen.add_command(label="Ver Resumen Estadístico",
                                    command=lambda: self.mostrar_resumen_completo(self.principle_frame))
            btn_resumen.config(menu=menu_resumen)
            btn_resumen.pack(side="left", padx=5, pady=2)

        else:
            # Menú clásico para ventana independiente
            menu_bar = tk.Menu(self.sub_window)
            self.sub_window.configure(menu=menu_bar)

            menu_dispersion = tk.Menu(menu_bar, tearoff=False)
            menu_bar.add_cascade(label="Medidas de Dispersión", menu=menu_dispersion)
            menu_dispersion.add_command(label="Calcular Dispersión",
                                       command=lambda: self.mostrar_medidas_dispersion(self.principle_frame))

            menu_forma = tk.Menu(menu_bar, tearoff=False)
            menu_bar.add_cascade(label="Medidas de Forma", menu=menu_forma)
            menu_forma.add_command(label="Calcular Asimetría y Curtosis",
                                  command=lambda: self.mostrar_medidas_forma(self.principle_frame))

            menu_resumen = tk.Menu(menu_bar, tearoff=False)
            menu_bar.add_cascade(label="Resumen Completo", menu=menu_resumen)
            menu_resumen.add_command(label="Ver Resumen Estadístico",
                                    command=lambda: self.mostrar_resumen_completo(self.principle_frame))
