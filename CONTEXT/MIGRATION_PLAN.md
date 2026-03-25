# Plan de Migración V2 → V3

## Estado: COMPLETADA ✅ + Módulos inferenciales integrados

Migración de scripts monolíticos V2 a arquitectura MVC modular con CustomTkinter completada.
Sobre esa base se integraron los módulos de muestreo e inferencia del directorio `AGREGAR/`.

---

## Mapeo de módulos V2 → V3

| Archivo V2 | Responsabilidad | Destino en V3 | Estado |
|---|---|---|---|
| `Tabla.py` (estructura) | CRUD de columnas/filas | `models/table.py` | ✅ |
| `Tabla.py` (frecuencias) | Tablas agrupadas/no agrupadas | `utils/trends.py` | ✅ |
| `Tabla.py` (medidas centrales) | Media, mediana, moda, cuartiles... | `utils/statistics.py` | ✅ |
| `Visuals.py` (ventana principal) | Layout y navegación | `views/main_window.py` | ✅ |
| `Visuals.py` (widgets) | Componentes reutilizables | `views/components.py` | ✅ |
| `Visuals.py` (callbacks) | Coordinar model + view | `controllers/app_controller.py` | ✅ |
| `Statistics.py` (cálculos) | Dispersión, forma | `utils/statistics.py` | ✅ |
| `Statistics.py` (UI) | Panel de medidas | `views/statistics_panel.py` | ✅ |
| `Graphs.py` (generación) | Figuras matplotlib | `utils/graphs.py` | ✅ |
| `Graphs.py` (UI) | Panel de gráficos | `views/graphs_panel.py` | ✅ |
| `Probability.py` (cálculos) | Probabilidad, Bayes, distribuciones | `utils/probability.py` | ✅ |
| `Probability.py` (UI) | Panel con diagrama de árbol | `views/probability_panel.py` | ✅ |
| `Regression.py` (cálculos) | Correlación, regresión lin/exp/log/múltiple | `utils/regression.py` | ✅ |
| `Regression.py` (UI) | Panel de regresión | `views/regression_panel.py` | ✅ |
| `app_v2.py` | Entry point | `main.py` | ✅ |

---

## Fases completadas

### Fase 1 — Modelos y utilidades puras ✅
- [x] `models/table.py` — bug de slice en `delete_column` corregido
- [x] `utils/trends.py` — bug `*` en vez de `/` en `freq_calculate` corregido
- [x] `utils/statistics.py` — `CentralMeasures` + `DispersionMeasures` implementados
- [x] `utils/graphs.py` — 7 funciones que retornan `(fig, ax)` sin UI
- [x] `utils/probability.py` — cálculos de probabilidad y distribuciones (Bernoulli, Binomial, Poisson, Normal)
- [x] `utils/regression.py` — correlación Pearson/Spearman + regresión lineal/exp/log/múltiple

### Fase 2 — Vistas (CustomTkinter) ✅
- [x] `views/theme.py` — apariencia dark, constantes de fuente/padding con escalado multiplataforma
- [x] `views/components.py` — `CTkDropdown`, `ResultTextWidget`, `DataTreeview`, `GraphCanvas`
- [x] `views/main_window.py` — `Sidebar`, `DataTable`, layout responsive con grid weights
- [x] `views/statistics_panel.py` — dispersión, forma, resumen completo
- [x] `views/graphs_panel.py` — histograma, polígono, ojiva, barras, circular, boxplot, dispersión
- [x] `views/probability_panel.py` — árbol de probabilidad, sucesos, Bayes, distribuciones
- [x] `views/regression_panel.py` — correlación, regresión simple/múltiple, predicción

### Fase 3 — Controladores ✅
- [x] `controllers/app_controller.py` — tabla, columnas, filas, import (con selector de hoja CTK), frecuencias, medidas estadísticas

