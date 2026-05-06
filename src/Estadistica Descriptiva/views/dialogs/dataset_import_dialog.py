"""
DatasetImportDialog — replaces the inline file-picker logic in app_controller.

Flow
----
1. User clicks "Explorar" → filedialog opens.
2. If .xlsx/.xls: sheet selector appears.
3. First 50 rows are shown in a preview Treeview.
4. User clicks "Importar" → result = {"filepath": ..., "sheet": ...}.

Usage
-----
    from views.dialogs.dataset_import_dialog import DatasetImportDialog

    dlg = DatasetImportDialog(parent_window)
    result = dlg.get_result()       # blocks; returns dict or None on cancel
    if result:
        controller.load_file_direct(result["filepath"], result["sheet"])
        # then call _refresh() on the main window
"""
import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
import pandas as pd

from views.dialogs.base_dialog import BaseDialog
from views.theme import (
    FONT_SECTION, FONT_NORMAL, FONT_SMALL,
    PAD_XS, PAD_S, PAD_M, PAD_L,
    apply_treeview_dark_style, COLOR_TREEVIEW_BG,
)


class DatasetImportDialog(BaseDialog):
    """
    Full-featured import dialog: file browse → sheet select → data preview → confirm.
    Returns {"filepath": str, "sheet": str | int | None} or None if cancelled.
    """

    def __init__(self, parent):
        self._filepath: str | None = None
        super().__init__(parent, "Importar Dataset", width=760, height=540)

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        apply_treeview_dark_style()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)     # preview row expands

        # ── Row 0: File picker ────────────────────────────────────────────────
        file_row = ctk.CTkFrame(self, fg_color="transparent")
        file_row.grid(row=0, column=0, sticky="ew",
                      padx=PAD_L, pady=(PAD_L, PAD_S))
        file_row.columnconfigure(1, weight=1)

        ctk.CTkLabel(file_row, text="Archivo:", font=FONT_NORMAL).grid(
            row=0, column=0, padx=(0, PAD_M))

        self._path_var = ctk.StringVar(value="Ningún archivo seleccionado")
        ctk.CTkEntry(
            file_row, textvariable=self._path_var,
            state="readonly", font=FONT_SMALL,
        ).grid(row=0, column=1, sticky="ew", padx=(0, PAD_M))

        ctk.CTkButton(
            file_row, text="Explorar…", width=100,
            command=self._browse,
        ).grid(row=0, column=2)

        # ── Row 1: Sheet selector (hidden until Excel is loaded) ───────────────
        self._sheet_row = ctk.CTkFrame(self, fg_color="transparent")
        self._sheet_row.grid(row=1, column=0, sticky="ew",
                             padx=PAD_L, pady=(0, PAD_S))
        self._sheet_row.grid_remove()

        ctk.CTkLabel(self._sheet_row, text="Hoja de cálculo:",
                     font=FONT_NORMAL).pack(side="left", padx=(0, PAD_M))
        self._sheet_var = ctk.StringVar()
        self._sheet_combo = ctk.CTkComboBox(
            self._sheet_row, variable=self._sheet_var,
            command=self._on_sheet_change, width=220, font=FONT_SMALL,
        )
        self._sheet_combo.pack(side="left")

        # ── Row 2: Preview area ───────────────────────────────────────────────
        preview_outer = ctk.CTkFrame(self, corner_radius=6)
        preview_outer.grid(row=2, column=0, sticky="nsew",
                           padx=PAD_L, pady=(0, PAD_S))
        preview_outer.rowconfigure(0, weight=1)
        preview_outer.columnconfigure(0, weight=1)

        self._placeholder = ctk.CTkLabel(
            preview_outer,
            text="Selecciona un archivo para previsualizar los datos",
            font=FONT_NORMAL, text_color=("gray45", "gray60"),
        )
        self._placeholder.grid(row=0, column=0)

        # The preview treeview is built inside this frame on demand
        self._preview_outer = preview_outer
        self._preview_tree_frame: ctk.CTkFrame | None = None

        # ── Row 3: Info + buttons ─────────────────────────────────────────────
        bottom = ctk.CTkFrame(self, fg_color="transparent")
        bottom.grid(row=3, column=0, sticky="ew",
                    padx=PAD_L, pady=(0, PAD_L))
        bottom.columnconfigure(0, weight=1)

        self._info_lbl = ctk.CTkLabel(
            bottom, text="", font=FONT_SMALL,
            text_color=("gray40", "gray60"), anchor="w",
        )
        self._info_lbl.grid(row=0, column=0, sticky="w")

        btn_frame = ctk.CTkFrame(bottom, fg_color="transparent")
        btn_frame.grid(row=0, column=1)

        ctk.CTkButton(
            btn_frame, text="Cancelar", width=100,
            fg_color=("gray72", "gray32"),
            hover_color=("gray60", "gray42"),
            command=self._on_cancel,
        ).pack(side="left", padx=PAD_S)

        self._confirm_btn = ctk.CTkButton(
            btn_frame, text="Importar", width=100,
            state="disabled", command=self._on_confirm,
        )
        self._confirm_btn.pack(side="left")

    # ── Event handlers ────────────────────────────────────────────────────────

    def _browse(self) -> None:
        path = filedialog.askopenfilename(
            title="Seleccionar archivo de datos",
            filetypes=[
                ("Archivos de datos", "*.csv *.xlsx *.xls"),
                ("CSV", "*.csv"),
                ("Excel", "*.xlsx *.xls"),
                ("Todos", "*.*"),
            ],
        )
        if not path:
            return

        self._filepath = path
        # Show only filename in entry for readability
        self._path_var.set(path.split("/")[-1].split("\\")[-1])

        if path.lower().endswith((".xlsx", ".xls")):
            try:
                sheets = pd.ExcelFile(path).sheet_names
                self._sheet_combo.configure(values=sheets)
                self._sheet_var.set(sheets[0])
                self._sheet_row.grid()
            except Exception:
                self._sheet_row.grid_remove()
        else:
            self._sheet_row.grid_remove()

        self._load_preview()

    def _on_sheet_change(self, _=None) -> None:
        if self._filepath:
            self._load_preview()

    def _load_preview(self) -> None:
        if not self._filepath:
            return
        try:
            sheet = self._sheet_var.get() or None
            if self._filepath.lower().endswith((".xlsx", ".xls")):
                df = pd.read_excel(self._filepath, sheet_name=sheet, nrows=50)
            else:
                df = pd.read_csv(self._filepath, nrows=50)

            self._render_preview(df)
            self._info_lbl.configure(
                text=f"{len(df.columns)} columnas · {len(df)} filas (vista previa de primeras 50 filas)",
                text_color=("gray40", "gray60"),
            )
            self._confirm_btn.configure(state="normal")
        except Exception as e:
            self._info_lbl.configure(
                text=f"Error al leer archivo: {e}",
                text_color=("red3", "red2"),
            )
            self._confirm_btn.configure(state="disabled")

    def _render_preview(self, df: pd.DataFrame) -> None:
        """Replaces the placeholder with a Treeview showing the DataFrame."""
        if self._placeholder.winfo_exists():
            self._placeholder.grid_remove()

        if self._preview_tree_frame and self._preview_tree_frame.winfo_exists():
            self._preview_tree_frame.destroy()

        outer = ctk.CTkFrame(self._preview_outer, fg_color="transparent")
        outer.grid(row=0, column=0, sticky="nsew", padx=PAD_S, pady=PAD_S)
        outer.rowconfigure(0, weight=1)
        outer.columnconfigure(0, weight=1)
        self._preview_tree_frame = outer

        # Build a minimal dark Treeview
        sb_y = ttk.Scrollbar(outer, orient="vertical",
                              style="Dark.Vertical.TScrollbar")
        sb_y.grid(row=0, column=1, sticky="ns")
        sb_x = ttk.Scrollbar(outer, orient="horizontal",
                              style="Dark.Horizontal.TScrollbar")
        sb_x.grid(row=1, column=0, sticky="ew")

        tree = ttk.Treeview(
            outer, style="Dark.Treeview",
            yscrollcommand=sb_y.set,
            xscrollcommand=sb_x.set,
        )
        tree.grid(row=0, column=0, sticky="nsew")
        sb_y.config(command=tree.yview)
        sb_x.config(command=tree.xview)

        tree["columns"] = list(df.columns)
        tree["show"] = "headings"
        for col in df.columns:
            tree.heading(col, text=str(col))
            tree.column(col, anchor="center", width=90, minwidth=60)
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))

    # ── Confirm ───────────────────────────────────────────────────────────────

    def _on_confirm(self) -> None:
        sheet = self._sheet_var.get() or None
        self._result = {
            "filepath": self._filepath,
            "sheet":    sheet,
        }
        super()._on_confirm()
