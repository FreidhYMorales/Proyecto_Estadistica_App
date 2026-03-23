import tkinter as tk
from tkinter import Toplevel, ttk
<<<<<<< HEAD
import pyautogui
import Probability

class WindowSet:
    def __init__(self, name, data):
        #CONFIGURAR TABLA DE DATOS
        self.data = data

        #CREACION DE VENTANA
=======

# import pyautogui
import Probability
import Statistics
import Graphs
import Regression


class WindowSet:
    def __init__(self, name, data):
        # CONFIGURAR TABLA DE DATOS
        self.data = data

        # CREACION DE VENTANA
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        self.window = tk.Tk()
        self.window.title(name)

    def accion_tabla_agrupada(self):
        self.mostrar_en_treeview(
<<<<<<< HEAD
            self.operation_table_frames, 
            self.data.procesar_y_mostrar_tabla(self.data.obtener_columna(self.data_type_box2.get().strip()))
            )

    def accion_tabla_no_agrupada(self):
        self.mostrar_en_treeview(
            self.operation_table_frames, 
            self.data.mostrar_tabla_completa_ordenada( self.data.obtener_columna(self.data_type_box2.get().strip()))
            )

    def medidas_tendencia_central(self):
        self.data.mostrar_medidas_central(
            self.operation_table_frames, 
            self.data.obtener_columna(self.data_type_box2.get().strip())
            )       

    def buildInApp(self):
        #CREACION DE FRAME PRINCIPAL PARA POSICIONAR DEMAS OBJETOS VISUALES
        self.principle_frame = tk.Frame(self.window)
        
        #CREACION DE OBJETOS SECUNDARIOS Y SUS RESPECTIVAS ETIQUETAS
            #FRAME PARA INGRESAR DATOS
        self.ingresos_datos_frame = tk.LabelFrame(self.principle_frame, bg="skyblue1", text="Variables", font=("bold", 12))
        
            #NOMBRE DE VARIABLE
        tk.Label(self.ingresos_datos_frame, text="Nombre:", bg="skyblue1", font=("bold", 10)).grid(row=0, column=0, sticky="ne", pady=5)
        self.name_box = tk.Entry(self.ingresos_datos_frame)
           
            #TIPO DE VARIABLES
        tk.Label(self.ingresos_datos_frame, text="Tipo: ", bg="skyblue1", font=("bold", 10)).grid(row=1, column=0, sticky="ne", pady=5)
        self.type_box = ttk.Combobox(self.ingresos_datos_frame, values=["Numero", "Cadena"], state="readonly")
            
            #APARTADO DE BOTONES DE VARIABLES
        self.buttons_var = tk.Frame(self.ingresos_datos_frame)
            #BOTON PARA EDITAR EL NOMBRE DE VARIABLE
        self.edit_clm = tk.Button(self.buttons_var, text="Editar", font=("bold", 10), command=self.editarNombreColumna)
            #BOTON PARA AGREGAR VARIABLE
        self.add_var1 = tk.Button(self.buttons_var, text="Agregar", font=("bold", 10), command=self.agregar_variable)
            #BOTON PARA IMPORTAR ARCHIVO
        self.import_button = tk.Button(self.buttons_var, text="Importar", font=("bold", 10), command=self.importar_archivo)
            #FRAME DE EDITAR DATOS
        self.editar_datos_frame = tk.LabelFrame(self.principle_frame, bg="skyblue1", text="Datos", font=("bold", 12))

        tk.Label(self.editar_datos_frame, text="Dato: ", bg="skyblue1", font=("bold", 10)).grid(row=0, column=0, sticky="ne", pady=5)
        self.data_box = tk.Entry(self.editar_datos_frame)
        
        tk.Label(self.editar_datos_frame, text="Variable: ", bg="skyblue1", font=("bold", 10)).grid(row=1, column=0, sticky="ne", pady=5)
        self.data_type_box = ttk.Combobox(self.editar_datos_frame, values=self.data.columnas, state="readonly")
        
        tk.Label(self.editar_datos_frame, text="Indice: ", bg="skyblue1", font=("bold", 10)).grid(row=2, column=0, sticky="ne", pady=5)
        self.index_box = ttk.Combobox(self.editar_datos_frame, values=self.rowAmount(self.data.obtener_filas()), state="readonly")
        
        self.add_data1 = tk.Button(self.editar_datos_frame, text="Crear", font=("bold", 10))
        self.edit_data1 = tk.Button(self.editar_datos_frame, text="Agregar", font=("bold", 10))
        
            #FRAME PARA VISUALIZAR LA TABLA DE DATOS
        self.data_table_frame = tk.LabelFrame(self.principle_frame, bg="skyblue1", text="Tabla de Datos", font=("bold", 12))
            #TABLA DE DATOS
        self.data_table = ttk.Treeview(self.data_table_frame, padding=5, columns=(self.data.columnas))
            #FRAME PARA MOSTRAR TABLA DE OPERACIONES
        self.operaciones_frame = tk.LabelFrame(self.principle_frame, bg="skyblue1", text="Operaciones", font=("bold", 12))

        self.data_type_box2 = ttk.Combobox(self.operaciones_frame, values=self.data.columnas, state="readonly")
            
            #FRAME PARA MOSTRAR GRAFICOS O RESULTADOS
        self.operation_table_frames = tk.LabelFrame(self.principle_frame, bg="skyblue1", text="Tablas de Calculos", font=("bold", 12))
        
        self.button1 = tk.Button(self.operaciones_frame, font=("bold", 10), text="Tabla de Frecuencias")
