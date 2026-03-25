from tkinter import filedialog
from typing import Optional, List
import customtkinter as ctk

from models.table import Table
from utils.trends import Trends
from utils.statistics import CentralMeasures, DispersionMeasures
from utils.sampling import MetodosMuestreo, MuestreoNoProbabilistico, ErroresMuestreo
from utils.inference import IntervalosConfianza, CalculadorTamanioMuestra


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

    def get_dataframe(self):
        """Returns the full table as a pandas DataFrame."""
        return self.table.to_dataframe()

    # ── Sampling ─────────────────────────────────────────────────────────────

    def sampling_simple(self, column_name: str, n: int, reemplazo: bool = False) -> dict:
        """Aleatorio simple sobre los datos numéricos de una columna."""
        data = self.table.get_numeric_column(column_name)
        if not data:
            raise ValueError(f"No hay datos numéricos en '{column_name}'.")
        mm = MetodosMuestreo()
        return mm.aleatorio_simple(data, n, reemplazo)

    def sampling_systematic(self, column_name: str, n: int) -> dict:
        """Muestreo sistemático sobre los datos numéricos de una columna."""
        data = self.table.get_numeric_column(column_name)
        if not data:
            raise ValueError(f"No hay datos numéricos en '{column_name}'.")
        mm = MetodosMuestreo()
        return mm.sistematico(data, n)

    def sampling_stratified(
        self,
        strata_col: str,
        n_total: int,
        tipo: str = "proporcional",
        variable_col: Optional[str] = None,
    ) -> dict:
        """Muestreo estratificado sobre el DataFrame completo."""
        df = self.table.to_dataframe()
        if df.empty:
            raise ValueError("No hay datos cargados.")
        mm = MetodosMuestreo()
        return mm.estratificado(df, strata_col, n_total, tipo, variable_col)

    def sampling_conglomerados(self, cluster_col: str, k: int) -> dict:
        """Muestreo por conglomerados: selecciona k grupos completos al azar."""
        df = self.table.to_dataframe()
        if df.empty:
            raise ValueError("No hay datos cargados.")
        mm = MetodosMuestreo()
        return mm.conglomerados(df, cluster_col, k)

    # ── Confidence Intervals ─────────────────────────────────────────────────

    def ic_proporcion(
        self, exitos: int, n: int, nivel_confianza: float = 0.95, metodo: str = "normal"
    ) -> dict:
        """IC para proporción poblacional."""
        ic = IntervalosConfianza(nivel_confianza)
        return ic.ic_proporcion(exitos, n, metodo)

    def ic_media_z(
        self, media: float, sigma: float, n: int, nivel_confianza: float = 0.95
    ) -> dict:
        """IC para media con σ conocida (distribución Z)."""
        ic = IntervalosConfianza(nivel_confianza)
        return ic.ic_media_sigma_conocida(media, sigma, n)

    def ic_media_t_datos(self, datos: List[float], nivel_confianza: float = 0.95) -> dict:
        """IC para media con σ desconocida, calculado desde datos muestrales."""
        ic = IntervalosConfianza(nivel_confianza)
        return ic.ic_media_sigma_desconocida(datos=datos)

    def ic_varianza(
        self,
        nivel_confianza: float = 0.95,
        datos: Optional[List[float]] = None,
        desv_muestral: Optional[float] = None,
        n: Optional[int] = None,
    ) -> dict:
        """IC para varianza poblacional (distribución chi-cuadrada)."""
        ic = IntervalosConfianza(nivel_confianza)
        return ic.ic_varianza(datos, desv_muestral, n)

    def ic_media_t_manual(
        self,
        media: float,
        desv: float,
        n: int,
        nivel_confianza: float = 0.95,
    ) -> dict:
        """IC para media con σ desconocida, valores ingresados manualmente."""
        ic = IntervalosConfianza(nivel_confianza)
        return ic.ic_media_sigma_desconocida(media_muestral=media, desv_muestral=desv, n=n)

    # ── Sample Size ───────────────────────────────────────────────────────────

    def sample_size_proportion(
        self,
        margen_error: float,
        proporcion_esperada: float = 0.5,
        nivel_confianza: float = 0.95,
        poblacion: Optional[int] = None,
        perdidas: Optional[float] = None,
    ) -> dict:
        """Tamaño de muestra para estimar una proporción."""
        calc = CalculadorTamanioMuestra(nivel_confianza)
        return calc.para_proporcion(margen_error, proporcion_esperada, poblacion, perdidas)

    def sample_size_mean(
        self,
        margen_error: float,
        desv_estandar: float,
        nivel_confianza: float = 0.95,
        poblacion: Optional[int] = None,
        perdidas: Optional[float] = None,
    ) -> dict:
        """Tamaño de muestra para estimar una media."""
        calc = CalculadorTamanioMuestra(nivel_confianza)
        return calc.para_media(margen_error, desv_estandar, poblacion, perdidas)

    # ── Non-probabilistic Sampling ────────────────────────────────────────────

    def sampling_conveniencia(self, column_name: str, n: int, inicio: int = 0) -> dict:
        """Muestreo por conveniencia: primeros n elementos desde 'inicio'."""
        data = self.table.get_numeric_column(column_name)
        if not data:
            raise ValueError(f"No hay datos numéricos en '{column_name}'.")
        return MuestreoNoProbabilistico.conveniencia(data, n, inicio)

    def sampling_juicio(
        self, column_name: str, indices: List[int], criterio: str = ""
    ) -> dict:
        """Muestreo por juicio: selección manual de índices por el investigador."""
        data = self.table.get_numeric_column(column_name)
        if not data:
            raise ValueError(f"No hay datos numéricos en '{column_name}'.")
        return MuestreoNoProbabilistico.juicio(data, indices, criterio)

    def sampling_cuotas(
        self,
        strata_col: str,
        cuotas: Optional[dict] = None,
        n_total: Optional[int] = None,
    ) -> dict:
        """Muestreo por cuotas: primeros n_h elementos de cada estrato (no aleatorio)."""
        df = self.table.to_dataframe()
        if df.empty:
            raise ValueError("No hay datos cargados.")
        return MuestreoNoProbabilistico.por_cuotas(df, strata_col, cuotas, n_total)

    def sampling_bola_de_nieve(
        self,
        column_name: str,
        indices_semilla: List[int],
        n_ondas: int,
        refs_por_onda: int,
    ) -> dict:
        """Muestreo bola de nieve: expansión por referidos desde índices semilla."""
        data = self.table.get_numeric_column(column_name)
        if not data:
            raise ValueError(f"No hay datos numéricos en '{column_name}'.")
        mm = MuestreoNoProbabilistico()
        return mm.bola_de_nieve(data, indices_semilla, n_ondas, refs_por_onda)

    # ── Sampling Errors ───────────────────────────────────────────────────────

    def errores_media(
        self,
        column_name: str,
        nivel_confianza: float = 0.95,
        N: Optional[int] = None,
        mu: Optional[float] = None,
    ) -> dict:
        """Calcula errores de muestreo para la media de una columna."""
        datos = self.table.get_numeric_column(column_name)
        if len(datos) < 2:
            raise ValueError("Se necesitan al menos 2 valores numéricos.")
        em = ErroresMuestreo(nivel_confianza)
        return em.para_media(datos=datos, N=N, mu=mu)

    def errores_proporcion(
        self,
        exitos: int,
        n: int,
        nivel_confianza: float = 0.95,
        N: Optional[int] = None,
        p_real: Optional[float] = None,
    ) -> dict:
        """Calcula errores de muestreo para una proporción."""
        em = ErroresMuestreo(nivel_confianza)
        return em.para_proporcion(exitos, n, N, p_real)
