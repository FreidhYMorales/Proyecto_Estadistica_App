import math
import tkinter as tk
from tkinter import filedialog
import pandas as pd
<<<<<<< HEAD
#from statistics import mode
from scipy.stats import gmean, hmean

class Tabla:
    def __init__(self, columnas=None):
        
        if columnas:
            self.columnas = tuple(columnas)
            self.filas = [tuple(['-'] * len(self.columnas))]
        else:
            self.columnas = ('Variable1',)
            self.filas = [('-',)]
=======

# from statistics import mode
from scipy.stats import gmean, hmean


class Tabla:
    def __init__(self, columnas=None):

        if columnas:
            self.columnas = tuple(columnas)
            self.filas = [tuple(["-"] * len(self.columnas))]
        else:
            self.columnas = ("Variable1",)
            self.filas = [("-",)]
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)

    def agregar_columna(self, nombre_columna, valores=None):
        if nombre_columna in self.columnas:
            raise ValueError(f"La columna '{nombre_columna}' ya existe.")
        self.columnas += (nombre_columna,)
        if not self.filas:
            return
        if valores is None:
<<<<<<< HEAD
            valores = ['-'] * len(self.filas)
=======
            valores = ["-"] * len(self.filas)
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        elif len(valores) != len(self.filas):
            raise ValueError("Número de valores no coincide con número de filas.")
        self.filas = [fila + (valor,) for fila, valor in zip(self.filas, valores)]

    def edit_column_name(self, old_name, new_name):
        if old_name not in self.columnas:
            raise ValueError(f"La columna '{old_name}' no existe.")
        if new_name in self.columnas:
            raise ValueError(f"La columna '{new_name}' ya existe.")
        col_index = self.columnas.index(old_name)
<<<<<<< HEAD
        self.columnas = self.columnas[:col_index] + (new_name,) + self.columnas[col_index + 1:]
=======
        self.columnas = (
            self.columnas[:col_index] + (new_name,) + self.columnas[col_index + 1 :]
        )
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)

    def agregar_fila(self, fila):
        if len(fila) != len(self.columnas):
            raise ValueError("La fila no coincide con el número de columnas.")
        self.filas.append(tuple(fila))

    def editar_celda(self, fila_index, columna_nombre, nuevo_valor):
        if fila_index < 0 or fila_index >= len(self.filas):
            raise IndexError("Índice de fila fuera de rango.")
        if columna_nombre not in self.columnas:
            raise ValueError("Nombre de columna no válido.")
        col_index = self.columnas.index(columna_nombre)
        fila_como_lista = list(self.filas[fila_index])
        fila_como_lista[col_index] = nuevo_valor
        self.filas[fila_index] = tuple(fila_como_lista)

    def eliminar_fila(self, fila_index):
        if fila_index < 0 or fila_index >= len(self.filas):
            raise IndexError("Índice de fila fuera de rango.")
        del self.filas[fila_index]

    def eliminar_columna(self, columna_nombre):
        if columna_nombre not in self.columnas:
            raise ValueError(f"La columna '{columna_nombre}' no existe.")
        col_index = self.columnas.index(columna_nombre)
<<<<<<< HEAD
        self.columnas = self.columnas[:col_index] + self.columnas[col_index + 1:]
        self.filas = [fila[:col_index] + fila[col_index + 1:] for fila in self.filas]
=======
        self.columnas = self.columnas[:col_index] + self.columnas[col_index + 1 :]
        self.filas = [fila[:col_index] + fila[col_index + 1 :] for fila in self.filas]
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)

    def obtener_filas(self):
        return list(self.filas)

    def obtener_fila(self, fila_index):
        if fila_index < 0 or fila_index >= len(self.filas):
            raise IndexError("Índice de fila fuera de rango.")
        return self.filas[fila_index]

    def obtener_columna(self, nombre_columna):
        if nombre_columna not in self.columnas:
            raise ValueError(f"La columna '{nombre_columna}' no existe.")
        idx = self.columnas.index(nombre_columna)
        return [fila[idx] for fila in self.filas]

    def obtener_tabla_como_tuplas(self):
        return [self.columnas] + self.filas

    def construir_tabla_agrupada(self, lista_datos, intervalo=None):