=======
            self.operation_table_frames,
            self.data.procesar_y_mostrar_tabla(
                self.data.obtener_columna(self.data_type_box2.get().strip())
            ),
        )

    def accion_tabla_no_agrupada(self):
        self.mostrar_en_treeview(
            self.operation_table_frames,
            self.data.mostrar_tabla_completa_ordenada(
                self.data.obtener_columna(self.data_type_box2.get().strip())
            ),
        )

    def medidas_tendencia_central(self):
        self.data.mostrar_medidas_central(
            self.operation_table_frames,
            self.data.obtener_columna(self.data_type_box2.get().strip()),
        )

    def buildInApp(self):
        # CREACION DE FRAME PRINCIPAL PARA POSICIONAR DEMAS OBJETOS VISUALES
        self.principle_frame = tk.Frame(self.window)

        # CREACION DE OBJETOS SECUNDARIOS Y SUS RESPECTIVAS ETIQUETAS
        # FRAME PARA INGRESAR DATOS
        self.ingresos_datos_frame = tk.LabelFrame(
            self.principle_frame, bg="black", fg="white", text="Variables", font=("bold", 12)
        )

        # NOMBRE DE VARIABLE
        tk.Label(
            self.ingresos_datos_frame, text="Nombre:", bg="black", fg="white", font=("bold", 10)
        ).grid(row=0, column=0, sticky="ne", pady=5)
        self.name_box = tk.Entry(self.ingresos_datos_frame)

        # TIPO DE VARIABLES
        tk.Label(
            self.ingresos_datos_frame, text="Tipo: ", bg="black", fg="white", font=("bold", 10)
        ).grid(row=1, column=0, sticky="ne", pady=5)
        self.type_box = ttk.Combobox(
            self.ingresos_datos_frame, values=["Numero", "Cadena"], state="readonly"
        )

        # APARTADO DE BOTONES DE VARIABLES
        self.buttons_var = tk.Frame(self.ingresos_datos_frame)
        # BOTON PARA EDITAR EL NOMBRE DE VARIABLE
        self.edit_clm = tk.Button(
            self.buttons_var,
            text="Editar",
            font=("bold", 10),
            command=self.editarNombreColumna,
        )
        # BOTON PARA AGREGAR VARIABLE
        self.add_var1 = tk.Button(
            self.buttons_var,
            text="Agregar",
            font=("bold", 10),
            command=self.agregar_variable,
        )
        # BOTON PARA IMPORTAR ARCHIVO
        self.import_button = tk.Button(
            self.buttons_var,
            text="Importar",
            font=("bold", 10),
            command=self.importar_archivo,
        )
        # FRAME DE EDITAR DATOS
        self.editar_datos_frame = tk.LabelFrame(
            self.principle_frame, bg="black", fg="white", text="Datos", font=("bold", 12)
        )

        tk.Label(
            self.editar_datos_frame, text="Dato: ", bg="black", fg="white", font=("bold", 10)
        ).grid(row=0, column=0, sticky="ne", pady=5)
        self.data_box = tk.Entry(self.editar_datos_frame)

        tk.Label(
            self.editar_datos_frame, text="Variable: ", bg="black", fg="white", font=("bold", 10)
        ).grid(row=1, column=0, sticky="ne", pady=5)
        self.data_type_box = ttk.Combobox(
            self.editar_datos_frame, values=self.data.columnas, state="readonly"
        )

        tk.Label(
            self.editar_datos_frame, text="Indice: ", bg="black", fg="white", font=("bold", 10)
        ).grid(row=2, column=0, sticky="ne", pady=5)
        self.index_box = ttk.Combobox(
            self.editar_datos_frame,
            values=self.rowAmount(self.data.obtener_filas()),
            state="readonly",
        )

        self.add_data1 = tk.Button(
            self.editar_datos_frame, text="Crear", font=("bold", 10)
        )
        self.edit_data1 = tk.Button(
            self.editar_datos_frame, text="Agregar", font=("bold", 10)
        )

        # FRAME PARA VISUALIZAR LA TABLA DE DATOS
        self.data_table_frame = tk.LabelFrame(
            self.principle_frame,
            bg="black", fg="white",
            text="Tabla de Datos",
            font=("bold", 12),
        )
        # TABLA DE DATOS
        self.data_table = ttk.Treeview(
            self.data_table_frame, padding=5, columns=(self.data.columnas)
        )
        # FRAME PARA MOSTRAR TABLA DE OPERACIONES
        self.operaciones_frame = tk.LabelFrame(
            self.principle_frame, bg="black", fg="white", text="Operaciones", font=("bold", 12)
        )

        self.data_type_box2 = ttk.Combobox(
            self.operaciones_frame, values=self.data.columnas, state="readonly"
        )

        # FRAME PARA MOSTRAR GRAFICOS O RESULTADOS
        self.operation_table_frames = tk.LabelFrame(
            self.principle_frame,
            bg="black", fg="white",
            text="Tablas de Calculos",
            font=("bold", 12),
        )

        self.button1 = tk.Button(
            self.operaciones_frame, font=("bold", 10), text="Tabla de Frecuencias"
        )
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)

    def importar_archivo(self):
        self.data.importar_archivo()
        self.actualizar_tabla()

    def editarNombreColumna(self):
        subwindow = Toplevel()
        subwindow.title("Editar")
        subwindow.geometry("350x140+600+350")
