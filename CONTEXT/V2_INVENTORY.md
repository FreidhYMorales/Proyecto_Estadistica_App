# Inventario del código V2

Este documento describe qué hace cada módulo de V2, qué parte pertenece al dominio
y qué parte es UI. Sirve como referencia histórica de la migración a V3.

**Estado:** Migración completada. Todos los módulos han sido migrados. ✅

---

## `app_v2.py` — Entry point ✅

```python
def main():
    data_table = Tabla.Tabla()
    app_window = Visuals.WindowSet("Estadística Descriptiva", data_table)
    app_window.running()
```

**Migrado a:** `main.py` + `AppController` + `MainWindow`.

---

## `Tabla.py` → `models/table.py` + `utils/trends.py` + `utils/statistics.py` ✅

### Parte 1: Estructura de datos (→ `models/table.py`)
| Método V2 | Método V3 | Estado |
|---|---|---|
| `__init__(columnas)` | `__init__(columns)` | ✅ |
| `agregar_columna(nombre, valores)` | `add_column(name, values)` | ✅ |
| `edit_column_name(old, new)` | `edit_column_name(old, new)` | ✅ (bug f-string corregido) |
| `agregar_fila(fila)` | `add_row(row)` | ✅ |
| `editar_celda(idx, col, val)` | `edit_cell(idx, col, val)` | ✅ |
| `eliminar_fila(idx)` | `delete_row(idx)` | ✅ |
| `eliminar_columna(nombre)` | `delete_column(name)` | ✅ (bug slice corregido) |
| `obtener_filas()` | `get_all_rows()` | ✅ (renombrado por claridad) |
| `obtener_fila(idx)` | `get_row(idx)` | ✅ (renombrado por claridad) |
| `obtener_columna(nombre)` | `get_column(name)` | ✅ |
| `importar_archivo()` | `load_from_file(path, sheet_name)` | ✅ (SRP: sin diálogo UI) |
| — | `get_sheet_names(path)` | ✅ (nuevo: soporte multi-hoja) |
| — | `get_numeric_column(name)` | ✅ (nuevo: filtrado de no-numéricos) |

### Parte 2: Tablas de frecuencia (→ `utils/trends.py`)
| Método V2 | Método V3 | Estado |
|---|---|---|
| `construir_tabla_agrupada(datos, intervalo)` | `Trends.build_grouped_table(data)` | ✅ |
| `calcular_frecuencias(tabla, n)` | `Trends.freq_calculate(table, n)` | ✅ (bug `/` corregido) |
| `agregar_totales_para_visual(tabla)` | `Trends.append_totals(table)` | ✅ |
| `mostrar_tabla_completa_ordenada(datos)` | `Trends.build_ungrouped_table(data)` | ✅ |

### Parte 3: Medidas centrales e interpolación (→ `utils/statistics.py`)
| Método V2 | Método V3 | Estado |
|---|---|---|
| `interpolar_valor(tabla, n, intervalo, pct)` | `CentralMeasures._interpolate(...)` | ✅ |
| `medidas_central(root, ...)` | `CentralMeasures.calculate(data, table, n, interval, df)` | ✅ (separado de UI) |

**Medidas calculadas:**
- Media aritmética, mediana, moda (interpolada y cruda)
- Media geométrica (`scipy.stats.gmean`), media armónica (`scipy.stats.hmean`)
- Q1, Q2, Q3
- Deciles D1–D9
- Percentiles seleccionados (1, 5, 10, 25, 50, 75, 90, 95, 99)

---

## `Statistics.py` → `utils/statistics.py` + `views/statistics_panel.py` ✅

### Cálculos puros (→ `utils/statistics.py`)
| Método V2 | Método V3 | Retorna |
|---|---|---|
| `calcular_medidas_dispersion(datos)` | `DispersionMeasures.calculate_dispersion(data)` | dict: n, mean, variance_population/sample, std, range, min, max, q1, q3, iqr, cv |
| `calcular_medidas_forma(datos)` | `DispersionMeasures.calculate_shape(data)` | dict: skewness, kurtosis, skewness_label, kurtosis_label |

### UI (→ `views/statistics_panel.py`)
- `StatisticsPanel` con `CTkDropdown` toolbar
- Paneles: dispersión, forma, resumen completo
- Exportación a `.txt` desde cada panel
- `ResultTextWidget` (CTkTextbox) para mostrar resultados

