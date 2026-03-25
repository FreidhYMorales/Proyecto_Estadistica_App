"""
Main application window built with CustomTkinter.

Layout
------
┌──────────────┬─────────────────────────────────────────────────┐
│              │  DataTable          (row 0, weight=2, min=180)  │
│   Sidebar    ├─────────────────────────────────────────────────┤
│  (col 0,     │  ContentToolbar     (row 1, fixed 32 px)        │
│   fixed w)   ├─────────────────────────────────────────────────┤
│              │  ContentStack       (row 2, weight=3, min=380)  │
│              │  [all panels stacked here, switched via raise]  │
└──────────────┴─────────────────────────────────────────────────┘

Navigation strategy
────────────────────
Panels are built ONCE at startup and placed in the same grid cell of ContentStack.
Switching is done with tkraise() — no widgets are destroyed, state is preserved
between navigation events (selected variables, generated graphs, drawn tree nodes).
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk

from views.theme import (
    FONT_TITLE, FONT_SECTION, FONT_SMALL,
    PAD_XS, PAD_S, PAD_M, PAD_L,
    apply_treeview_dark_style,
)
from views.components import clear_frame, DataTreeview
from views.statistics_panel import StatisticsPanel
from views.graphs_panel import GraphsPanel
from views.probability_panel import ProbabilityPanel
from views.regression_panel import RegressionPanel
from views.sampling_panel import SamplingPanel
from views.inference_panel import InferencePanel


# ── ContentToolbar ────────────────────────────────────────────────────────────

class ContentToolbar(ctk.CTkFrame):
    """
    Thin breadcrumb bar between the data table and the content stack.
    Shows the active panel name and optional contextual action buttons.
    """

    _LABELS: dict[str, str] = {
        "freq":      "Tablas de Frecuencia",
        "central":   "Medidas de Tendencia Central",
        "stats":     "Dispersión y Forma",
        "graphs":    "Gráficos Estadísticos",
        "prob":      "Probabilidad",
        "reg":       "Regresión",
        "sampling":  "Muestreo Probabilístico",
        "inference": "Inferencia Estadística",
    }

    def __init__(self, parent, **kwargs):
        super().__init__(parent, height=32, corner_radius=0,
                         fg_color=("gray83", "gray20"), **kwargs)
        self.grid_propagate(False)      # enforce fixed height
        self.columnconfigure(1, weight=1)

        self._dot = ctk.CTkLabel(
            self, text="▶", font=FONT_SMALL,
            text_color=("#1f6aa5", "#4d9de0"),
        )
        self._dot.grid(row=0, column=0, padx=(PAD_M, PAD_XS), sticky="w")

        self._title = ctk.CTkLabel(
            self, text="─", font=FONT_SMALL,
            text_color=("gray35", "gray65"), anchor="w",
        )
        self._title.grid(row=0, column=1, padx=(0, PAD_M), sticky="w")

        self._actions = ctk.CTkFrame(self, fg_color="transparent")
        self._actions.grid(row=0, column=2, padx=PAD_S, sticky="e")

    def set_panel(self, key: str, actions: list[tuple[str, callable]] | None = None) -> None:
        """Update the breadcrumb label and rebuild action buttons."""
        self._title.configure(text=self._LABELS.get(key, key))
        for w in self._actions.winfo_children():
            w.destroy()
        for label, cmd in (actions or []):
            ctk.CTkButton(
                self._actions, text=label, height=24, font=FONT_SMALL, width=76,
                fg_color=("gray72", "gray32"),
                hover_color=("gray60", "gray42"),
                command=cmd,
            ).pack(side="left", padx=PAD_XS)


# ── ContentStack ──────────────────────────────────────────────────────────────

class ContentStack(ctk.CTkFrame):
    """
    Stacks all content panels in one grid cell (row=0, col=0).
    Switching is done with tkraise() — panels are built once and preserve state.

    minsize on row/col provides a floor so matplotlib figures never collapse:
        _MIN_H=380 × _MIN_W=580 guarantees readable charts on 13" laptops.
    """

    _MIN_H: int = 380
    _MIN_W: int = 580

    def __init__(self, parent, **kwargs):
        super().__init__(parent, corner_radius=0,
                         fg_color=("gray95", "gray13"), **kwargs)
        self.rowconfigure(0, weight=1, minsize=self._MIN_H)
        self.columnconfigure(0, weight=1, minsize=self._MIN_W)
        self._panels: dict[str, ctk.CTkFrame] = {}

    def register(self, key: str, frame: ctk.CTkFrame) -> None:
        """Place a panel frame in the stack. All panels share (row=0, col=0)."""
        frame.grid(row=0, column=0, sticky="nsew")
        self._panels[key] = frame

    def show(self, key: str) -> None:
        """Raise the panel with this key to the top of the z-stack."""
        if key in self._panels:
            self._panels[key].tkraise()


# ── FrequencyPanel ────────────────────────────────────────────────────────────

class FrequencyPanel:
    """
    Displays a frequency DataFrame (grouped or ungrouped) in a DataTreeview.
    Registered in ContentStack under the key 'freq'.
    Updated in-place via load() without recreating widgets.
    """

    def __init__(self, parent):
        self._root = ctk.CTkFrame(parent, fg_color="transparent")
        self._root.rowconfigure(1, weight=1)
        self._root.columnconfigure(0, weight=1)

        self._header = ctk.CTkLabel(
            self._root, text="─", font=FONT_SECTION, anchor="w",
        )
        self._header.grid(row=0, column=0, sticky="w", padx=PAD_L, pady=(PAD_M, PAD_XS))

        inner = ctk.CTkFrame(self._root, fg_color="transparent")
        inner.grid(row=1, column=0, sticky="nsew")
        self._tree = DataTreeview(inner)

    def load(self, title: str, df) -> None:
        self._header.configure(text=title)
        self._tree.load(df)


# ── Sidebar ───────────────────────────────────────────────────────────────────

class Sidebar(ctk.CTkScrollableFrame):
    """
    Left navigation panel: data-entry controls + analysis navigation.
    Active panel is highlighted via set_active(key).
    """

    # Default colors for each nav button (inactive state)
    _BTN_COLORS: dict[str, str | tuple] = {
        "stats":     ("#2a6494", "#1a4a70"),
        "graphs":    ("#2e6b3e", "#1b4a28"),
        "prob":      ("#7a6b2e", "#4a3e18"),
        "reg":       ("#6b2e2e", "#4a1b1b"),
        "sampling":  ("#2e5b7a", "#1a3a52"),
        "inference": ("#5a3e7a", "#3a2552"),
    }
    _ACTIVE_COLOR = ("#1f6aa5", "#4d9de0")

    def __init__(self, parent, callbacks: dict, controller, **kwargs):
        super().__init__(parent, width=240, label_text="", corner_radius=0,
                         fg_color=("gray92", "gray14"), **kwargs)
        self._cb = callbacks
        self._ctrl = controller
        self._nav_buttons: dict[str, ctk.CTkButton] = {}
        self._build()

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _section(self, text: str) -> None:
        ctk.CTkLabel(self, text=text, font=FONT_SMALL, anchor="w",
                     text_color=("gray30", "gray70")).pack(
            fill="x", padx=PAD_M, pady=(PAD_L, PAD_XS))
        ctk.CTkFrame(self, height=1, fg_color=("gray70", "gray40")).pack(
            fill="x", padx=PAD_M, pady=(0, PAD_S))

    def _nav_btn(self, text: str, command,
                 key: str = "", color: str | tuple = "transparent") -> ctk.CTkButton:
        btn = ctk.CTkButton(
            self, text=text, font=FONT_SMALL, height=34,
            anchor="w", fg_color=color,
            hover_color=("gray80", "gray28"),
            command=command,
        )
        btn.pack(fill="x", padx=PAD_M, pady=PAD_XS)
        if key:
            self._nav_buttons[key] = btn
        return btn

    def set_active(self, key: str) -> None:
        """Highlight the active navigation button and restore others to default."""
        for k, btn in self._nav_buttons.items():
            btn.configure(
                fg_color=self._ACTIVE_COLOR if k == key
                else self._BTN_COLORS.get(k, "transparent")
            )

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build(self) -> None:
        ctk.CTkLabel(self, text="Estadística\nDescriptiva",
                     font=FONT_TITLE, justify="left").pack(
            padx=PAD_M, pady=(PAD_L, PAD_S), anchor="w")

        # Variables
        self._section("VARIABLES")
        ctk.CTkLabel(self, text="Nombre:", font=FONT_SMALL, anchor="w").pack(
            fill="x", padx=PAD_M, pady=(PAD_XS, 0))
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Nombre de variable",
                                       font=FONT_SMALL, height=30)
        self.name_entry.pack(fill="x", padx=PAD_M, pady=PAD_XS)

        ctk.CTkLabel(self, text="Tipo:", font=FONT_SMALL, anchor="w").pack(
            fill="x", padx=PAD_M, pady=(PAD_XS, 0))
        self.type_combo = ctk.CTkComboBox(
            self, values=["Numero", "Cadena"],
            state="readonly", font=FONT_SMALL, height=30,
        )
        self.type_combo.set("Numero")
        self.type_combo.pack(fill="x", padx=PAD_M, pady=PAD_XS)

        r1 = ctk.CTkFrame(self, fg_color="transparent")
        r1.pack(fill="x", padx=PAD_M, pady=PAD_XS)
        r1.columnconfigure((0, 1), weight=1)
        ctk.CTkButton(r1, text="Agregar", font=FONT_SMALL, height=28,
                      command=self._cb["add_column"]).grid(
            row=0, column=0, sticky="ew", padx=(0, PAD_XS))
        ctk.CTkButton(r1, text="Editar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"),
                      hover_color=("gray60", "gray45"),
                      command=self._cb["edit_column"]).grid(
            row=0, column=1, sticky="ew", padx=(PAD_XS, 0))
        ctk.CTkButton(self, text="Importar archivo", font=FONT_SMALL, height=28,
                      fg_color=("#3a7ebf", "#1f6aa5"),
                      command=self._cb["import_file"]).pack(
            fill="x", padx=PAD_M, pady=(PAD_XS, 0))

        # Datos
        self._section("DATOS")
        ctk.CTkLabel(self, text="Dato:", font=FONT_SMALL, anchor="w").pack(
            fill="x", padx=PAD_M, pady=(PAD_XS, 0))
        self.data_entry = ctk.CTkEntry(self, placeholder_text="Valor",
                                       font=FONT_SMALL, height=30)
        self.data_entry.pack(fill="x", padx=PAD_M, pady=PAD_XS)

        ctk.CTkLabel(self, text="Variable:", font=FONT_SMALL, anchor="w").pack(
            fill="x", padx=PAD_M, pady=(PAD_XS, 0))
        self.data_col_combo = ctk.CTkComboBox(
            self, values=list(self._ctrl.columns),
            state="readonly", font=FONT_SMALL, height=30,
        )
        self.data_col_combo.pack(fill="x", padx=PAD_M, pady=PAD_XS)

        ctk.CTkLabel(self, text="Índice de fila:", font=FONT_SMALL, anchor="w").pack(
            fill="x", padx=PAD_M, pady=(PAD_XS, 0))
        self.index_combo = ctk.CTkComboBox(
            self, values=["1"], state="readonly", font=FONT_SMALL, height=30,
        )
        self.index_combo.set("1")
        self.index_combo.pack(fill="x", padx=PAD_M, pady=PAD_XS)

        r2 = ctk.CTkFrame(self, fg_color="transparent")
        r2.pack(fill="x", padx=PAD_M, pady=PAD_XS)
        r2.columnconfigure((0, 1), weight=1)
        ctk.CTkButton(r2, text="Nueva fila", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"),
                      hover_color=("gray60", "gray45"),
                      command=self._cb["add_row"]).grid(
            row=0, column=0, sticky="ew", padx=(0, PAD_XS))
        ctk.CTkButton(r2, text="Guardar", font=FONT_SMALL, height=28,
                      command=self._cb["edit_cell"]).grid(
            row=0, column=1, sticky="ew", padx=(PAD_XS, 0))

        # Análisis
        self._section("ANÁLISIS")
        ctk.CTkLabel(self, text="Variable activa:", font=FONT_SMALL, anchor="w").pack(
            fill="x", padx=PAD_M, pady=(PAD_XS, 0))
        self.col_selector = ctk.CTkComboBox(
            self, values=list(self._ctrl.columns),
            state="readonly", font=FONT_SMALL, height=30,
        )
        self.col_selector.pack(fill="x", padx=PAD_M, pady=(PAD_XS, PAD_S))

        self._nav_btn("  Tabla Agrupada",    self._cb["grouped_table"],   key="freq")
        self._nav_btn("  Tabla No Agrupada", self._cb["ungrouped_table"])

        self._section("ESTADÍSTICA")
        self._nav_btn("  Medidas Centrales",  self._cb["central_measures"])
        self._nav_btn("  Dispersión y Forma", self._cb["statistics_panel"],
                      key="stats", color=self._BTN_COLORS["stats"])

        self._section("GRÁFICOS")
        self._nav_btn("  Gráficos Estadísticos", self._cb["graphs_panel"],
                      key="graphs", color=self._BTN_COLORS["graphs"])

        self._section("PROBABILIDADES")
        self._nav_btn("  Cálculo de Probabilidades", self._cb["probability_panel"],
                      key="prob", color=self._BTN_COLORS["prob"])

        self._section("REGRESIÓN")
        self._nav_btn("  Análisis de Regresión", self._cb["regression_panel"],
                      key="reg", color=self._BTN_COLORS["reg"])

        self._section("MUESTREO E INFERENCIA")
        self._nav_btn("  Muestreo Probabilístico", self._cb["sampling_panel"],
                      key="sampling", color=self._BTN_COLORS["sampling"])
        self._nav_btn("  Inferencia Estadística", self._cb["inference_panel"],
                      key="inference", color=self._BTN_COLORS["inference"])


# ── DataTable ─────────────────────────────────────────────────────────────────

class DataTable(ctk.CTkFrame):
    """Dark-styled ttk.Treeview wrapped in a CTkFrame for the main data grid."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        apply_treeview_dark_style()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        sb_y = ttk.Scrollbar(self, orient="vertical",
                              style="Dark.Vertical.TScrollbar")
        sb_y.grid(row=0, column=1, sticky="ns")
        sb_x = ttk.Scrollbar(self, orient="horizontal",
                              style="Dark.Horizontal.TScrollbar")
        sb_x.grid(row=1, column=0, sticky="ew")

        self._tree = ttk.Treeview(
            self, style="Dark.Treeview",
            yscrollcommand=sb_y.set,
            xscrollcommand=sb_x.set,
        )
        self._tree.grid(row=0, column=0, sticky="nsew")
        sb_y.config(command=self._tree.yview)
        sb_x.config(command=self._tree.xview)

    @property
    def tree(self) -> ttk.Treeview:
        return self._tree

    def refresh(self, columns: tuple, rows: list) -> None:
        self._tree.delete(*self._tree.get_children())
        self._tree["columns"] = columns
        self._tree.column("#0", width=50, stretch=False)
        self._tree.heading("#0", text="#")
        for col in columns:
            self._tree.heading(col, text=col)
            self._tree.column(col, anchor="center", width=90, minwidth=60)
        for idx, row in enumerate(rows, start=1):
            self._tree.insert("", "end", text=str(idx), values=row)