<<<<<<< HEAD
        subwindow.configure(bg="skyblue1")
         
        #Frame Principal
        principle_frame = tk.Frame(subwindow)
        principle_frame.configure(bg="skyblue1")
=======
        subwindow.configure(bg="black")

        # Frame Principal
        principle_frame = tk.Frame(subwindow)
        principle_frame.configure(bg="black")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        principle_frame.grid(row=0, column=0, sticky="nsew")

        principle_frame.rowconfigure(0, weight=1)
        principle_frame.columnconfigure(0, weight=1)
        principle_frame.rowconfigure(1, weight=1)
        principle_frame.columnconfigure(1, weight=1)
        principle_frame.rowconfigure(2, weight=1)
<<<<<<< HEAD
        
        tk.Label(principle_frame, text="Variable: ", bg="skyblue1", font=("bold", 10)).grid(row=1, column=0, sticky="ne", pady=5)
        data2_type_box = ttk.Combobox(principle_frame, values=self.data.columnas, state="readonly")
        data2_type_box.grid(row=1, column=1, sticky="nw", padx=5, pady=5)

        tk.Label(principle_frame, text="Nuevo Nombre:", bg="skyblue1", font=("bold", 10)).grid(row=0, column=0, sticky="ne", pady=5)
=======

        tk.Label(
            principle_frame, text="Variable: ", bg="black", fg="white", font=("bold", 10)
        ).grid(row=1, column=0, sticky="ne", pady=5)
        data2_type_box = ttk.Combobox(
            principle_frame, values=self.data.columnas, state="readonly"
        )
        data2_type_box.grid(row=1, column=1, sticky="nw", padx=5, pady=5)

        tk.Label(
            principle_frame, text="Nuevo Nombre:", bg="black", fg="white", font=("bold", 10)
        ).grid(row=0, column=0, sticky="ne", pady=5)
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        name2_box = tk.Entry(principle_frame)
        name2_box.grid(row=0, column=1, sticky="nw", padx=5, pady=5)

        def changeClmName(old_name_box2=data2_type_box, new_name_box2=name2_box):
            old_name = old_name_box2.get().strip()
            new_name = new_name_box2.get().strip()
            if not old_name:
