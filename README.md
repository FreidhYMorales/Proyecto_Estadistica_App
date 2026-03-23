<<<<<<< HEAD
# Instalación de Dependencias

Antes de usar este proyecto, asegúrate de tener instaladas las siguientes librerías de Python:

<<<<<<< HEAD
1. `tkinter`  
2. `math`  
3. `pandas`  
4. `scipy`  
=======
1. `tkinter`
2. `math`
3. `pandas`
4. `scipy`
5. `numpy`
6. `matplotlib`
7. `openpyxl` (para importar archivos Excel)
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)

Si no las tienes, puedes instalarlas fácilmente copiando y pegando el siguiente comando en tu terminal:

```bash
<<<<<<< HEAD
pip install tkinter math pandas scipy

```

=======
pip install pandas scipy numpy matplotlib openpyxl

```

**Nota:** `tkinter` y `math` generalmente vienen preinstalados con Python.

>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
# Como correr el programa

Para poder correr el programa utilizar el comando en consola:

```bash
python app.py
<<<<<<< HEAD

```

Se utilizara este comando para ejecutar el programa hasta que se termine de integrar todas las funciones solicitadas.
=======
```

# Funcionalidades del Programa

Este programa de estadística descriptiva e inferencial incluye las siguientes funcionalidades:

## 📊 Tablas de Frecuencias
- Tabla de frecuencias agrupada (con intervalos)
- Tabla de frecuencias no agrupada (datos individuales)
- Importación de datos desde archivos Excel (.xlsx, .xls) y CSV

## 📈 Análisis Descriptivo

### Medidas de Tendencia Central
- Media aritmética, geométrica y armónica
- Mediana (interpolada y cruda)
- Moda (cruda e interpolada)

### Medidas de Posición
- Cuartiles (Q1, Q2, Q3)
- Deciles (D1-D9)
- Percentiles (P1-P99)

### Medidas de Dispersión
- Varianza (poblacional y muestral)
- Desviación estándar (poblacional y muestral)
- Rango y rango intercuartílico
- Coeficiente de variación

### Medidas de Forma
- Asimetría (coeficiente de sesgo)
- Curtosis (apuntamiento)

## 📊 Gráficos Estadísticos
- Histogramas
- Polígonos de frecuencia
- Ojivas (ascendentes y descendentes)
- Gráficos de barras
- Gráficos circulares (pie charts)
- Diagramas de caja (boxplots)
- Diagramas de dispersión

## 🎲 Probabilidades

### Probabilidades Elementales
- Sucesos simples
- Sucesos excluyentes
- Sucesos no excluyentes
- Sucesos independientes
- Sucesos dependientes

### Teorema de Bayes
- Cálculo de probabilidades condicionales

### Diagramas de Árbol
- Creación interactiva de diagramas de árbol
- Cálculo automático de probabilidades acumuladas
- Visualización de todas las ramas posibles

### Distribuciones de Probabilidad
- Distribución de Bernoulli
- Distribución Binomial
- Distribución de Poisson
- Distribución Normal (con cálculo de Z-scores)

## 📉 Correlación y Regresión

### Análisis de Correlación
- Correlación de Pearson (lineal)
- Correlación de Spearman (rangos)
- Coeficiente de determinación (r²)

### Regresión Simple
- Regresión lineal simple (Y = a + bX)
- Regresión exponencial (Y = a * e^(bX))
- Regresión logarítmica (Y = a + b*ln(X))
- Visualización de datos y línea de regresión
- Cálculo de errores (SSE, MSE, RMSE)

### Regresión Múltiple
- Regresión lineal múltiple (Y = β₀ + β₁X₁ + β₂X₂ + ... + βₙXₙ)
- Coeficiente de determinación ajustado (R² ajustado)
- Interpretación de coeficientes

## 🎨 Características de la Interfaz
- Interfaz gráfica intuitiva con tkinter
- Organización por módulos temáticos
- Gráficos interactivos embebidos con matplotlib
- Resultados detallados con interpretaciones estadísticas
- Exportación e importación de datos
>>>>>>> 7c28551 (Adding Version 2 to repo, starting modular architecture)
=======
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

## Instalación y ejecución

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

# Windows
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt

# O instalando el proyecto en modo editable (recomendado para desarrollo)
pip install -e ".[dev]"
```

### 4. Ejecutar la aplicación

```bash
cd "src/Estadistica Descriptiva"
python main.py
```

---

## Cómo ejecutar el programa

> Asegúrate de tener el entorno virtual **activado** antes de ejecutar.

### Linux / macOS

```bash
# Desde la raíz del proyecto
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

### Verificar que todo funciona antes de ejecutar

```bash
# Desde la raíz del proyecto (con el venv activo)
python -c "import customtkinter, matplotlib, pandas, scipy; print('OK')"
```

Si imprime `OK`, el entorno está listo. Si lanza un `ModuleNotFoundError`, ejecuta
`pip install -r requirements.txt` nuevamente.

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

# Con reporte de cobertura
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
>>>>>>> 87b4d89 (Adding Version 3 to repo)
