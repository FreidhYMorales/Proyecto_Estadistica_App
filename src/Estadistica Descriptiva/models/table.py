import pandas as pd


class Table:
    """Data model for a statistical table with typed columns and rows."""

    def __init__(self, columns: list | None = None):
        if columns:
            self.columns = tuple(columns)
            self.rows = [tuple(["-"] * len(self.columns))]
        else:
            self.columns = ("Variable 1",)
            self.rows = [("-",)]

    # ── Column operations ───────────────────────────────────────────────────

    def add_column(self, column_name: str, values: list | None = None) -> None:
        if column_name in self.columns:
            raise ValueError(f"La columna '{column_name}' ya existe!")
        self.columns += (column_name,)
        if not self.rows:
            return
        if values is None:
            values = ["-"] * len(self.rows)
        elif len(values) != len(self.rows):
            raise ValueError("El número de valores no coincide con el número de filas!")
        self.rows = [row + (value,) for row, value in zip(self.rows, values)]

    def edit_column_name(self, old_name: str, new_name: str) -> None:
        if old_name not in self.columns:
            raise ValueError(f"La columna '{old_name}' no existe!")
        if new_name in self.columns:
            raise ValueError(f"La columna '{new_name}' ya existe!")
        idx = self.columns.index(old_name)
        self.columns = self.columns[:idx] + (new_name,) + self.columns[idx + 1:]

    def get_column(self, column_name: str) -> list:
        if column_name not in self.columns:
            raise ValueError(f"La columna '{column_name}' no existe!")
        idx = self.columns.index(column_name)
        return [row[idx] for row in self.rows]

    def get_numeric_column(self, column_name: str) -> list:
        """Returns only numeric float values from a column, filtering '-' and non-numeric."""
        result = []
        for value in self.get_column(column_name):
            try:
                if value != "-":
                    result.append(float(value))
            except (ValueError, TypeError):
                pass
        return result

    def delete_column(self, column_name: str) -> None:
        if column_name not in self.columns:
            raise ValueError(f"La columna '{column_name}' no existe!")
        idx = self.columns.index(column_name)
        self.columns = self.columns[:idx] + self.columns[idx + 1:]
        self.rows = [row[:idx] + row[idx + 1:] for row in self.rows]

    # ── Row operations ──────────────────────────────────────────────────────

    def add_row(self, row: list) -> None:
        if len(row) != len(self.columns):
            raise ValueError("La fila no coincide con el número de columnas.")
        self.rows.append(tuple(row))

    def get_all_rows(self) -> list:
        return list(self.rows)

    def get_row(self, row_index: int) -> tuple:
        if row_index < 0 or row_index >= len(self.rows):
            raise IndexError("Índice de fila fuera de rango!")
        return self.rows[row_index]

    def delete_row(self, row_index: int) -> None:
        if row_index < 0 or row_index >= len(self.rows):
            raise IndexError("Índice de fila fuera de rango!")
        del self.rows[row_index]

    # ── Cell operations ─────────────────────────────────────────────────────

    def edit_cell(self, row_index: int, column_name: str, new_value) -> None:
        if row_index < 0 or row_index >= len(self.rows):
            raise IndexError("Índice de fila fuera de rango!")
        if column_name not in self.columns:
            raise ValueError(f"Nombre de la columna no válida: '{column_name}'")
        col_idx = self.columns.index(column_name)
        row_list = list(self.rows[row_index])
        row_list[col_idx] = new_value
        self.rows[row_index] = tuple(row_list)

    # ── Serialization ───────────────────────────────────────────────────────

    def get_table_as_list(self) -> list:
        return [self.columns] + self.rows

    # ── File I/O ────────────────────────────────────────────────────────────

    def load_from_file(self, path: str, sheet_name=0) -> None:
        """Loads data from a CSV or Excel file. The path must be provided externally.
        sheet_name is only used for Excel files (default: first sheet)."""
        try:
            if path.endswith(".csv"):
                df = pd.read_csv(path)
            else:
                df = pd.read_excel(path, sheet_name=sheet_name)
            self.columns = tuple(df.columns)
            self.rows = [tuple(row) for row in df.values.tolist()]
        except Exception as e:
            raise RuntimeError(f"Error al importar archivo: {e}")

    def get_sheet_names(self, path: str) -> list:
        """Returns sheet names for an Excel file. Returns empty list for CSV."""
        if path.endswith(".csv"):
            return []
        try:
            return pd.ExcelFile(path).sheet_names
        except Exception:
            return []