<<<<<<< HEAD
                return  # No se agrega si el nombre está vacío
=======
                return  #  No se agrega si el nombre está vacío
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
            try:
                self.data.edit_column_name(old_name, new_name)
                self.actualizar_tabla()
                subwindow.destroy()
            except ValueError as e:
                print(f"Error: {e}")

        button = tk.Button(principle_frame, text="Cambiar", font=("bold", 10))
        button.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        button.config(command=changeClmName)
<<<<<<< HEAD
        
=======

>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        subwindow.mainloop()

    def agregar_variable(self):
        nombre = self.name_box.get().strip()
        if not nombre:
<<<<<<< HEAD
            return  # No se agrega si el nombre está vacío
=======
            return  #  No se agrega si el nombre está vacío
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        try:
            self.data.agregar_columna(nombre)
            self.actualizar_tabla()
        except ValueError as e:
            print(f"Error: {e}")
<<<<<<< HEAD
     
      
    def frameSet(self):
        #ANCHO Y ALTO DE LA VENTANA DEL DISPOSITIVO
        widht, height = pyautogui.size()
        
        #CONFIGURACION DE LA VENTANA PRINCIPAL
        self.window.minsize(widht, height)
        self.window.state("zoomed")
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        #CONFIGURACION DE FRAME PRINCIPAL
=======

    def frameSet(self):
        # ANCHO Y ALTO DE LA VENTANA DEL DISPOSITIVO
        widht, height = 1080, 720

        # CONFIGURACION DE LA VENTANA PRINCIPAL
        self.window.minsize(widht, height)
        self.window.state("normal")
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        # CONFIGURACION DE FRAME PRINCIPAL
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        self.principle_frame.grid(row=0, column=0, sticky="nsew")
        self.principle_frame.rowconfigure(0, weight=1)
        self.principle_frame.columnconfigure(0, weight=1)
        self.principle_frame.rowconfigure(1, weight=1)
        self.principle_frame.columnconfigure(1, weight=1)
<<<<<<< HEAD
        
        #CONFIGURACION DE FRAMES SECUNDARIOS
            #INGRESO DE DATOS
        self.ingresos_datos_frame.place(relx=0, rely=0, relheight=0.2, relwidth= 0.16)
            #NOMBRE DE VARIABLE
        self.name_box.grid(row=0, column=1, sticky="nw", padx=5, pady=5)
        self.type_box.set("Numero")
        self.type_box.grid(row=1, column=1, sticky="nw", padx=5, pady=5)
            #BOTONES DE VARIABLES
        self.buttons_var.configure(bg="skyblue1")
        self.buttons_var.grid(row=3, column=0, sticky="nsew", rowspan=2,columnspan=2)
