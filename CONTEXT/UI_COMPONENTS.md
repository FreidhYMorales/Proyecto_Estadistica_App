# Componentes de UI — CustomTkinter

Referencia de los widgets reutilizables definidos en `views/components.py` y `views/theme.py`,
y de las clases de layout definidas en `views/main_window.py`.

---

## `views/theme.py`

Debe importarse antes de cualquier widget CTK.
`main_window.py` lo importa primero, garantizando que `ctk.set_appearance_mode("dark")`
se ejecute antes de crear ningún widget.

### Constantes de fuente

| Constante | Valor base | Uso |
|---|---|---|
| `FONT_TITLE` | Arial 18 bold | Título de la aplicación en Sidebar |
| `FONT_SECTION` | Arial 12 bold | Subtítulos dentro de paneles |
| `FONT_NORMAL` | Arial 11 | Texto general |
| `FONT_SMALL` | Arial 10 | Labels, botones en toolbar |
| `FONT_MONO` | Courier New 10 | Resultados con alineación |
| `FONT_MONO_SM` | Courier New 9 | Resultados compactos |

En macOS se aplica `_SCALE = 1.15` automáticamente.

### Constantes de padding

| Constante | Valor | Uso |
|---|---|---|
| `PAD_XS` | 3 px | Espaciado mínimo entre elementos |
| `PAD_S` | 5 px | Padding estándar en toolbar |
| `PAD_M` | 10 px | Padding entre secciones |
| `PAD_L` | 16 px | Márgenes externos de paneles |

### `COLOR_CANVAS_BG = "#1e1e2e"`
Color de fondo del `tk.Canvas` del diagrama de árbol.

### `apply_treeview_dark_style()`
Aplica el estilo `"Dark.Treeview"` a `ttk.Style` (tema `clam`).
Llamar una vez al iniciar la aplicación.

---

## `views/components.py`

### `clear_frame(frame)`
Destruye todos los widgets hijos de un frame.

---

### `CTkDropdown`

`CTkButton` que muestra un popup flotante de opciones al hacer clic.
Reemplaza `tk.Menubutton + tk.Menu`.

```python
CTkDropdown(
    parent, "Título del menú",
    items=[("Opción", callback), ...],
    font=FONT_SMALL,
).pack(side="left", padx=PAD_S)
```

El popup usa `place()` en la ventana raíz, calculando posición desde el botón.
Se cierra al hacer clic fuera de él.

---

### `GraphCanvas`

Embebe un `FigureCanvasTkAgg` de matplotlib + `NavigationToolbar2Tk` dentro de un
`ctk.CTkFrame`.

**Usa `grid(row=0, col=0, sticky="nsew")`** → el parent debe tener:
```python
parent.rowconfigure(0, weight=1)
parent.columnconfigure(0, weight=1)
```
(los métodos `_graph_container()` de cada panel ya lo hacen).

```python
canvas = GraphCanvas(graph_container)
fig, ax = graph_utils.build_histogram(data, 10, "Variable")
canvas.render(fig)   # reemplaza figura anterior sin memory leak
```

---

### `ScrollableCanvas`

`tk.Canvas` con `CTkScrollbar` siempre presentes (nunca desaparecen al redimensionar).

**Modelo de coordenadas:** todas las coordenadas de los items son absolutas dentro
del espacio virtual (`virtual_w × virtual_h`). El viewport es una ventana deslizable
sobre ese espacio. Al redimensionar la ventana **solo cambia el viewport**, no las
coordenadas de los nodos → nunca se necesita recalcular posiciones.

```python
sc = ScrollableCanvas(parent, virtual_w=2000, virtual_h=1400, bg=COLOR_CANVAS_BG)
sc.grid(row=0, column=0, sticky="nsew")

# Dibujar en coordenadas virtuales absolutas:
sc.canvas.create_rectangle(100, 60, 156, 116, fill="#1f6aa5")

# Después de dibujar, expandir el scrollregion:
sc.expand_scrollregion()

# Para operaciones en el canvas interno (click, zoom, etc.):
sc.canvas.bind("<Button-1>", on_click)
```

**Scroll con rueda:** `ScrollableCanvas` NO vincula eventos de rueda del mouse,
para que el consumidor pueda implementar su propio handler (ej. Ctrl+rueda = zoom
en el diagrama de árbol).

---

### `ResultTextWidget`

`ctk.CTkTextbox` de solo lectura con exportación a `.txt`.

```python
w = ResultTextWidget(parent, font=FONT_MONO_SM)
w.set("Contenido formateado")
w.export("nombre_sugerido.txt")   # abre diálogo guardar
```

---

### `DataTreeview`