<<<<<<< HEAD
        df = pd.DataFrame({'x': lista_datos})
        n = len(df)
        xmin, xmax = int(df['x'].min()), int(df['x'].max())
=======
        df = pd.DataFrame({"x": lista_datos})
        n = len(df)
        xmin, xmax = int(df["x"].min()), int(df["x"].max())
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        rango = xmax - xmin

        # Calcular amplitud si no se especifica
        if intervalo is None:
            k = round(1 + 3.322 * math.log2(n))
            intervalo = math.ceil(rango / k)
            if intervalo < 2:
                intervalo = 2  # mínimo rango de 2

        # Generar límites inferiores y superiores
        Li = list(range(xmin, xmax + 1, intervalo))
        Ls = [li + intervalo - 1 for li in Li]

        # Ajustar último límite superior para cubrir xmax
        if Ls[-1] < xmax:
            Ls[-1] = xmax

        # Crear tabla
<<<<<<< HEAD
        tabla = pd.DataFrame({'Li': Li, 'Ls': Ls})
        tabla['Xi o ci'] = (tabla['Li'] + tabla['Ls']) / 2

        # Calcular frecuencias
        tabla['f'] = [
            df[(df['x'] >= Li[i]) & (df['x'] <= Ls[i])].shape[0]
            for i in range(len(Li))
=======
        tabla = pd.DataFrame({"Li": Li, "Ls": Ls})
        tabla["Xi o ci"] = (tabla["Li"] + tabla["Ls"]) / 2

        # Calcular frecuencias
        tabla["f"] = [
            df[(df["x"] >= Li[i]) & (df["x"] <= Ls[i])].shape[0] for i in range(len(Li))
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        ]

        return tabla, n, intervalo, df

    def calcular_frecuencias(self, tabla, n):
<<<<<<< HEAD
        tabla['fr%'] = (tabla['f'] / n * 100).round(2)
        diferencia = 100 - tabla['fr%'].sum()
        tabla.loc[tabla.index[-1], 'fr%'] += diferencia
        tabla['Fa'] = tabla['f'].cumsum()
        tabla['Fa%'] = (tabla['Fa'] / n * 100).round(2)
        tabla.loc[tabla.index[-1], 'Fa%'] = 100.0
        tabla['Fd'] = n - tabla['Fa'].shift(1, fill_value=0)
        tabla['Fd%'] = (tabla['Fd'] / n * 100).round(2)
        tabla.loc[tabla.index[0], 'Fd%'] = 100.0
=======
        tabla["fr%"] = (tabla["f"] / n * 100).round(2)
        diferencia = 100 - tabla["fr%"].sum()
        tabla.loc[tabla.index[-1], "fr%"] += diferencia
        tabla["Fa"] = tabla["f"].cumsum()
        tabla["Fa%"] = (tabla["Fa"] / n * 100).round(2)
        tabla.loc[tabla.index[-1], "Fa%"] = 100.0
        tabla["Fd"] = n - tabla["Fa"].shift(1, fill_value=0)
        tabla["Fd%"] = (tabla["Fd"] / n * 100).round(2)
        tabla.loc[tabla.index[0], "Fd%"] = 100.0
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        return tabla

    def agregar_totales_para_visual(self, tabla):
        fila_total = {
<<<<<<< HEAD
            'Li': '', 'Ls': '', 'Xi o ci': '',
            'f': tabla['f'].sum(),
            'fr%': f"{round(tabla['fr%'].sum(), 2)}%",
            'Fa': '', 'Fa%': '', 'Fd': '', 'Fd%': ''
=======
            "Li": "",
            "Ls": "",
            "Xi o ci": "",
            "f": tabla["f"].sum(),
            "fr%": f"{round(tabla['fr%'].sum(), 2)}%",
            "Fa": "",
            "Fa%": "",
            "Fd": "",
            "Fd%": "",
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        }
        return pd.concat([tabla, pd.DataFrame([fila_total])], ignore_index=True)

    def mostrar_medidas_central(self, root, datos):
        tabla, n, intervalo, df = self.construir_tabla_agrupada(datos)
        tabla = self.calcular_frecuencias(tabla, n)
        self.medidas_central(root, tabla, n, intervalo, df)

    def interpolar_valor(self, tabla, n, intervalo, porcentaje):
<<<<<<< HEAD
            pos = n * porcentaje
            fila = tabla[tabla['Fa'] >= pos].iloc[0]
            idx = fila.name
            L = fila['Li']
            F = tabla.loc[idx - 1, 'Fa'] if idx > 0 else 0
            f = fila['f']
            return L + ((pos - F) / f) * intervalo if f != 0 else L

    def medidas_central(self, root, tabla, n, intervalo, df):

        media_arit = (tabla['Xi o ci'] * tabla['f']).sum() / n

        mediana_pos = n / 2
        fila_mediana = tabla[tabla['Fa'] >= mediana_pos].iloc[0]
        idx = fila_mediana.name
        L = fila_mediana['Li']
        F = tabla.loc[idx - 1, 'Fa'] if idx > 0 else 0
        f_med = fila_mediana['f']
        mediana = L + ((mediana_pos - F) / f_med) * intervalo

        f_modal = tabla['f'].max()
        fila_moda = tabla[tabla['f'] == f_modal].iloc[0]
        idx_moda = fila_moda.name
        Lm = fila_moda['Li']
        f1 = f_modal
        f0 = tabla.loc[idx_moda - 1, 'f'] if idx_moda > 0 else 0
        f2 = tabla.loc[idx_moda + 1, 'f'] if (idx_moda + 1) in tabla.index else 0
=======
        pos = n * porcentaje
        fila = tabla[tabla["Fa"] >= pos].iloc[0]
        idx = fila.name
        L = fila["Li"]
        F = tabla.loc[idx - 1, "Fa"] if idx > 0 else 0
        f = fila["f"]
        return L + ((pos - F) / f) * intervalo if f != 0 else L

    def medidas_central(self, root, tabla, n, intervalo, df):

        media_arit = (tabla["Xi o ci"] * tabla["f"]).sum() / n

        mediana_pos = n / 2
        fila_mediana = tabla[tabla["Fa"] >= mediana_pos].iloc[0]
        idx = fila_mediana.name
        L = fila_mediana["Li"]
        F = tabla.loc[idx - 1, "Fa"] if idx > 0 else 0
        f_med = fila_mediana["f"]
        mediana = L + ((mediana_pos - F) / f_med) * intervalo

        f_modal = tabla["f"].max()
        fila_moda = tabla[tabla["f"] == f_modal].iloc[0]
        idx_moda = fila_moda.name
        Lm = fila_moda["Li"]
        f1 = f_modal
        f0 = tabla.loc[idx_moda - 1, "f"] if idx_moda > 0 else 0
        f2 = tabla.loc[idx_moda + 1, "f"] if (idx_moda + 1) in tabla.index else 0
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        D1, D2 = f1 - f0, f1 - f2
        moda_interpolada = Lm + (D1 / (D1 + D2)) * intervalo if (D1 + D2) != 0 else Lm

        # Calcular moda cruda (puede haber múltiples modas)
<<<<<<< HEAD
        frecuencias = df['x'].value_counts()
        moda_cruda_lista = frecuencias[frecuencias == frecuencias.max()].index.tolist()
        moda_cruda = ', '.join(map(str, moda_cruda_lista))

        media_geom = gmean(df['x'])
        media_arm = hmean(df['x'])
=======
        frecuencias = df["x"].value_counts()
        moda_cruda_lista = frecuencias[frecuencias == frecuencias.max()].index.tolist()
        moda_cruda = ", ".join(map(str, moda_cruda_lista))

        media_geom = gmean(df["x"])
        media_arm = hmean(df["x"])
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)

        Q1 = self.interpolar_valor(tabla, n, intervalo, 0.25)
        Q2 = mediana
        Q3 = self.interpolar_valor(tabla, n, intervalo, 0.75)