=======

        # CONFIGURACION DE FRAMES SECUNDARIOS
        # INGRESO DE DATOS
        self.ingresos_datos_frame.place(relx=0, rely=0, relheight=0.2, relwidth=0.16)
        # NOMBRE DE VARIABLE
        self.name_box.grid(row=0, column=1, sticky="nw", padx=5, pady=5)
        self.type_box.set("Numero")
        self.type_box.grid(row=1, column=1, sticky="nw", padx=5, pady=5)
        # BOTONES DE VARIABLES
        self.buttons_var.configure(bg="black")
        self.buttons_var.grid(row=3, column=0, sticky="nsew", rowspan=2, columnspan=2)
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        self.buttons_var.rowconfigure(0, weight=1)
        self.buttons_var.columnconfigure(0, weight=1)
        self.buttons_var.rowconfigure(1, weight=1)
        self.buttons_var.columnconfigure(1, weight=1)
<<<<<<< HEAD
            #EDITAR NOMBRE DE VARIABLE
        self.edit_clm.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
            #AGREGAR VARIABLE
        self.add_var1.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
            #EXPORTAR EXCEL
        self.import_button.grid(row=0, column=2, sticky="nsew", padx=10, pady=5)
            #EDITAR DATOS
        self.editar_datos_frame.place(relx=0, rely=0.2, relheight=0.3, relwidth= 0.16)
        self.data_box.grid(row=0, column=1, sticky="nw", padx=5, pady=5)
        self.data_type_box.set(self.data.columnas[0])
        self.data_type_box.grid(row=1, column=1, sticky="nw", padx=5, pady=5)
        self.index_box.set('1')
=======
        # EDITAR NOMBRE DE VARIABLE
        self.edit_clm.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        # AGREGAR VARIABLE
        self.add_var1.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        # EXPORTAR EXCEL
        self.import_button.grid(row=0, column=2, sticky="nsew", padx=10, pady=5)
        # EDITAR DATOS
        self.editar_datos_frame.place(relx=0, rely=0.2, relheight=0.3, relwidth=0.16)
        self.data_box.grid(row=0, column=1, sticky="nw", padx=5, pady=5)
        self.data_type_box.set(self.data.columnas[0])
        self.data_type_box.grid(row=1, column=1, sticky="nw", padx=5, pady=5)
        self.index_box.set("1")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        self.index_box.grid(row=2, column=1, sticky="nw", padx=5, pady=5)
        self.add_data1.grid(row=3, column=0, sticky="ne", padx=5, pady=5)
        self.add_data1.config(command=self.rowAdd)
        self.edit_data1.grid(row=3, column=1, sticky="ne", padx=5, pady=5)
        self.edit_data1.config(command=self.addData)
<<<<<<< HEAD
            #TABLA DE DATOS
        self.data_table_frame.place(relx=0.16, rely=0, relheight=0.5, relwidth=0.84)
        self.data_table.place(relx=0.01, rely=0.01, relheight=0.95, relwidth=0.98)
            #OPERACIONES
        self.operaciones_frame.place(relx=0, rely=0.5, relheight=0.5, relwidth=0.16)
        self.data_type_box2.set(self.data.columnas[0])
        self.data_type_box2.pack()
            #GRAFICOS Y RESULTADOS
        self.operation_table_frames.place(relx=0.16, rely=0.5, relheight=0.5, relwidth=0.84)
        tk.Button(
                self.operaciones_frame,
                text="Tabla Agrupada",
                command=self.accion_tabla_agrupada
                ).pack(padx=10, pady=5)
        tk.Button(
                self.operaciones_frame,
                text="Tabla No Agrupada",
                command=self.accion_tabla_no_agrupada
                ).pack(padx=10, pady=5)
        tk.Button(
                self.operaciones_frame,
                text="Medidas Centrales",
                command=self.medidas_tendencia_central
                ).pack(padx=10, pady=5)
        tk.Button(
                self.operaciones_frame,
                text="Probabilidades",
                command=self.probability_window
                ).pack(padx=10, pady=5)
        
        #Actualizar tabla para mostrar en aplicacion
        self.actualizar_tabla()

    def rowAdd(self):
        valores = ['-'] * len(self.data.columnas)
        self.data.agregar_fila(valores)
        self.actualizar_tabla()
    
    def addData(self):
        index = int(self.index_box.get().strip()) - 1
        column = self.data_type_box.get().strip()
        dat = self.data_box.get().strip()    