`ttk.Treeview` con estilo oscuro dentro de un `ctk.CTkFrame`.
Acepta un `pandas.DataFrame` via `load(df)`.

---

## `views/main_window.py`

### Jerarquía de clases y layout

```
CTk (ventana raíz)
├── Sidebar (CTkScrollableFrame, col=0, weight=0, minsize=240)
│   ├── Sección VARIABLES: name_entry, type_combo, [Agregar][Editar][Importar]
│   ├── Sección DATOS: data_entry, data_col_combo, index_combo, [Nueva fila][Guardar]
│   └── Sección ANÁLISIS/ESTADÍSTICA/GRÁFICOS/PROBABILIDADES/REGRESIÓN: nav buttons
│       └── set_active(key) → resalta el botón activo
└── RightPane (CTkFrame, col=1, weight=1)
    ├── DataTable        (row=0, weight=2, minsize=180) — siempre visible
    ├── ContentToolbar   (row=1, fixed 32 px)           — breadcrumb + acciones
    └── ContentStack     (row=2, weight=3, minsize=380) — panel switcher
        ├── FrequencyPanel    (key="freq")
        ├── StatisticsPanel   (key="stats")
        ├── GraphsPanel       (key="graphs")
        ├── ProbabilityPanel  (key="prob")
        └── RegressionPanel   (key="reg")
```

### `ContentToolbar`

Barra de 32 px con breadcrumb y botones contextuales opcionales.

```python
toolbar.set_panel("graphs", actions=[("Exportar PNG", callback)])
```

Los `_LABELS` mapean la clave del panel a su nombre legible.

### `ContentStack`

Todos los paneles están en `row=0, col=0` del stack. `tkraise()` los alterna.

```
minsize garantías:
  ContentStack.rowconfigure(0, weight=1, minsize=380)   → matplotlib nunca <380 px alto
  ContentStack.columnconfigure(0, weight=1, minsize=580) → matplotlib nunca <580 px ancho
  window.minsize(1060, 700)                              → límite de la ventana
```

### `FrequencyPanel`

Panel liviano para tablas de frecuencia. Se actualiza sin destruir widgets:
```python
freq_panel.load("Tabla Agrupada — Peso", df)
stack.show("freq")
```

### Navegación

```python
# Correcto: un solo método central
def _show_panel(self, key, actions=None):
    self._stack.show(key)        # tkraise() al panel correcto
    self._ctoolbar.set_panel(key, actions)  # actualiza breadcrumb
    self._sidebar.set_active(key)           # resalta botón activo

# Cada callback simplemente llama:
def _show_graphs_panel(self): self._show_panel("graphs")
```

### `Sidebar.set_active(key)`

```python
# Botones con colores por dominio (estado inactivo):
_BTN_COLORS = {
    "stats":  ("#2a6494", "#1a4a70"),
    "graphs": ("#2e6b3e", "#1b4a28"),
    "prob":   ("#7a6b2e", "#4a3e18"),
    "reg":    ("#6b2e2e", "#4a1b1b"),
}
_ACTIVE_COLOR = ("#1f6aa5", "#4d9de0")   # azul brillante para estado activo
```

---

## Patrón de layout en paneles de análisis

Todos los paneles siguen la misma estructura interna:

```
Panel._root (CTkFrame fg_color="transparent", row=0 col=0 en ContentStack)
├── _toolbar (row=0, height=44, fg_color=gray) — CTkDropdown × N
└── _content (row=1, weight=1)
      ├── Control row (row=0): combos + entry + [Calcular/Generar] + [Exportar]
      └── Result/Graph area (row=1, weight=1): ResultTextWidget o GraphCanvas
```

`_make_panel()` en cada panel limpia `_content` con `clear_frame()` y retorna
el frame de control + widget de resultado.

---

## Estrategia de coordenadas del Canvas en resize

El diagrama de árbol usa `ScrollableCanvas` con espacio virtual 2000×1400 px.

```
┌─────────────────── virtual space (2000×1400) ────────────────────┐
│                                                                    │
│   Nodo A ──── Nodo B                                              │
│         ╲─── Nodo C                                               │
│                                                                    │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
         ↑
    Viewport (tamaño = ventana actual, scrollable)
    Al redimensionar, el viewport cambia pero los nodos NO se mueven.
    Los scrollbars permiten navegar el espacio virtual restante.
```

Al hacer zoom con Ctrl+rueda, `canvas.scale("all", cx, cy, factor, factor)` escala
todos los items *in-place* en el espacio virtual. Las coordenadas de los items cambian
pero permanecen dentro del espacio virtual. Después se llama `sc.expand_scrollregion()`
para ajustar el scrollregion al nuevo bbox.