### Fase 4 — Tests e integración ✅
- [x] `tests/conftest.py`
- [x] `tests/test_trends.py` — 14 tests
- [x] `tests/test_statistics.py` — 13 tests
- [x] `tests/test_regression.py` — 20 tests
- [x] `tests/test_probability.py` — 25 tests
- [x] `requirements.txt` actualizado con `customtkinter>=5.2.0` y `pytest>=7.0.0`

### Mejoras adicionales implementadas (post-migración)
- [x] **#1** Acceso unificado a columnas a través del controlador (la vista no accede al modelo directamente)
- [x] **#2** `linear_regression()` retorna los arrays originales `x` e `y` para graficar
- [x] **#3** 72 tests unitarios para todos los módulos `utils/`
- [x] **#4** Diagrama de árbol optimizado con `canvas.itemconfig()` en lugar de redibujado completo
- [x] **#5** Selector de hoja para Excel con múltiples hojas (CTkToplevel + CTkRadioButton)
- [x] **#6** Exportar resultados a `.txt` desde todos los paneles de resultados

---

### Fase 5 — Integración de módulos inferenciales (desde `AGREGAR/`) ✅

Los archivos de la carpeta `AGREGAR/estadistica proyecto/estadistica/` contenían lógica
estadística inferencial en formato consola. Se adaptaron e integraron en la arquitectura MVC.

#### Fuentes del directorio `AGREGAR/`
| Archivo origen | Clases/funciones | Destino en V3 | Cambios |
|---|---|---|---|
| `sampling_methods.py` | `MetodosMuestreo` (MAS, sistemático, estratificado) | `utils/sampling.py` | Sin cambios sustanciales (ya MVC-compatible) |
| `confidence_intervals.py` | `IntervalosConfianza` | `utils/inference.py` | Sin cambios sustanciales |
| `sample_size.py` | `CalculadorTamanioMuestra` | `utils/inference.py` | Sin cambios sustanciales |
| `visualizer.py` | `Visualizador` (5 gráficos) | `utils/inference_graphs.py` | Refactorizado: `plt.show()` → `Figure` + retorna `(fig, ax)` |
| `data_loader.py` | `CargadorDatos` | ❌ No integrado | Duplica `Table.load_from_file()` ya existente |
| `main.py` (consola) | Menú principal | ❌ No integrado | Reemplazado por paneles GUI |
| `12_muestreo_no_probabilistico.py` | Conveniencia, cuotas, bola de nieve, juicio | `utils/sampling.py` | Adaptado como clase `MuestreoNoProbabilistico` |

#### Nuevos archivos creados
| Archivo | Descripción |
|---|---|
| `utils/sampling.py` | `MetodosMuestreo`, `MuestreoNoProbabilistico`, `ErroresMuestreo` |
| `utils/inference.py` | `IntervalosConfianza`, `CalculadorTamanioMuestra` |
| `utils/inference_graphs.py` | 4 funciones de gráficos inferencial que retornan `(fig, ax)` |
| `views/sampling_panel.py` | `SamplingPanel` — muestreo probabilístico + no probabilístico + errores |
| `views/inference_panel.py` | `InferencePanel` — IC (proporción, media Z/t) + tamaño de muestra |

#### Modificaciones en archivos existentes
| Archivo | Cambio |
|---|---|
| `models/table.py` | Agregado `to_dataframe()` — expone los datos como `pd.DataFrame` para el muestreo estratificado y por cuotas |
| `controllers/app_controller.py` | 13 nuevos métodos en 3 dominios: muestreo probabilístico (3), muestreo no probabilístico (4), inferencia/IC (4), errores (2) |
| `views/main_window.py` | `ContentStack` + 2 paneles nuevos; Sidebar: sección "MUESTREO E INFERENCIA" con 2 botones; `_BTN_COLORS` y `_LABELS` ampliados |

---

## Archivos renombrados
| Nombre V2/incorrecto | Nombre correcto |
|---|---|
| `utils/regressino.py` | `utils/regression.py` ✅ |
| `views/compenents.py` | `views/components.py` ✅ |