=======
        # TABLA DE DATOS
        self.data_table_frame.place(relx=0.16, rely=0, relheight=0.5, relwidth=0.84)
        self.data_table.place(relx=0.01, rely=0.01, relheight=0.95, relwidth=0.98)
        # OPERACIONES
        self.operaciones_frame.place(relx=0, rely=0.5, relheight=0.5, relwidth=0.16)
        self.data_type_box2.set(self.data.columnas[0])
        self.data_type_box2.pack()

        # # GRAFICOS Y RESULTADOS
        # self.operation_table_frames.place(
        #     relx=0.16, rely=0.5, relheight=0.5, relwidth=0.84
        # )
        # # Título de sección - Tablas
        # tk.Label(
        #     self.operaciones_frame,
        #     text="TABLAS",
        #     bg="black", fg="white",
        #     font=("Arial", 10, "bold")
        # ).pack(padx=10, pady=(10, 5))
        #
        # tk.Button(
        #     self.operaciones_frame,
        #     text="Tabla Agrupada",
        #     command=self.accion_tabla_agrupada,
        # ).pack(padx=10, pady=5, fill=tk.X)
        # tk.Button(
        #     self.operaciones_frame,
        #     text="Tabla No Agrupada",
        #     command=self.accion_tabla_no_agrupada,
        # ).pack(padx=10, pady=5, fill=tk.X)
        #
        # # Separador
        # ttk.Separator(self.operaciones_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=10)
        #
        # # Título de sección - Análisis Descriptivo
        # tk.Label(
        #     self.operaciones_frame,
        #     text="ANÁLISIS DESCRIPTIVO",
        #     bg="black", fg="white",
        #     font=("Arial", 10, "bold")
        # ).pack(padx=10, pady=(5, 5))
        #
        # tk.Button(
        #     self.operaciones_frame,
        #     text="Medidas Centrales",
        #     command=self.medidas_tendencia_central,
        # ).pack(padx=10, pady=5, fill=tk.X)
        # tk.Button(
        #     self.operaciones_frame,
        #     text="Medidas de Dispersión y Forma",
        #     command=self.statistics_window,
        #     bg="lightblue"
        # ).pack(padx=10, pady=5, fill=tk.X)
        #
        # # Separador
        # ttk.Separator(self.operaciones_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=10)
        #
        # # Título de sección - Gráficos
        # tk.Label(
        #     self.operaciones_frame,
        #     text="GRÁFICOS",
        #     bg="black", fg="white",
        #     font=("Arial", 10, "bold")
        # ).pack(padx=10, pady=(5, 5))
        #
        # tk.Button(
        #     self.operaciones_frame,
        #     text="Gráficos Estadísticos",
        #     command=self.graphs_window,
        #     bg="lightgreen"
        # ).pack(padx=10, pady=5, fill=tk.X)
        #
        # # Separador
        # ttk.Separator(self.operaciones_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=10)
        #
        # # Título de sección - Probabilidades
        # tk.Label(
        #     self.operaciones_frame,
        #     text="PROBABILIDADES",
        #     bg="black", fg="white",
        #     font=("Arial", 10, "bold")
        # ).pack(padx=10, pady=(5, 5))
        #
        # tk.Button(
        #     self.operaciones_frame,
        #     text="Cálculo de Probabilidades",
        #     command=self.probability_window,
        #     bg="lightyellow"
        # ).pack(padx=10, pady=5, fill=tk.X)
        #
        # # Separador
        # ttk.Separator(self.operaciones_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=10)
        #
        # # Título de sección - Regresión
        # tk.Label(
        #     self.operaciones_frame,
        #     text="CORRELACIÓN Y REGRESIÓN",
        #     bg="black", fg="white",
        #     font=("Arial", 10, "bold")
        # ).pack(padx=10, pady=(5, 5))
        #
        # tk.Button(
        #     self.operaciones_frame,
        #     text="Análisis de Regresión",
        #     command=self.regression_window,
        #     bg="lightcoral"
        # ).pack(padx=10, pady=5, fill=tk.X)

        # GRAFICOS Y RESULTADOS
        self.operation_table_frames.place(
            relx=0.16, rely=0.5, relheight=0.5, relwidth=0.84
        )

        # --- TABLAS ---
        tk.Label(
            self.operaciones_frame,
            text="TABLAS",
            bg="black", fg="white",
            font=("Arial", 10, "bold")
        ).pack(padx=10, pady=(10, 5), fill=tk.X)

        tk.Button(
            self.operaciones_frame,
            text="Tabla Agrupada",
            command=self.accion_tabla_agrupada,
        ).pack(padx=10, pady=3, fill=tk.X)

        tk.Button(
            self.operaciones_frame,
            text="Tabla No Agrupada",
            command=self.accion_tabla_no_agrupada,
        ).pack(padx=10, pady=3, fill=tk.X)

        # --- ANÁLISIS DESCRIPTIVO ---
        tk.Label(
            self.operaciones_frame,
            text="ANÁLISIS DESCRIPTIVO",
            bg="black", fg="white",
            font=("Arial", 10, "bold")
        ).pack(padx=10, pady=(10, 5), fill=tk.X)

        tk.Button(
            self.operaciones_frame,
            text="Medidas Centrales",
            command=self.medidas_tendencia_central,
        ).pack(padx=10, pady=3, fill=tk.X)

        tk.Button(
            self.operaciones_frame,
            text="Medidas de Dispersión y Forma",
            command=self.statistics_window,
            bg="lightblue"
        ).pack(padx=10, pady=3, fill=tk.X)

        # --- GRÁFICOS ---
        tk.Label(
            self.operaciones_frame,
            text="GRÁFICOS",
            bg="black", fg="white",
            font=("Arial", 10, "bold")
        ).pack(padx=10, pady=(10, 5), fill=tk.X)

        tk.Button(
            self.operaciones_frame,
            text="Gráficos Estadísticos",
            command=self.graphs_window,
            bg="lightgreen"
        ).pack(padx=10, pady=3, fill=tk.X)

        # --- PROBABILIDADES ---
        tk.Label(
            self.operaciones_frame,
            text="PROBABILIDADES",
            bg="black", fg="white",
            font=("Arial", 10, "bold")
        ).pack(padx=10, pady=(10, 5), fill=tk.X)

        tk.Button(
            self.operaciones_frame,
            text="Cálculo de Probabilidades",
            command=self.probability_window,
            bg="lightyellow"
        ).pack(padx=10, pady=3, fill=tk.X)

        # --- REGRESIÓN ---
        tk.Label(
            self.operaciones_frame,
            text="CORRELACIÓN Y REGRESIÓN",
            bg="black", fg="white",
            font=("Arial", 10, "bold")
        ).pack(padx=10, pady=(10, 5), fill=tk.X)

        tk.Button(
            self.operaciones_frame,
            text="Análisis de Regresión",
            command=self.regression_window,
            bg="lightcoral"
        ).pack(padx=10, pady=3, fill=tk.X)

        # Actualizar tabla para mostrar en aplicacion
        self.actualizar_tabla()

    def rowAdd(self):
        valores = ["-"] * len(self.data.columnas)
        self.data.agregar_fila(valores)
        self.actualizar_tabla()

    def addData(self):
        index = int(self.index_box.get().strip()) - 1
        column = self.data_type_box.get().strip()
        dat = self.data_box.get().strip()
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)

        if not dat:
            return
        try:
            self.data.editar_celda(index, column, dat)
            self.actualizar_tabla()
        except ValueError as e:
            print(f"Error: {e}")