# ── MainWindow ────────────────────────────────────────────────────────────────

class MainWindow:
    """
    Root application window.

    All content panels are built ONCE in _build() and registered in ContentStack.
    Navigation uses tkraise() — no widget destruction, state is preserved.
    """

    def __init__(self, title: str, controller):
        self._ctrl = controller
        self._active_panel: str = ""

        self._window = ctk.CTk()
        self._window.title(title)
        # Minimum: ensures matplotlib never renders below ~580×380
        self._window.minsize(1060, 700)

        self._build()
        self._layout()
        self._refresh()

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build(self) -> None:
        callbacks = {
            "add_column":        self._add_column,
            "edit_column":       self._edit_column_dialog,
            "import_file":       self._import_file,
            "add_row":           self._add_row,
            "edit_cell":         self._edit_cell,
            "grouped_table":     self._show_grouped_table,
            "ungrouped_table":   self._show_ungrouped_table,
            "central_measures":  self._show_central_measures,
            "statistics_panel":  self._show_statistics_panel,
            "graphs_panel":      self._show_graphs_panel,
            "probability_panel": self._show_probability_panel,
            "regression_panel":  self._show_regression_panel,
            "sampling_panel":    self._show_sampling_panel,
            "inference_panel":   self._show_inference_panel,
        }

        # ── Right pane (intermediate container for the 3-row right layout) ──
        self._right_pane = ctk.CTkFrame(self._window, corner_radius=0,
                                        fg_color="transparent")

        self._sidebar     = Sidebar(self._window, callbacks, self._ctrl)
        self._data_table  = DataTable(self._right_pane, corner_radius=0)
        self._ctoolbar    = ContentToolbar(self._right_pane)
        self._stack       = ContentStack(self._right_pane)

        # ── Pre-build all panels (built once, preserved across navigation) ──
        self._freq_panel      = FrequencyPanel(self._stack)
        self._stats_panel     = StatisticsPanel(self._stack, self._ctrl)
        self._graph_panel     = GraphsPanel(self._stack, self._ctrl)
        self._prob_panel      = ProbabilityPanel(self._stack, self._ctrl)
        self._reg_panel       = RegressionPanel(self._stack, self._ctrl)
        self._sampling_panel  = SamplingPanel(self._stack, self._ctrl)
        self._inference_panel = InferencePanel(self._stack, self._ctrl)

        self._stack.register("freq",      self._freq_panel._root)
        self._stack.register("stats",     self._stats_panel._root)
        self._stack.register("graphs",    self._graph_panel._root)
        self._stack.register("prob",      self._prob_panel._root)
        self._stack.register("reg",       self._reg_panel._root)
        self._stack.register("sampling",  self._sampling_panel._root)
        self._stack.register("inference", self._inference_panel._root)

        # Default view on startup
        self._show_panel("stats")

    # ── Layout ────────────────────────────────────────────────────────────────

    def _layout(self) -> None:
        """
        Window grid
        ───────────
        col 0: Sidebar  (fixed width 240, weight=0)
        col 1: RightPane (weight=1)

        RightPane grid
        ──────────────
        row 0: DataTable     (weight=2, minsize=180) — always visible
        row 1: ContentToolbar (fixed 32 px, weight=0)
        row 2: ContentStack  (weight=3, minsize=380) — panel switcher
        """
        self._window.columnconfigure(0, weight=0, minsize=240)
        self._window.columnconfigure(1, weight=1)
        self._window.rowconfigure(0, weight=1)

        self._sidebar.grid(row=0, column=0, sticky="nsew")
        self._right_pane.grid(row=0, column=1, sticky="nsew")

        self._right_pane.columnconfigure(0, weight=1)
        self._right_pane.rowconfigure(0, weight=2, minsize=180)
        self._right_pane.rowconfigure(1, weight=0)
        self._right_pane.rowconfigure(2, weight=3, minsize=380)

        self._data_table.grid(row=0, column=0, sticky="nsew", padx=(1, 0))
        self._ctoolbar.grid(row=1, column=0, sticky="ew",   padx=(1, 0))
        self._stack.grid(   row=2, column=0, sticky="nsew", padx=(1, 0), pady=(1, 0))

    # ── Navigation helpers ────────────────────────────────────────────────────

    def _show_panel(self, key: str,
                    actions: list[tuple[str, callable]] | None = None) -> None:
        """Raise a panel, update breadcrumb, and highlight the sidebar button."""
        self._stack.show(key)
        self._ctoolbar.set_panel(key, actions)
        self._sidebar.set_active(key)
        self._active_panel = key

    # ── Sidebar actions ───────────────────────────────────────────────────────

    def _add_column(self) -> None:
        name = self._sidebar.name_entry.get().strip()
        if not name:
            return
        try:
            self._ctrl.add_column(name)
            self._refresh()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _add_row(self) -> None:
        self._ctrl.add_empty_row()
        self._refresh()

    def _edit_cell(self) -> None:
        idx_str = self._sidebar.index_combo.get().strip()
        column  = self._sidebar.data_col_combo.get().strip()
        value   = self._sidebar.data_entry.get().strip()
        if not value:
            return
        try:
            self._ctrl.edit_cell(int(idx_str) - 1, column, value)
            self._refresh()
        except (ValueError, IndexError) as e:
            messagebox.showerror("Error", str(e))

    def _import_file(self) -> None:
        try:
            if self._ctrl.import_file():
                self._refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _edit_column_dialog(self) -> None:
        win = ctk.CTkToplevel(self._window)
        win.title("Editar nombre de variable")
        win.geometry("340x180")
        win.resizable(False, False)
        win.grab_set()

        content = ctk.CTkFrame(win, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=PAD_L, pady=PAD_L)
        content.columnconfigure(1, weight=1)

        ctk.CTkLabel(content, text="Variable:", font=FONT_SMALL, anchor="w").grid(
            row=0, column=0, sticky="w", pady=PAD_S, padx=(0, PAD_M))
        col_combo = ctk.CTkComboBox(content, values=list(self._ctrl.columns),
                                    state="readonly", font=FONT_SMALL)
        if self._ctrl.columns:
            col_combo.set(self._ctrl.columns[0])
        col_combo.grid(row=0, column=1, sticky="ew", pady=PAD_S)

        ctk.CTkLabel(content, text="Nuevo nombre:", font=FONT_SMALL, anchor="w").grid(
            row=1, column=0, sticky="w", pady=PAD_S, padx=(0, PAD_M))
        name_entry = ctk.CTkEntry(content, font=FONT_SMALL)
        name_entry.grid(row=1, column=1, sticky="ew", pady=PAD_S)

        def apply():
            old = col_combo.get().strip()
            new = name_entry.get().strip()
            if not old or not new:
                return
            try:
                self._ctrl.rename_column(old, new)
                self._refresh()
                win.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(content, text="Cambiar nombre", font=FONT_SMALL,
                      command=apply).grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(PAD_M, 0))

    # ── Frequency tables ──────────────────────────────────────────────────────

    def _show_grouped_table(self) -> None:
        col = self._sidebar.col_selector.get()
        if not col:
            return
        try:
            df = self._ctrl.get_grouped_table(col)
            self._freq_panel.load(f"Tabla Agrupada — {col}", df)
            self._show_panel("freq")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _show_ungrouped_table(self) -> None:
        col = self._sidebar.col_selector.get()
        if not col:
            return
        try:
            df = self._ctrl.get_ungrouped_table(col)
            self._freq_panel.load(f"Tabla No Agrupada — {col}", df)
            self._show_panel("freq")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ── Central measures ──────────────────────────────────────────────────────

    def _show_central_measures(self) -> None:
        col = self._sidebar.col_selector.get()
        if not col:
            return
        try:
            m = self._ctrl.get_central_measures(col)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        win = ctk.CTkToplevel(self._window)
        win.title("Medidas de Tendencia Central")
        win.geometry("600x620")

        textbox = ctk.CTkTextbox(win, font=("Arial", 11), wrap="word")
        textbox.pack(fill="both", expand=True, padx=PAD_L, pady=PAD_L)

        lines = [
            "── MEDIDAS DE TENDENCIA CENTRAL ──\n",
            f"Variable: {col}\n",
            f"Media Aritmética (agrupada):  {m['mean']:.4f}",
            f"Mediana (agrupada):           {m['median']:.4f}",
            f"Moda Cruda:                   {m['mode_raw']}",
            f"Moda Interpolada (Czuber):    {m['mode_interpolated']:.4f}",
            f"Media Geométrica:             {m['geometric_mean']:.4f}",
            f"Media Armónica:               {m['harmonic_mean']:.4f}",
            "\n── Cuartiles ──",
            f"Q1: {m['q1']:.4f}",
            f"Q2 (Mediana): {m['q2']:.4f}",
            f"Q3: {m['q3']:.4f}",
            "\n── Deciles ──",
        ]
        for k, v in m["deciles"].items():
            lines.append(f"{k}: {v:.4f}")
        lines += ["\n── Percentiles (seleccionados) ──"]
        for k in [1, 5, 10, 25, 50, 75, 90, 95, 99]:
            lines.append(f"P{k:>2}: {m['percentiles'][f'P{k}']:.4f}")

        textbox.insert("end", "\n".join(lines))
        textbox.configure(state="disabled")

    # ── Module panels ─────────────────────────────────────────────────────────

    def _show_statistics_panel(self) -> None:
        self._show_panel("stats")

    def _show_graphs_panel(self) -> None:
        self._show_panel("graphs")

    def _show_probability_panel(self) -> None:
        self._show_panel("prob")

    def _show_regression_panel(self) -> None:
        self._show_panel("reg")

    def _show_sampling_panel(self) -> None:
        self._show_panel("sampling")

    def _show_inference_panel(self) -> None:
        self._show_panel("inference")

    # ── Refresh ───────────────────────────────────────────────────────────────

    def _refresh(self) -> None:
        """Syncs all sidebar combos and data table after any data change."""
        cols    = self._ctrl.columns
        rows    = self._ctrl.get_all_rows()
        indexes = tuple(str(i + 1) for i in range(len(rows)))

        self._data_table.refresh(cols, rows)

        self._sidebar.data_col_combo.configure(values=list(cols))
        if cols:
            self._sidebar.data_col_combo.set(cols[0])
        self._sidebar.index_combo.configure(values=list(indexes))
        if indexes:
            self._sidebar.index_combo.set(indexes[0])
        self._sidebar.col_selector.configure(values=list(cols))
        if cols:
            self._sidebar.col_selector.set(cols[0])

    def run(self) -> None:
        self._window.mainloop()
