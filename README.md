# Estadística Descriptiva — v3

Aplicación de escritorio para análisis estadístico descriptivo, construida con Python y CustomTkinter. Desarrollada como proyecto académico para los cursos de Estadística I y II de la Universidad Mariano Gálvez, y como ejercicio práctico de arquitectura de software.

---

## Características

### Gestión de datos
- Creación manual de tablas con columnas numéricas o de cadena
- Importación de archivos **CSV** y **Excel** (`.xlsx` / `.xls`)
- Soporte para archivos Excel con **múltiples hojas** — selector interactivo al importar
- Edición de celdas y columnas en tiempo real

### Tablas de frecuencia
- Tabla de distribución **agrupada** (con intervalos calculados automáticamente)
- Tabla de distribución **no agrupada**
- Frecuencias absolutas, relativas, acumuladas y porcentuales

### Medidas estadísticas

| Categoría | Medidas |
|---|---|
| Tendencia central | Media aritmética, mediana, moda (cruda e interpolada), media geométrica, media armónica |
| Posición | Cuartiles Q1–Q3, deciles D1–D9, percentiles seleccionados |
| Dispersión | Rango, IQR, varianza poblacional/muestral, desviación estándar, coeficiente de variación |
| Forma | Asimetría (skewness), curtosis (kurtosis) con interpretación automática |

### Gráficos (Matplotlib integrado)
- **Frecuencia:** histograma, polígono de frecuencia, ojiva ascendente/descendente
- **Categórico:** gráfico de barras, gráfico circular
- **Comparativo:** diagrama de caja (boxplot multi-variable), diagrama de dispersión
- Barra de herramientas de matplotlib integrada (zoom, pan, guardar imagen)

### Probabilidad
- Probabilidad de sucesos simples, excluyentes y no excluyentes
- Teorema de Bayes
- **Diagrama de árbol interactivo** — añadir/eliminar nodos, visualizar ramas con probabilidades acumuladas
- Distribuciones: Bernoulli, Binomial, Poisson, Normal

### Regresión
- Correlación de Pearson y Spearman
- Regresión lineal simple, exponencial y logarítmica
- Regresión lineal múltiple
- Métricas de ajuste: R², R² ajustado, SSE, MSE, RMSE
- Panel de predicción interactivo

### Exportación
- Resultados de estadísticas a archivos `.txt`
- Gráficos exportables directamente desde la barra de matplotlib

---

## Requisitos

- **Python 3.11+**
- Las dependencias se listan en `requirements.txt` y `pyproject.toml`

| Paquete | Uso |
|---|---|
| `customtkinter` | Interfaz gráfica moderna con tema oscuro |
| `matplotlib` | Generación de gráficos estadísticos |
| `pandas` | Manejo de tablas de datos y DataFrames |
| `numpy` | Operaciones numéricas vectorizadas |
| `scipy` | Funciones estadísticas (correlación, distribuciones) |
| `openpyxl` | Lectura de archivos Excel |
| `python-dateutil` | Manejo de fechas |

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd Proyecto_Estadistica_App_V3
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows (CMD)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Cómo ejecutar el programa

> Asegúrate de tener el entorno virtual **activado** antes de ejecutar.

### Linux / macOS

```bash
source venv/bin/activate
cd "src/Estadistica Descriptiva"
python main.py
```

### Windows (CMD)

```cmd
venv\Scripts\activate
cd "src\Estadistica Descriptiva"
python main.py
```

### Windows (PowerShell)

```powershell
venv\Scripts\Activate.ps1
cd "src\Estadistica Descriptiva"
python main.py
```

> **Nota:** la carpeta `src/Estadistica Descriptiva` contiene un espacio en el nombre.
> Siempre enciérrala entre comillas al escribirla en la terminal.

### Verificar que el entorno está listo

```bash
python -c "import customtkinter, matplotlib, pandas, scipy; print('OK')"
```

Si imprime `OK`, el entorno está configurado correctamente. Si aparece un `ModuleNotFoundError`, ejecuta `pip install -r requirements.txt` nuevamente.

---

## Estructura del proyecto

```
Proyecto_Estadistica_App_V3/
├── pyproject.toml                        ← Metadatos y configuración del proyecto
├── requirements.txt                      ← Dependencias
├── README.md
├── CONTEXT/                              ← Documentación técnica interna
│   ├── ARCHITECTURE.md                   ← Arquitectura MVC y reglas de capas
│   ├── UI_COMPONENTS.md                  ← Referencia de widgets y layout
│   ├── BUGS_AND_ISSUES.md                ← Historial de bugs resueltos
│   ├── MIGRATION_PLAN.md                 ← Plan de migración V2 → V3 (completado)
│   └── V2_INVENTORY.md                   ← Inventario del código original
├── src/
│   └── Estadistica Descriptiva/          ← Paquete principal
│       ├── main.py                       ← Entry point
│       ├── models/
│       │   └── table.py                  ← Modelo de tabla (CRUD + importación)
│       ├── views/
│       │   ├── theme.py                  ← Tema, fuentes y constantes de UI
│       │   ├── components.py             ← Widgets reutilizables (CTkDropdown, GraphCanvas…)
│       │   ├── main_window.py            ← Ventana principal y navegación
│       │   ├── statistics_panel.py       ← Panel de dispersión y forma
│       │   ├── graphs_panel.py           ← Panel de gráficos
│       │   ├── probability_panel.py      ← Panel de probabilidad
│       │   └── regression_panel.py       ← Panel de regresión
│       ├── controllers/
│       │   └── app_controller.py         ← Controlador principal
│       └── utils/                        ← Lógica de negocio pura (sin UI)
│           ├── trends.py
│           ├── statistics.py
│           ├── graphs.py
│           ├── probability.py
│           └── regression.py
└── tests/
    ├── test_trends.py                    ← 14 tests
    ├── test_statistics.py                ← 13 tests
    ├── test_regression.py                ← 20 tests
    └── test_probability.py               ← 25 tests
```

---

## Arquitectura

El proyecto sigue el patrón **MVC** con separación estricta de capas:

```
views/          →  solo UI (CustomTkinter), sin cálculos
controllers/    →  coordinación entre modelo y vista
models/         →  estructura de datos, sin UI
utils/          →  funciones puras y testeables, sin UI
```

**Regla fundamental:** `utils/` y `models/` nunca importan `tkinter` ni `customtkinter`.

La navegación entre paneles usa `tkraise()` — todos los paneles se construyen una sola vez al iniciar y se alternan por z-order, preservando su estado entre navegaciones.

---

## Tests

```bash
# Desde la raíz del proyecto (con el venv activo)
pytest

# Con salida detallada
pytest -v
```

72 tests unitarios cubriendo todos los módulos de `utils/`.

---

## Versiones anteriores

| Versión | Descripción |
|---|---|
| V1 | Script monolítico, sin separación de responsabilidades |
| V2 | Múltiples archivos pero con lógica de negocio mezclada en la UI |
| **V3** | **Arquitectura MVC modular, CustomTkinter, tests unitarios** |
