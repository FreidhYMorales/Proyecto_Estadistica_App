"""
GraphConfigDialog — floating config window for chart customization.

Decouples chart options (title, axis labels, bins, color) from the panel
toolbar, keeping panel toolbars uncluttered.

Usage
-----
    from views.dialogs.graph_config_dialog import GraphConfigDialog, GraphConfig

    cfg = GraphConfig(bins=15, title="Distribución de edades")
    dlg = GraphConfigDialog(parent, current_config=cfg)
    result: GraphConfig | None = dlg.get_result()
    if result:
        fig, _ = graph_utils.build_histogram(data, result.bins, result.title)
        canvas.render(fig)
"""
from dataclasses import dataclass, field
import customtkinter as ctk

from views.dialogs.base_dialog import BaseDialog
from views.theme import (
    FONT_NORMAL, FONT_SMALL, PAD_XS, PAD_S, PAD_M, PAD_L,
    CLR_BTN_SECONDARY, CLR_HOVER_SECONDARY, CLR_DIVIDER,
)


@dataclass
class GraphConfig:
    """Immutable snapshot of user-chosen chart options."""
    title:     str   = ""
    xlabel:    str   = ""
    ylabel:    str   = ""
    bins:      int   = 10
    color:     str   = "#5b9bd5"
    show_grid: bool  = True


class GraphConfigDialog(BaseDialog):
    """
    Modal dialog for editing GraphConfig.
    Returns a new GraphConfig instance on confirm, None on cancel.
    """

    def __init__(self, parent, current_config: GraphConfig | None = None,
                 show_bins: bool = True):
        """
        Args:
            parent:         Parent window.
            current_config: Pre-populate fields with existing config values.
            show_bins:      Set False to hide the Bins field (e.g. for pie/bar charts).
        """
        self._cfg = current_config or GraphConfig()
        self._show_bins = show_bins
        height = 370 if show_bins else 330
        super().__init__(parent, "Configurar Gráfico", width=420, height=height)

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        self.grid_columnconfigure(1, weight=1)

        self._vars: dict = {}
        row = 0

        def _add_entry(label: str, key: str, default: str) -> None:
            nonlocal row
            ctk.CTkLabel(self, text=label, font=FONT_NORMAL, anchor="w").grid(
                row=row, column=0, sticky="w", padx=(PAD_L, PAD_M), pady=PAD_S)
            var = ctk.StringVar(value=default)
            ctk.CTkEntry(self, textvariable=var, font=FONT_SMALL).grid(
                row=row, column=1, sticky="ew", padx=(0, PAD_L), pady=PAD_S)
            self._vars[key] = var
            row += 1

        _add_entry("Título:",    "title",  self._cfg.title)
        _add_entry("Eje X:",     "xlabel", self._cfg.xlabel)
        _add_entry("Eje Y:",     "ylabel", self._cfg.ylabel)
        _add_entry("Color hex:", "color",  self._cfg.color)

        if self._show_bins:
            ctk.CTkLabel(self, text="Bins:", font=FONT_NORMAL, anchor="w").grid(
                row=row, column=0, sticky="w", padx=(PAD_L, PAD_M), pady=PAD_S)
            var_bins = ctk.StringVar(value=str(self._cfg.bins))
            ctk.CTkEntry(self, textvariable=var_bins,
                         font=FONT_SMALL, width=80).grid(
                row=row, column=1, sticky="w", padx=(0, PAD_L), pady=PAD_S)
            self._vars["bins"] = var_bins
            row += 1

        # Grid switch
        ctk.CTkLabel(self, text="Mostrar grilla:", font=FONT_NORMAL, anchor="w").grid(
            row=row, column=0, sticky="w", padx=(PAD_L, PAD_M), pady=PAD_S)
        var_grid = ctk.BooleanVar(value=self._cfg.show_grid)
        ctk.CTkSwitch(self, variable=var_grid, text="").grid(
            row=row, column=1, sticky="w", padx=(0, PAD_L), pady=PAD_S)
        self._vars["show_grid"] = var_grid
        row += 1

        # Separator
        ctk.CTkFrame(self, height=1, fg_color=CLR_DIVIDER).grid(
            row=row, column=0, columnspan=2, sticky="ew",
            padx=PAD_L, pady=(PAD_S, 0))
        row += 1

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=row, column=0, columnspan=2,
                       sticky="e", padx=PAD_L, pady=PAD_M)

        ctk.CTkButton(
            btn_frame, text="Cancelar", width=100,
            fg_color=CLR_BTN_SECONDARY,
            hover_color=CLR_HOVER_SECONDARY,
            command=self._on_cancel,
        ).pack(side="left", padx=PAD_S)

        ctk.CTkButton(
            btn_frame, text="Aplicar", width=100,
            command=self._on_confirm,
        ).pack(side="left")

    # ── Confirm ───────────────────────────────────────────────────────────────

    def _on_confirm(self) -> None:
        try:
            bins = int(self._vars["bins"].get()) if "bins" in self._vars else self._cfg.bins
            if bins < 1:
                bins = 1
        except ValueError:
            bins = 10

        self._result = GraphConfig(
            title=self._vars["title"].get(),
            xlabel=self._vars["xlabel"].get(),
            ylabel=self._vars["ylabel"].get(),
            color=self._vars["color"].get() or "#5b9bd5",
            bins=bins,
            show_grid=self._vars["show_grid"].get(),
        )
        super()._on_confirm()