<<<<<<< HEAD
    #Indices de filas        
    def rowAmount(self, tupla):
        indexes = []
        
        for i in range(len(tupla)):
           indexes.append(f"{i+1}")
        
=======
    # Indices de filas
    def rowAmount(self, tupla):
        indexes = []

        for i in range(len(tupla)):
            indexes.append(f"{i+1}")

>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        return tuple(indexes)

    def mostrar_en_treeview(self, root, tabla):
        self.clear_frame(root)
        tree = ttk.Treeview(root)
<<<<<<< HEAD
        #tree.pack(expand=True, fill="both")
=======
        # tree.pack(expand=True, fill="both")
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        tree.place(relx=0.01, rely=0.01, relheight=0.95, relwidth=0.84)
        tree["columns"] = list(tabla.columns)
        tree["show"] = "headings"
        for col in tabla.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=80)
        for _, fila in tabla.iterrows():
            tree.insert("", "end", values=list(fila))

<<<<<<< HEAD
    #Funciones de utilidad
=======
    # Funciones de utilidad
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def probability_window(self):
<<<<<<< HEAD
        # Limpiar primero el frame de operaciones
        self.clear_frame(self.operation_table_frames)

        # Crear Probability embebido dentro del operation_table_frames
        self.probability = Probability.Probability(
            self.window,
            parent_frame=self.operation_table_frames
        )
        self.probability.running()

