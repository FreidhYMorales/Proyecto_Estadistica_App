from tkinter import filedialog
import customtkinter as ctk

from models.table import Table
from utils.trends import Trends
from utils.statistics import CentralMeasures, DispersionMeasures


class AppController:
    """
    Orchestrates interactions between the data model and the view.

    The view calls controller methods; the controller calls models and utils,
    returning plain Python data structures (dicts, DataFrames, lists) to the view.
    """

    def __init__(self):
        self.table = Table()

    # ── Table data ──────────────────────────────────────────────────────────

    @property
    def columns(self) -> tuple:
        return self.table.columns

    def get_all_rows(self) -> list:
        return self.table.get_all_rows()

    def get_column(self, column_name: str) -> list:
        return self.table.get_column(column_name)

    def get_numeric_column(self, column_name: str) -> list:
        return self.table.get_numeric_column(column_name)

    # ── Column operations ───────────────────────────────────────────────────

    def add_column(self, name: str) -> None:
        self.table.add_column(name)

    def rename_column(self, old_name: str, new_name: str) -> None:
        self.table.edit_column_name(old_name, new_name)

    def delete_column(self, name: str) -> None:
        self.table.delete_column(name)

    # ── Row / cell operations ───────────────────────────────────────────────

    def add_empty_row(self) -> None:
        self.table.add_row(["-"] * len(self.table.columns))

    def edit_cell(self, row_index: int, column_name: str, value: str) -> None:
        self.table.edit_cell(row_index, column_name, value)

    def delete_row(self, row_index: int) -> None:
        self.table.delete_row(row_index)

    # ── File import ─────────────────────────────────────────────────────────

    def import_file(self) -> bool:
        """Opens a file dialog and loads the selected file into the table.
        For Excel files with multiple sheets, shows a sheet selector dialog.
        Returns True if a file was loaded, False if the user cancelled."""
        path = filedialog.askopenfilename(
            title="Selecciona un archivo para importar",
            filetypes=(
                ("Archivos Excel", "*.xlsx *.xls"),
                ("Archivos CSV", "*.csv"),
                ("Todos los archivos", "*.*"),
            ),
        )
        if not path:
            return False

        sheet_names = self.table.get_sheet_names(path)
        if len(sheet_names) > 1:
            sheet = self._ask_sheet(sheet_names)
            if sheet is None:
                return False
        else:
            sheet = 0

        self.table.load_from_file(path, sheet_name=sheet)
        return True

    def _ask_sheet(self, sheet_names: list) -> str | None:
        """Shows a CTK modal dialog to choose an Excel sheet. Returns the chosen name or None."""
        result = [None]

        win = ctk.CTkToplevel()
        win.title("Seleccionar hoja")
        win.resizable(False, False)
        win.grab_set()

        ctk.CTkLabel(win, text="El archivo tiene varias hojas.\nSelecciona cuál importar:",
                     font=("Arial", 11)).pack(padx=20, pady=(15, 5))

        scroll = ctk.CTkScrollableFrame(win, width=260,
                                        height=min(len(sheet_names), 8) * 32,
                                        fg_color=("gray80", "gray22"))
        scroll.pack(padx=20, pady=5, fill="x")

        radio_var = ctk.StringVar(value=sheet_names[0])
        for name in sheet_names:
            ctk.CTkRadioButton(scroll, text=name, variable=radio_var,
                               value=name, font=("Arial", 11)).pack(anchor="w", pady=2)

        def confirm():
            result[0] = radio_var.get()
            win.destroy()

        def cancel():
            win.destroy()

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=(5, 15))
        ctk.CTkButton(btn_frame, text="Importar", command=confirm, width=100,
                      font=("Arial", 11)).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Cancelar", command=cancel, width=100,
                      font=("Arial", 11),
                      fg_color=("gray65", "gray35")).pack(side="left", padx=5)

        win.wait_window()
        return result[0]

    # ── Frequency tables ────────────────────────────────────────────────────

    def get_grouped_table(self, column_name: str):
        """Returns a grouped frequency DataFrame ready for display."""
        data = self.table.get_numeric_column(column_name)
        if not data:
            raise ValueError(f"No hay datos numéricos en '{column_name}'.")
        table, n, interval, _ = Trends.build_grouped_table(data)
        table = Trends.freq_calculate(table, n)
        return Trends.append_totals(table)

    def get_ungrouped_table(self, column_name: str):
        """Returns a non-grouped frequency DataFrame ready for display."""
        data = self.table.get_numeric_column(column_name)
        if not data:
            raise ValueError(f"No hay datos numéricos en '{column_name}'.")
        return Trends.build_ungrouped_table(data)

    # ── Statistical measures ────────────────────────────────────────────────

    def get_central_measures(self, column_name: str) -> dict:
        """Returns a dict with all central tendency measures."""
        data = self.table.get_numeric_column(column_name)
        if len(data) < 2:
            raise ValueError("Se necesitan al menos 2 valores numéricos.")
        table, n, interval, df = Trends.build_grouped_table(data)
        table = Trends.freq_calculate(table, n)
        return CentralMeasures.calculate(data, table, n, interval, df)

    def get_dispersion_measures(self, column_name: str) -> dict:
        """Returns a dict with dispersion measures."""
        data = self.table.get_numeric_column(column_name)
        if len(data) < 2:
            raise ValueError("Se necesitan al menos 2 valores numéricos.")
        return DispersionMeasures.calculate_dispersion(data)

    def get_shape_measures(self, column_name: str) -> dict:
        """Returns a dict with shape measures (skewness, kurtosis)."""
        data = self.table.get_numeric_column(column_name)
        if len(data) < 3:
            raise ValueError("Se necesitan al menos 3 valores numéricos.")
        return DispersionMeasures.calculate_shape(data)

    def get_full_summary(self, column_name: str) -> dict:
        """Returns combined dispersion + shape measures."""
        data = self.table.get_numeric_column(column_name)
        if len(data) < 3:
            raise ValueError("Se necesitan al menos 3 valores numéricos.")
        return {
            **DispersionMeasures.calculate_dispersion(data),
            **DispersionMeasures.calculate_shape(data),
        }
