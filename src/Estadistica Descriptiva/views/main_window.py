"""
Main application window — restructured with CTkTabview navigation.

Layout
------
┌────────────────┬────────────────────────────────────────────────────┐
│  ☰ Menú  (40px)│  [Estadística][Gráficos][Probabilidad]...          │
│  ──────────────│  ──────────────────────────────────────────────── │
│  Sidebar       │  Active panel  (lazy-loaded, weight=1)             │
│  (collapsible  ├────────────────────────────────────────────────────┤
│   240 ↔ 48 px) │  ▲ Tabla de datos  [+ Fila] [✕ Fila]   (toolbar) │
│                │  DataTable Treeview (collapsible ~180 px)          │
└────────────────┴────────────────────────────────────────────────────┘

Navigation
──────────
• CTkTabview (top of right pane) replaces the old ContentStack + sidebar
  nav buttons.
• Panels are created LAZILY on the first activation of each tab and then
  cached in self._panels — state is preserved across tab switches.
• FrequencyPanel lives in the "Frecuencias" tab and is triggered by
  sidebar buttons "Tabla Agrupada" / "Tabla No Agrupada".
• "Medidas Centrales" still opens as a CTkToplevel popup (no change).

Sidebar
───────
• Toggle button collapses/expands the sidebar (240 ↔ 48 px).
• Contains only data-entry controls (variables, data cells, analysis
  variable selector, frequency shortcuts). Navigation is on the tabview.

DataTable
─────────
• Fixed at the bottom of the right pane.
• Toggle button shows/hides the treeview body (~180 px).
• Quick-action buttons in its toolbar row.

Import
──────
• "Importar archivo" opens DatasetImportDialog (views/dialogs) which gives
  the user a full preview before committing. Replaces the old inline dialog
  in app_controller.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import importlib
import customtkinter as ctk

from views.theme import (
    FONT_TITLE, FONT_SECTION, FONT_NORMAL, FONT_SMALL, FONT_MONO,
    PAD_XS, PAD_S, PAD_M, PAD_L,
    SUBTOOLBAR_H, TOOLBAR_BG,
    CLR_BTN_PRIMARY, CLR_BTN_SECONDARY,
    CLR_HOVER_PRIMARY, CLR_HOVER_SECONDARY,
    SIDEBAR_BG, SIDEBAR_TOGGLE_BG, CLR_DIVIDER, CLR_PLACEHOLDER,
    apply_treeview_dark_style,
)
from views.dialogs.base_dialog import BaseDialog
from views.dialogs.dataset_import_dialog import DatasetImportDialog

# ── Layout constants ──────────────────────────────────────────────────────────
_SB_EXPANDED  = 240   # sidebar width when open
_SB_COLLAPSED = 48    # sidebar width when closed (toggle button only)
_DT_HEIGHT    = 180   # DataTable body height when visible


# ── DataTable ─────────────────────────────────────────────────────────────────

class DataTable(ctk.CTkFrame):
    """Dark-styled ttk.Treeview for the main data grid."""

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
        char_px = 8
        for i, col in enumerate(columns):
            col_vals = [str(row[i]) for row in rows] if rows else []
            max_chars = max(len(str(col)), max((len(v) for v in col_vals), default=0))
            col_w = max(60, min(int(max_chars * char_px) + 16, 240))
            self._tree.heading(col, text=col)
            self._tree.column(col, anchor="center", width=col_w, minwidth=60)
        for idx, row in enumerate(rows, start=1):
            self._tree.insert("", "end", text=str(idx), values=row)


# ── FrequencyPanel ────────────────────────────────────────────────────────────

class FrequencyPanel:
    """
    Shows a frequency DataFrame in a DataTreeview.
    Lives inside the 'Frecuencias' tab; loaded lazily like the other panels.
    """

    def __init__(self, parent):
        from views.components import DataTreeview

        self._root = ctk.CTkFrame(parent, fg_color="transparent")
        self._root.grid(row=0, column=0, sticky="nsew")
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self._root.rowconfigure(1, weight=1)
        self._root.columnconfigure(0, weight=1)

        self._header = ctk.CTkLabel(
            self._root,
            text="Selecciona una variable y tipo de tabla en el panel izquierdo →",
            font=FONT_SECTION, anchor="w",
            text_color=CLR_PLACEHOLDER,
        )
        self._header.grid(row=0, column=0, sticky="w",
                          padx=PAD_L, pady=(PAD_M, PAD_XS))

        inner = ctk.CTkFrame(self._root, fg_color="transparent")
        inner.grid(row=1, column=0, sticky="nsew")
        inner.rowconfigure(0, weight=1)
        inner.columnconfigure(0, weight=1)
        self._tree = DataTreeview(inner)

    def load(self, title: str, df) -> None:
        self._header.configure(text=title)
        self._tree.load(df)


# ── Sidebar ───────────────────────────────────────────────────────────────────

class Sidebar(ctk.CTkScrollableFrame):
    """
    Left data-entry panel.
    Navigation is handled by CTkTabview — this sidebar contains only:
      • Variable management (add, rename, import)
      • Data cell editing
      • Analysis variable selector + frequency/central-measures shortcuts
    """

    def __init__(self, parent, callbacks: dict, controller, **kwargs):
        super().__init__(
            parent,
            width=_SB_EXPANDED - 10,
            label_text="",
            corner_radius=0,
            fg_color=("gray92", "gray14"),
            **kwargs,
        )
        self._cb   = callbacks
        self._ctrl = controller
        self._build()

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _section(self, text: str) -> None:
        ctk.CTkLabel(
            self, text=text, font=FONT_SMALL, anchor="w",
            text_color=("gray30", "gray70"),
        ).pack(fill="x", padx=PAD_M, pady=(PAD_L, PAD_XS))
        ctk.CTkFrame(self, height=1,
                     fg_color=CLR_DIVIDER).pack(
            fill="x", padx=PAD_M, pady=(0, PAD_S))

    def _action_btn(self, text: str, cmd, **kw) -> ctk.CTkButton:
        btn = ctk.CTkButton(
            self, text=text, font=FONT_SMALL,
            height=32, anchor="w",
            fg_color=CLR_BTN_SECONDARY,
            hover_color=CLR_HOVER_SECONDARY,
            command=cmd, **kw,
        )
        btn.pack(fill="x", padx=PAD_M, pady=PAD_XS)
        return btn

    # ── Build ─────────────────────────────────────────────────────────────────

    def _build(self) -> None:
        ctk.CTkLabel(
            self, text="Estadística\nDescriptiva",
            font=FONT_TITLE, justify="left",
        ).pack(padx=PAD_M, pady=(PAD_L, PAD_S), anchor="w")

        # ── Variables ─────────────────────────────────────────────────────────
        self._section("VARIABLES")
        ctk.CTkLabel(self, text="Nombre:", font=FONT_SMALL, anchor="w").pack(
            fill="x", padx=PAD_M, pady=(PAD_XS, 0))
        self.name_entry = ctk.CTkEntry(
            self, placeholder_text="Nombre de variable",
            font=FONT_SMALL, height=30,
        )
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
                      fg_color=CLR_BTN_SECONDARY,
                      hover_color=CLR_HOVER_SECONDARY,
                      command=self._cb["edit_column"]).grid(
            row=0, column=1, sticky="ew", padx=(PAD_XS, 0))

        ctk.CTkButton(
            self, text="⬆  Importar CSV / Excel",
            font=FONT_SMALL, height=30,
            fg_color=CLR_BTN_PRIMARY,
            hover_color=CLR_HOVER_PRIMARY,
            command=self._cb["import_file"],
        ).pack(fill="x", padx=PAD_M, pady=(PAD_XS, 0))

        # ── Datos ─────────────────────────────────────────────────────────────
        self._section("DATOS")
        ctk.CTkLabel(self, text="Dato:", font=FONT_SMALL, anchor="w").pack(
            fill="x", padx=PAD_M, pady=(PAD_XS, 0))
        self.data_entry = ctk.CTkEntry(
            self, placeholder_text="Valor",
            font=FONT_SMALL, height=30,
        )
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
            self, values=["1"], state="readonly",
            font=FONT_SMALL, height=30,
        )
        self.index_combo.set("1")
        self.index_combo.pack(fill="x", padx=PAD_M, pady=PAD_XS)

        r2 = ctk.CTkFrame(self, fg_color="transparent")
        r2.pack(fill="x", padx=PAD_M, pady=PAD_XS)
        r2.columnconfigure((0, 1), weight=1)
        ctk.CTkButton(r2, text="Nueva fila", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY,
                      hover_color=CLR_HOVER_SECONDARY,
                      command=self._cb["add_row"]).grid(
            row=0, column=0, sticky="ew", padx=(0, PAD_XS))
        ctk.CTkButton(r2, text="Guardar", font=FONT_SMALL, height=28,
                      command=self._cb["edit_cell"]).grid(
            row=0, column=1, sticky="ew", padx=(PAD_XS, 0))

        # ── Análisis ──────────────────────────────────────────────────────────
        self._section("ANÁLISIS")
        ctk.CTkLabel(self, text="Variable activa:", font=FONT_SMALL, anchor="w").pack(
            fill="x", padx=PAD_M, pady=(PAD_XS, 0))
        self.col_selector = ctk.CTkComboBox(
            self, values=list(self._ctrl.columns),
            state="readonly", font=FONT_SMALL, height=30,
        )
        self.col_selector.pack(fill="x", padx=PAD_M, pady=(PAD_XS, PAD_S))

        self._action_btn("Tabla Agrupada",    self._cb["grouped_table"])
        self._action_btn("Tabla No Agrupada", self._cb["ungrouped_table"])
        self._action_btn("Medidas Centrales", self._cb["central_measures"])


# ── _EditColumnDialog ─────────────────────────────────────────────────────────

class _EditColumnDialog(BaseDialog):
    """Modal dialog for renaming a dataset column. Returns (old_name, new_name) or None."""

    def __init__(self, parent, columns):
        self._columns = columns
        super().__init__(parent, "Editar nombre de variable", width=340, height=180)

    def _build_ui(self) -> None:
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=PAD_L, pady=PAD_L)
        content.columnconfigure(1, weight=1)

        ctk.CTkLabel(content, text="Variable:", font=FONT_SMALL, anchor="w").grid(
            row=0, column=0, sticky="w", pady=PAD_S, padx=(0, PAD_M))
        self._col_combo = ctk.CTkComboBox(
            content, values=list(self._columns), state="readonly", font=FONT_SMALL,
        )
        if self._columns:
            self._col_combo.set(self._columns[0])
        self._col_combo.grid(row=0, column=1, sticky="ew", pady=PAD_S)

        ctk.CTkLabel(content, text="Nuevo nombre:", font=FONT_SMALL, anchor="w").grid(
            row=1, column=0, sticky="w", pady=PAD_S, padx=(0, PAD_M))
        self._name_entry = ctk.CTkEntry(content, font=FONT_SMALL)
        self._name_entry.grid(row=1, column=1, sticky="ew", pady=PAD_S)

        ctk.CTkButton(
            content, text="Cambiar nombre", font=FONT_SMALL, command=self._apply,
        ).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(PAD_M, 0))

    def _apply(self) -> None:
        old = self._col_combo.get().strip()
        new = self._name_entry.get().strip()
        if old and new:
            self._result = (old, new)
            super()._on_confirm()


# ── MainWindow ────────────────────────────────────────────────────────────────

class MainWindow:
    """
    Root application window.

    All content panels are loaded LAZILY on first tab visit and cached in
    self._panels.  Navigation is through CTkTabview — no tkraise() calls.
    """

    # (tab label, module path for importlib, class name)
    # module_path=None → FrequencyPanel (special case, no controller arg)
    _TABS: list[tuple] = [
        ("Frecuencias",  None,                      None),
        ("Estadística",  "views.statistics_panel",  "StatisticsPanel"),
        ("Gráficos",     "views.graphs_panel",      "GraphsPanel"),
        ("Probabilidad", "views.probability_panel", "ProbabilityPanel"),
        ("Regresión",    "views.regression_panel",  "RegressionPanel"),
        ("Muestreo",     "views.sampling_panel",    "SamplingPanel"),
        ("Inferencia",   "views.inference_panel",   "InferencePanel"),
    ]

    def __init__(self, title: str, controller):
        self._ctrl              = controller
        self._sidebar_expanded  = True
        self._dt_visible        = True
        self._panels: dict      = {}   # tab_name -> panel instance
        self._freq_panel: FrequencyPanel | None = None

        self._window = ctk.CTk()
        self._window.title(title)
        self._window.minsize(960, 680)

        self._build()
        self._layout()
        self._refresh()

    # ── Build ──────────────────────────────────────────────────────────────────

    def _build(self) -> None:
        callbacks = {
            "add_column":       self._add_column,
            "edit_column":      self._edit_column_dialog,
            "import_file":      self._import_file,
            "add_row":          self._add_row,
            "edit_cell":        self._edit_cell,
            "grouped_table":    self._show_grouped_table,
            "ungrouped_table":  self._show_ungrouped_table,
            "central_measures": self._show_central_measures,
        }

        self._build_sidebar_wrapper(callbacks)
        self._build_right_pane()

    # ── Sidebar wrapper ────────────────────────────────────────────────────────

    def _build_sidebar_wrapper(self, callbacks: dict) -> None:
        """
        col 0 of the root window.
        ┌─────────────────────────────┐
        │ row 0: toggle button (40px) │  ← always visible
        │ row 1: Sidebar scrollable   │  ← hidden on collapse
        └─────────────────────────────┘
        """
        self._sb_wrapper = ctk.CTkFrame(
            self._window, corner_radius=0,
            fg_color=SIDEBAR_BG,
        )
        self._sb_wrapper.rowconfigure(1, weight=1)
        self._sb_wrapper.columnconfigure(0, weight=1)

        # Toggle strip
        toggle_strip = ctk.CTkFrame(
            self._sb_wrapper, height=40, width=_SB_COLLAPSED, corner_radius=0,
            fg_color=SIDEBAR_TOGGLE_BG,
        )
        toggle_strip.grid(row=0, column=0, sticky="ew")
        toggle_strip.columnconfigure(0, weight=1)
        toggle_strip.grid_propagate(False)

        self._toggle_btn = ctk.CTkButton(
            toggle_strip, text="☰  Menú",
            font=FONT_SMALL, height=36,
            fg_color="transparent",
            hover_color=("gray72", "gray30"),
            anchor="w",
            command=self._toggle_sidebar,
        )
        self._toggle_btn.grid(row=0, column=0, sticky="ew", padx=PAD_S)

        # Scrollable content
        self._sidebar = Sidebar(self._sb_wrapper, callbacks, self._ctrl)
        self._sidebar.grid(row=1, column=0, sticky="nsew")

    # ── Right pane ─────────────────────────────────────────────────────────────

    def _build_right_pane(self) -> None:
        """
        col 1 of the root window.
        ┌────────────────────────────────────┐
        │ row 0: CTkTabview (weight=1)        │
        ├────────────────────────────────────┤
        │ row 1: DataTable container (fixed)  │
        └────────────────────────────────────┘
        """
        self._right_pane = ctk.CTkFrame(
            self._window, corner_radius=0, fg_color="transparent",
        )
        self._right_pane.columnconfigure(0, weight=1)
        self._right_pane.rowconfigure(0, weight=1)
        self._right_pane.rowconfigure(1, weight=0)

        self._build_tabview()
        self._build_datatable()

    def _build_tabview(self) -> None:
        self._tabview = ctk.CTkTabview(
            self._right_pane,
            corner_radius=6,
            anchor="nw",
        )
        self._tabview.grid(row=0, column=0, sticky="nsew", padx=(1, 0))

        for tab_name, _, _ in self._TABS:
            self._tabview.add(tab_name)
            tab = self._tabview.tab(tab_name)
            tab.rowconfigure(0, weight=1)
            tab.columnconfigure(0, weight=1)
            # Placeholder label shown before the panel is loaded
            ph = ctk.CTkLabel(
                tab,
                text=f"Cargando {tab_name}…",
                font=FONT_NORMAL,
                text_color=("gray50", "gray60"),
            )
            ph.grid(row=0, column=0)
            tab._ph = ph  # noqa: SLF001

        # Wire tab-change callback and pre-load the default tab
        self._tabview.configure(command=self._on_tab_change)
        self._tabview.set("Estadística")
        self._load_tab("Estadística")

    def _build_datatable(self) -> None:
        """Collapsible DataTable fixed at the bottom of the right pane."""
        self._dt_container = ctk.CTkFrame(
            self._right_pane, fg_color="transparent",
        )
        self._dt_container.grid(row=1, column=0, sticky="ew", padx=(1, 0))
        self._dt_container.columnconfigure(0, weight=1)
        self._dt_container.rowconfigure(1, weight=0)

        # Toolbar row
        dt_toolbar = ctk.CTkFrame(
            self._dt_container, height=SUBTOOLBAR_H, corner_radius=0,
            fg_color=TOOLBAR_BG,
        )
        dt_toolbar.grid(row=0, column=0, sticky="ew")
        dt_toolbar.columnconfigure(1, weight=1)
        dt_toolbar.grid_propagate(False)

        self._dt_toggle_btn = ctk.CTkButton(
            dt_toolbar, text="▲  Tabla de datos",
            font=FONT_SMALL, height=28,
            fg_color="transparent",
            hover_color=("gray73", "gray30"),
            anchor="w",
            command=self._toggle_datatable,
        )
        self._dt_toggle_btn.grid(row=0, column=0, sticky="w",
                                  padx=PAD_M, pady=PAD_XS)

        for col_i, (lbl, cmd) in enumerate([
            ("+ Fila",  self._add_row),
            ("✕ Fila",  self._del_row_by_index),
        ], start=2):
            ctk.CTkButton(
                dt_toolbar, text=lbl, width=64, height=24,
                font=FONT_SMALL,
                fg_color=CLR_BTN_SECONDARY,
                hover_color=CLR_HOVER_SECONDARY,
                command=cmd,
            ).grid(row=0, column=col_i, padx=PAD_XS, pady=PAD_XS)

        # Body (hidden on collapse)
        self._dt_body = ctk.CTkFrame(
            self._dt_container, height=_DT_HEIGHT,
            fg_color="transparent", corner_radius=0,
        )
        self._dt_body.grid(row=1, column=0, sticky="ew")
        self._dt_body.grid_propagate(False)
        self._dt_body.rowconfigure(0, weight=1)
        self._dt_body.columnconfigure(0, weight=1)

        self._data_table = DataTable(self._dt_body, corner_radius=0)
        self._data_table.grid(row=0, column=0, sticky="nsew")

    # ── Layout ────────────────────────────────────────────────────────────────

    def _layout(self) -> None:
        self._window.columnconfigure(0, weight=0, minsize=_SB_EXPANDED)
        self._window.columnconfigure(1, weight=1)
        self._window.rowconfigure(0, weight=1)

        self._sb_wrapper.grid(row=0, column=0, sticky="nsew")
        self._right_pane.grid(row=0, column=1, sticky="nsew")

    # ── Lazy panel loading ────────────────────────────────────────────────────

    def _on_tab_change(self) -> None:
        self._load_tab(self._tabview.get())

    def _load_tab(self, name: str) -> None:
        """Create a panel the first time its tab is visited; cache it."""
        if name in self._panels:
            return

        tab_def = next((t for t in self._TABS if t[0] == name), None)
        if tab_def is None:
            return

        _, module_path, class_name = tab_def
        tab = self._tabview.tab(name)

        # Destroy placeholder
        if hasattr(tab, "_ph") and tab._ph.winfo_exists():  # noqa: SLF001
            tab._ph.destroy()  # noqa: SLF001

        if name == "Frecuencias":
            panel = FrequencyPanel(tab)
            self._freq_panel = panel
        else:
            mod = importlib.import_module(module_path)
            PanelClass = getattr(mod, class_name)
            panel = PanelClass(tab, self._ctrl)

        self._panels[name] = panel

    # ── Sidebar toggle ────────────────────────────────────────────────────────

    def _toggle_sidebar(self) -> None:
        self._sidebar_expanded = not self._sidebar_expanded
        if self._sidebar_expanded:
            self._sidebar.grid()
            self._window.columnconfigure(0, weight=0, minsize=_SB_EXPANDED)
            self._toggle_btn.configure(text="☰  Menú")
        else:
            self._sidebar.grid_remove()
            self._window.columnconfigure(0, weight=0, minsize=_SB_COLLAPSED)
            self._toggle_btn.configure(text="☰")

    # ── DataTable toggle ──────────────────────────────────────────────────────

    def _toggle_datatable(self) -> None:
        self._dt_visible = not self._dt_visible
        if self._dt_visible:
            self._dt_body.grid()
            self._dt_toggle_btn.configure(text="▲  Tabla de datos")
        else:
            self._dt_body.grid_remove()
            self._dt_toggle_btn.configure(text="▼  Tabla de datos")

    # ── Variable actions ──────────────────────────────────────────────────────

    def _add_column(self) -> None:
        name = self._sidebar.name_entry.get().strip()
        if not name:
            return
        try:
            self._ctrl.add_column(name)
            self._refresh()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _edit_column_dialog(self) -> None:
        dlg = _EditColumnDialog(self._window, self._ctrl.columns)
        result = dlg.get_result()
        if result:
            old, new = result
            try:
                self._ctrl.rename_column(old, new)
                self._refresh()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    # ── Data actions ──────────────────────────────────────────────────────────

    def _add_row(self) -> None:
        self._ctrl.add_empty_row()
        self._refresh()

    def _del_row_by_index(self) -> None:
        idx_str = self._sidebar.index_combo.get().strip()
        if not idx_str:
            return
        try:
            self._ctrl.delete_row(int(idx_str) - 1)
            self._refresh()
        except (ValueError, IndexError) as e:
            messagebox.showerror("Error", str(e))

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
        """
        Opens DatasetImportDialog for a full browse → preview → confirm flow.
        Falls back to the controller's built-in dialog if the dialog is
        unavailable for any reason.
        """
        try:
            dlg = DatasetImportDialog(self._window)
            result = dlg.get_result()
            if result:
                self._ctrl.load_file_direct(result["filepath"], result["sheet"])
                self._refresh()
        except Exception as e:
            messagebox.showerror("Error al importar", str(e))

    # ── Frequency tables ──────────────────────────────────────────────────────

    def _show_grouped_table(self) -> None:
        col = self._sidebar.col_selector.get()
        if not col:
            return
        try:
            df = self._ctrl.get_grouped_table(col)
            self._ensure_freq_tab()
            self._freq_panel.load(f"Tabla Agrupada — {col}", df)
            self._tabview.set("Frecuencias")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _show_ungrouped_table(self) -> None:
        col = self._sidebar.col_selector.get()
        if not col:
            return
        try:
            df = self._ctrl.get_ungrouped_table(col)
            self._ensure_freq_tab()
            self._freq_panel.load(f"Tabla No Agrupada — {col}", df)
            self._tabview.set("Frecuencias")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _ensure_freq_tab(self) -> None:
        """Guarantees FrequencyPanel exists before use."""
        if "Frecuencias" not in self._panels:
            self._load_tab("Frecuencias")

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

        width, height = 600, 620
        win = ctk.CTkToplevel(self._window)
        win.title("Medidas de Tendencia Central")
        win.resizable(True, True)
        win.update_idletasks()
        px = self._window.winfo_rootx() + max(0, (self._window.winfo_width() - width) // 2)
        py = self._window.winfo_rooty() + max(0, (self._window.winfo_height() - height) // 2)
        win.geometry(f"{width}x{height}+{px}+{py}")
        win.after(200, win.grab_set)

        textbox = ctk.CTkTextbox(win, font=FONT_MONO, wrap="word")
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

    # ── Refresh ───────────────────────────────────────────────────────────────

    def _refresh(self) -> None:
        """Syncs sidebar combos and DataTable after any data change."""
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