=======
        #  Limpiar primero el frame de operaciones
        self.clear_frame(self.operation_table_frames)

        #  Crear Probability embebido dentro del operation_table_frames
        self.probability = Probability.Probability(
            self.window, parent_frame=self.operation_table_frames
        )
        self.probability.running()

    def statistics_window(self):
        #  Limpiar el frame de operaciones
        self.clear_frame(self.operation_table_frames)

        #  Crear Statistics embebido
        self.statistics = Statistics.Statistics(
            self.window, self.data, parent_frame=self.operation_table_frames
        )
        self.statistics.running()

    def graphs_window(self):
        #  Limpiar el frame de operaciones
        self.clear_frame(self.operation_table_frames)

        #  Crear Graphs embebido
        self.graphs = Graphs.Graphs(
            self.window, self.data, parent_frame=self.operation_table_frames
        )
        self.graphs.running()

    def regression_window(self):
        #  Limpiar el frame de operaciones
        self.clear_frame(self.operation_table_frames)

        #  Crear Regression embebido
        self.regression = Regression.Regression(
            self.window, self.data, parent_frame=self.operation_table_frames
        )
        self.regression.running()

>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
    def running(self):
        self.buildInApp()
        self.frameSet()
        self.window.mainloop()

    def actualizar_tabla(self):
<<<<<<< HEAD
        # Limpiar columnas anteriores
=======
        #  Limpiar columnas anteriores
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        self.data_table.delete(*self.data_table.get_children())
        self.data_table["columns"] = self.data.columnas

        self.data_table.column("#0", width=20)
        self.data_table.heading("#0", text="Índice")
<<<<<<< HEAD
        
        # Configurar encabezados
=======

        #  Configurar encabezados
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        for col in self.data.columnas:
            self.data_table.heading(col, text=col)
            self.data_table.column(col, anchor="center", width=80)

<<<<<<< HEAD
        # Insertar filas
        for idx, fila in enumerate(self.data.obtener_filas(), start=1):
            self.data_table.insert("", "end", text=str(idx), values=fila)
        
=======
        #  Insertar filas
        for idx, fila in enumerate(self.data.obtener_filas(), start=1):
            self.data_table.insert("", "end", text=str(idx), values=fila)

>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
        self.index_box.configure(values=self.rowAmount(self.data.obtener_filas()))
        self.data_type_box.configure(values=self.data.columnas)
        self.data_type_box.set(self.data.columnas[0])
        self.data_type_box2.configure(values=self.data.columnas)
        self.data_type_box2.set(self.data.columnas[0])
