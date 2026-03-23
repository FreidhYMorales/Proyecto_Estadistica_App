# Bugs y Problemas Identificados

## Bugs de V3 — RESUELTOS ✅

### BUG-001 — `models/table.py`: `delete_column` con slice incorrecto ✅ RESUELTO
**Severidad:** Alta — corrompe los datos silenciosamente.

```python
# INCORRECTO
self.rows = [row[:column_index] + row[: column_index + 1 :] for row in self.rows]

# CORRECTO
self.rows = [row[:column_index] + row[column_index + 1:] for row in self.rows]
```
`row[: column_index + 1 :]` incluía el elemento a eliminar en lugar de excluirlo.

---

### BUG-002 — `utils/trends.py`: `freq_calculate` con `*` en lugar de `/` ✅ RESUELTO
**Severidad:** Alta — frecuencias acumuladas completamente erróneas.

```python
# INCORRECTO
table["Fa%"] = (table["Fa"] * n * 100).round(2)

# CORRECTO
table["Fa%"] = (table["Fa"] / n * 100).round(2)
```

---

### BUG-003 — `models/table.py`: `edit_column_name` con f-string mal formada ✅ RESUELTO
**Severidad:** Baja — mensaje de error no interpolaba la variable.

```python
# INCORRECTO
raise ValueError("La columna '{new_name}' ya existe!")

# CORRECTO
raise ValueError(f"La columna '{new_name}' ya existe!")
```

---

### BUG-004 — `models/table.py`: nombres `get_row` / `get_rows` invertidos ✅ RESUELTO
**Severidad:** Baja — API semánticamente confusa.
Renombrados a `get_all_rows()` (todas las filas) y `get_row(index)` (una fila por índice).

---

### BUG-005 — `controllers/app_controller.py`: `_ask_sheet` usaba `listbox.curselection()` ✅ RESUELTO
**Severidad:** Alta — crash al importar Excel con múltiples hojas.

Después de migrar `tk.Listbox` a `ctk.CTkScrollableFrame + ctk.CTkRadioButton`,
la función `confirm()` seguía referenciando `listbox` (variable inexistente).

```python
# INCORRECTO
def confirm():
    sel = listbox.curselection()   # NameError: listbox no existe
    if sel:
        result[0] = sheet_names[sel[0]]

# CORRECTO
def confirm():
    result[0] = radio_var.get()    # StringVar del CTkRadioButton seleccionado
```

---

## Errores de nomenclatura en V3 — RESUELTOS ✅

| Nombre incorrecto | Nombre correcto |
|---|---|
| `utils/regressino.py` | `utils/regression.py` ✅ |
| `views/compenents.py` | `views/components.py` ✅ |

---

## Problemas de diseño de V2 — NO REPETIDOS EN V3 ✅

### DESIGN-001 — `Table.import_file()` abría diálogo de UI ✅
El modelo ya no abre diálogos. `filedialog.askopenfilename()` vive en `AppController.import_file()`.
El modelo solo expone `load_from_file(path, sheet_name)`.

### DESIGN-002 — Flag `is_embedded` mezclaba dos modos de operación ✅
Eliminado. En V3, la vista siempre es embeddable. Los paneles se instancian en su frame contenedor.

### DESIGN-003 — `clear_frame` duplicado en 4 módulos ✅
Centralizado en `views/components.py` como función `clear_frame(frame)`.

### DESIGN-004 — Medidas centrales mezcladas con UI ✅
`utils/statistics.py` solo retorna dicts con resultados. La vista formatea y muestra.

### DESIGN-005 — Acoplamiento entre `Visuals.py` y todos los módulos ✅
El controlador es quien conoce los módulos de utils. Las vistas reciben el controlador por inyección.

---

## Issues conocidos (pendientes)

No hay bugs conocidos activos. Si se detecta alguno, documentarlo aquí con severidad y pasos para reproducir.
