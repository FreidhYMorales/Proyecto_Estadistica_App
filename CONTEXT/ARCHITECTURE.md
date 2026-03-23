# Arquitectura V3 — Estadística Descriptiva

## Estado del proyecto

**V3 completada.** Migración desde V2 (scripts monolíticos con tkinter puro) a arquitectura
MVC modular con CustomTkinter. Toda la lógica de negocio está separada de la UI.

---

## Estructura de directorios

```
Proyecto_Estadistica_App_V3/
├── pyproject.toml
├── requirements.txt
├── README.md
├── CONTEXT/                              ← Documentación del proyecto
│   ├── ARCHITECTURE.md                   ← Este archivo
│   ├── MIGRATION_PLAN.md
│   ├── BUGS_AND_ISSUES.md
│   └── V2_INVENTORY.md
├── src/
│   └── Estadistica Descriptiva/          ← Paquete principal
│       ├── main.py                       ← Entry point
│       ├── __init__.py
│       ├── models/                       ← Capa de datos
│       │   ├── table.py                  ← Modelo de tabla (CRUD + import de archivo)
│       │   └── __init__.py
│       ├── views/                        ← Capa de presentación (CustomTkinter)
│       │   ├── theme.py                  ← Apariencia CTK, constantes de fuente/padding
│       │   ├── components.py             ← Widgets reutilizables (CTkDropdown, GraphCanvas…)
│       │   ├── main_window.py            ← Ventana principal, Sidebar, DataTable
│       │   ├── statistics_panel.py       ← Panel de dispersión y forma
│       │   ├── graphs_panel.py           ← Panel de gráficos matplotlib
│       │   ├── probability_panel.py      ← Panel de probabilidad y distribuciones
│       │   ├── regression_panel.py       ← Panel de correlación y regresión
│       │   └── __init__.py
│       ├── controllers/                  ← Capa de coordinación
│       │   ├── app_controller.py         ← Controlador principal
│       │   └── __init__.py
│       └── utils/                        ← Lógica de negocio pura (sin UI)
│           ├── trends.py                 ← Tablas de frecuencia agrupadas/no agrupadas
│           ├── statistics.py             ← Medidas estadísticas (central, dispersión, forma)
│           ├── graphs.py                 ← Generación de figuras matplotlib (fig, ax)
│           ├── probability.py            ← Cálculos de probabilidad y distribuciones
│           ├── regression.py             ← Correlación y regresión (lineal, exp, log, múltiple)
│           └── __init__.py
├── tests/
│   ├── conftest.py                       ← sys.path setup para pytest
│   ├── test_trends.py                    ← 14 tests para utils/trends.py
│   ├── test_statistics.py                ← 13 tests para utils/statistics.py
│   ├── test_regression.py                ← 20 tests para utils/regression.py
│   └── test_probability.py               ← 25 tests para utils/probability.py
├── data/
├── docs/
└── misc/
```

---

## Capas y responsabilidades

### `models/` — Datos
- **Qué hace:** Almacena y gestiona la estructura de datos (tabla con columnas y filas). Importa archivos CSV/Excel dado una ruta.
- **Qué NO hace:** Cálculos estadísticos, UI, diálogos de archivo.
- **Dependencias externas:** `pandas`, `openpyxl`.
- **Regla:** Nunca importar `tkinter` ni `customtkinter`.

### `utils/` — Lógica de negocio
- **Qué hace:** Cálculos estadísticos puros que reciben datos y retornan resultados (dicts, DataFrames, tuplas).
- **Qué NO hace:** Crear widgets, abrir ventanas, gestionar estado de la aplicación.
- **Dependencias externas:** `numpy`, `scipy`, `pandas`, `matplotlib` (solo `Figure`/`Axes`, nunca `plt.show()`).
- **Regla:** Nunca importar `tkinter` ni `customtkinter`. Todas las funciones son testeables de forma unitaria.

### `views/` — Interfaz gráfica
- **Qué hace:** Construir y mostrar la UI con CustomTkinter. Delegar eventos al controlador.
- **Qué NO hace:** Calcular estadísticas directamente, gestionar datos del modelo.
- **Dependencias externas:** `customtkinter`, `tkinter` (filedialog, ttk), `matplotlib.backends.backend_tkagg`.
- **Regla:** No tiene lógica de negocio. Recibe datos ya procesados del controlador para mostrarlos.

### `controllers/` — Coordinación
- **Qué hace:** Responder a eventos de la vista, llamar a utils/models, devolver resultados a la vista.
- **Dependencias externas:** `tkinter.filedialog`, `customtkinter` (para el diálogo de selección de hoja).
- **Regla:** Es el único lugar donde se conecta model + utils + view.

---

## Framework de UI: CustomTkinter

La UI usa **CustomTkinter 5.2.2** en modo oscuro (`ctk.set_appearance_mode("dark")`).