---

## `Graphs.py` → `utils/graphs.py` + `views/graphs_panel.py` ✅

### Funciones en `utils/graphs.py` (todas retornan `(fig, ax)`)
| Función | Tipo de gráfico |
|---|---|
| `build_histogram(data, bins, variable_name)` | Frecuencia |
| `build_frequency_polygon(data, bins, variable_name)` | Frecuencia |
| `build_ogive(data, ascending, variable_name)` | Frecuencia acumulada |
| `build_bar_chart(data, variable_name)` | Categórico |
| `build_pie_chart(data, max_categories, variable_name)` | Categórico |
| `build_boxplot(data_groups, labels)` | Comparativo |
| `build_scatter(x, y, x_name, y_name)` | Comparativo |

### UI (→ `views/graphs_panel.py`)
- `GraphsPanel` con 3 `CTkDropdown` en toolbar (Frecuencia, Categórico, Comparativo)
- `GraphCanvas` embebe `FigureCanvasTkAgg` dentro de `ctk.CTkFrame`
- Selección múltiple para boxplot: `CTkScrollableFrame` + `CTkCheckBox` por columna

---

## `Probability.py` → `utils/probability.py` + `views/probability_panel.py` ✅

### Cálculos en `utils/probability.py`
| Función | Descripción |
|---|---|
| `simple_probability(cases, total)` | P(A) = casos/total |
| `exclusive_probability(events)` | P(A ∪ B) = P(A) + P(B) |
| `bayes_theorem(prior, likelihood, evidence)` | Teorema de Bayes |
| `bernoulli(p, k)` | P(X=k) distribución Bernoulli |
| `binomial(n, p, k)` | P(X=k) distribución Binomial |
| `poisson(lambda_, k)` | P(X=k) distribución Poisson |
| `normal_cdf(mu, sigma, x)` | P(X ≤ x) distribución Normal |

### UI (→ `views/probability_panel.py`)
- Diagrama de árbol en `tk.Canvas` (no tiene equivalente CTK)
- Optimizado: actualiza nodos con `canvas.itemconfig()` sin redibujar todo el árbol
- Paneles de distribuciones con `CTkDropdown`
- Selector de sucesos con `CTkScrollableFrame` + `CTkCheckBox`

---

## `Regression.py` → `utils/regression.py` + `views/regression_panel.py` ✅

### Cálculos en `utils/regression.py`
| Función | Retorna |
|---|---|
| `pearson_correlation(x, y)` | dict: r, p_value, interpretación |
| `spearman_correlation(x, y)` | dict: rho, p_value, interpretación |
| `linear_regression(x, y)` | dict: a, b, r2, sse, mse, rmse, **x, y** (arrays originales) |
| `exponential_regression(x, y)` | dict: a, b, r2, ecuación |
| `logarithmic_regression(x, y)` | dict: a, b, r2, ecuación |
| `multiple_regression(X, y)` | dict: coefs, r2, r2_adj, sse, mse, rmse |
| `predict_linear(a, b, x_value)` | float |

> Nota: `linear_regression()` incluye los arrays `x` e `y` originales en el dict resultado
> para que la vista pueda graficar los puntos junto con la línea de regresión sin acceder
> al modelo directamente.

### UI (→ `views/regression_panel.py`)
- Selector de variables múltiples: `CTkScrollableFrame` + `CTkCheckBox`
- Panel de predicción con `ctk.CTkFrame` como tarjeta
- `CTkDropdown` para 3 categorías: Correlación, Regresión Simple, Regresión Múltiple

---

## Patrones reutilizables de V2 — resueltos en V3

| Patrón V2 | Solución V3 |
|---|---|
| `obtener_datos_numericos()` duplicado en Graphs + Regression | `Table.get_numeric_column(name)` en el modelo |
| `crear_figura_en_frame()` en Graphs y Regression | `GraphCanvas` en `views/components.py` |
| `clear_frame()` duplicado en 4 módulos | `clear_frame()` en `views/components.py` |
| `tk.Menubutton` + `tk.Menu` en 4 paneles | `CTkDropdown` en `views/components.py` |
| `tk.Text` para resultados en 3 paneles | `ResultTextWidget` (CTkTextbox) en `views/components.py` |