<<<<<<< HEAD
        deciles = {f"D{i}": self.interpolar_valor(tabla, n, intervalo, i / 10) for i in range(1, 10)}
        percentiles = {f"P{i}": self.interpolar_valor(tabla, n, intervalo, i / 100) for i in range(1, 100)}
=======
        deciles = {
            f"D{i}": self.interpolar_valor(tabla, n, intervalo, i / 10)
            for i in range(1, 10)
        }
        percentiles = {
            f"P{i}": self.interpolar_valor(tabla, n, intervalo, i / 100)
            for i in range(1, 100)
        }
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)

        # Crear ventana emergente
        ventana = tk.Toplevel(root)
        ventana.title("Medidas de Tendencia Central")
        ventana.geometry("600x600")

        text = tk.Text(ventana, wrap="word", font=("Arial", 10))
        text.pack(expand=True, fill="both", padx=10, pady=10)

        text.insert(tk.END, "--- Medidas de Tendencia Central ---\n")
        text.insert(tk.END, f"Media Aritmética (agrupada): {media_arit:.2f}\n")
        text.insert(tk.END, f"Mediana (agrupada): {mediana:.2f}\n")
        text.insert(tk.END, f"Moda Cruda: {moda_cruda}\n")
        text.insert(tk.END, f"Moda Interpolada: {moda_interpolada:.2f}\n")
        text.insert(tk.END, f"Media Geométrica: {media_geom:.2f}\n")
        text.insert(tk.END, f"Media Armónica: {media_arm:.2f}\n\n")

        text.insert(tk.END, "Cuartiles\n")
        text.insert(tk.END, f"Q1: {float(Q1):.2f}\n")
        text.insert(tk.END, f"Q2 (Mediana): {float(Q2):.2f}\n")
        text.insert(tk.END, f"Q3: {float(Q3):.2f}\n\n")

        text.insert(tk.END, "Deciles\n")
        for k, v in deciles.items():
            text.insert(tk.END, f"{k}: {v:.2f}  \n")
        text.insert(tk.END, "\n\n")

        text.insert(tk.END, "Percentiles (seleccionados)\n")
        for k in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
            text.insert(tk.END, f"P{k}: {percentiles[f'P{k}']:.2f}  \n")
        text.insert(tk.END, "\n")

    def procesar_y_mostrar_tabla(self, datos):
        tabla, n, intervalo, df = self.construir_tabla_agrupada(datos)
        tabla = self.calcular_frecuencias(tabla, n)
        tabla_final = self.agregar_totales_para_visual(tabla)
        return tabla_final

    def mostrar_tabla_completa_ordenada(self, datos):