### Widgets CTK usados
| Widget CTK | Reemplaza |
|---|---|
| `ctk.CTkFrame` | `tk.Frame` / `ttk.Frame` |
| `ctk.CTkButton` | `tk.Button` / `ttk.Button` |
| `ctk.CTkEntry` | `tk.Entry` |
| `ctk.CTkLabel` | `tk.Label` |
| `ctk.CTkComboBox` | `ttk.Combobox` |
| `ctk.CTkScrollableFrame` | `tk.Frame` + `tk.Scrollbar` |
| `ctk.CTkTextbox` | `tk.Text` |
| `ctk.CTkRadioButton` | `tk.Radiobutton` |
| `ctk.CTkCheckBox` | `tk.Checkbutton` |
| `ctk.CTkToplevel` | `tk.Toplevel` |
| `CTkDropdown` (custom) | `tk.Menubutton` + `tk.Menu` |

### Widgets sin equivalente CTK (mantenidos con adaptación)
| Widget | Solución |
|---|---|
| `ttk.Treeview` | Mantenido con estilo `"Dark.Treeview"` definido en `theme.py` |
| `tk.Canvas` | Mantenido para el diagrama de árbol en `probability_panel.py` |

### Layout
- Todo usa `grid(sticky="nsew")` con `rowconfigure/columnconfigure(weight=)`.
- Eliminado completamente el uso de `place(relx=..., rely=...)`.

### Escalado de fuentes (multiplataforma)
```python
# views/theme.py
_SCALE = 1.15 if sys.platform == "darwin" else 1.0
FONT_TITLE   = ("Arial", scaled(18), "bold")
FONT_SECTION = ("Arial", scaled(12), "bold")
FONT_NORMAL  = ("Arial", scaled(11))
FONT_SMALL   = ("Arial", scaled(10))
FONT_MONO_SM = ("Courier New", scaled(9))
```

---

## Flujo de datos típico

```
Usuario hace clic en "Tabla Agrupada"
  → View notifica al Controller (callback)
    → Controller llama a Table.get_numeric_column(variable)
      → Controller llama a Trends.build_grouped_table(data)
        → Controller llama a Trends.freq_calculate(table, n)
          → Controller llama a Trends.append_totals(table)
            → Controller retorna DataFrame a la View
              → View renderiza el Treeview con los datos
```

---

## Regla de dependencias

```
main.py
  └── controllers/app_controller.py
        ├── models/table.py
        ├── utils/statistics.py
        ├── utils/trends.py
        ├── utils/graphs.py
        ├── utils/probability.py
        ├── utils/regression.py
        └── views/main_window.py
              ├── views/theme.py
              ├── views/components.py
              ├── views/statistics_panel.py
              ├── views/graphs_panel.py
              ├── views/probability_panel.py
              └── views/regression_panel.py
```

**Los `utils/` NUNCA importan tkinter ni customtkinter.**
**Los `models/` NUNCA importan tkinter ni customtkinter.**
**Los `views/` NO hacen cálculos estadísticos.**

---

## Principios SOLID aplicados

### S — Single Responsibility
- `Table`: solo estructura de datos (CRUD filas/columnas + cargar archivo por ruta).
- `Trends`: solo construir tablas de frecuencia agrupadas/no agrupadas.
- `CentralMeasures` / `DispersionMeasures`: solo calcular medidas estadísticas.
- `AppController`: coordinar flujo, no calcular ni dibujar.
- Cada panel de vista (`statistics_panel`, `graphs_panel`, etc.) tiene una sola área funcional.

### O — Open/Closed
- Para agregar un nuevo gráfico: añadir función en `utils/graphs.py` + método en `GraphsPanel`. Sin modificar existentes.

### L — Liskov Substitution
- Los paneles de vista son intercambiables si se decide cambiar de CTK a otro framework, sin afectar controladores.

### I — Interface Segregation
- La interfaz pública del controlador está dividida por dominio: tabla, columnas, filas, import, frecuencias, medidas.

### D — Dependency Inversion
- El controlador recibe el modelo por inyección en `__init__`. Las vistas reciben el controlador por inyección.

---

## Convenciones de código

- Nombres de clases: `PascalCase`
- Nombres de funciones y variables: `snake_case`
- Nombres de archivos: `snake_case.py`
- Idioma del código: **inglés** (variables, funciones, clases, docstrings)
- Idioma de la UI: **español** (textos visibles al usuario)
- Type hints en todas las funciones públicas
- Docstrings estilo Google en funciones de `utils/`

---

## Dependencias del proyecto

```
pandas>=1.5.0
numpy>=1.23.0
scipy>=1.9.0
matplotlib>=3.6.0
openpyxl>=3.0.0
python-dateutil>=2.8.0
customtkinter>=5.2.0
pytest>=7.0.0          # solo tests
```

`tkinter` y `ttk` son parte de la librería estándar de Python.