<<<<<<< HEAD
        df = pd.DataFrame({'x': datos})
        frecuencia = df['x'].value_counts().sort_index()
=======
        df = pd.DataFrame({"x": datos})
        frecuencia = df["x"].value_counts().sort_index()
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        valores = frecuencia.index.tolist()
        f = frecuencia.values.tolist()
        fr_percent = ((frecuencia / len(df)) * 100).round(2).tolist()
        fa = frecuencia.cumsum().tolist()
        fa_percent = ((frecuencia.cumsum() / len(df)) * 100).round(2).tolist()
        fd = (len(df) - frecuencia.cumsum().shift(1, fill_value=0)).tolist()
        fd_percent = ((pd.Series(fd) / len(df)) * 100).round(2).tolist()
<<<<<<< HEAD
        #fx = [valores[i] * f[i] for i in range(len(valores))]

        tabla = pd.DataFrame({
            'x': valores,
            'f': f,
            'fr%': fr_percent,
            'Fa': fa,
            'Fa%': fa_percent,
            'Fd': fd,
            'Fd%': fd_percent,
        })
=======
        # fx = [valores[i] * f[i] for i in range(len(valores))]

        tabla = pd.DataFrame(
            {
                "x": valores,
                "f": f,
                "fr%": fr_percent,
                "Fa": fa,
                "Fa%": fa_percent,
                "Fd": fd,
                "Fd%": fd_percent,
            }
        )
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)

        return tabla

    def importar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona un archivo para importar",
            filetypes=(
                ("Archivos Excel", "*.xlsx *.xls"),
                ("Archivos CSV", "*.csv"),
<<<<<<< HEAD
                ("Todos los archivos", "*.*")
            )
=======
                ("Todos los archivos", "*.*"),
            ),
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        )
        if not ruta:
            print("No se seleccionó ningún archivo.")
            return

        try:
            df = pd.read_csv(ruta) if ruta.endswith(".csv") else pd.read_excel(ruta)
            self.columnas = tuple(df.columns)
            self.filas = [tuple(fila) for fila in df.values.tolist()]
            print("Datos importados correctamente.")
        except Exception as e:
            print("Error al importar archivo:", e)
