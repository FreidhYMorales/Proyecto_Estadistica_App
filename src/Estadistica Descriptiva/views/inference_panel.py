"""
Panel de Inferencia Estadística.

Secciones:
  1. Intervalos de Confianza
     - IC para Proporción (Wald o Wilson)
     - IC para Media con σ conocida (distribución Z)
     - IC para Media con σ desconocida (distribución t-Student)
  2. Tamaño de Muestra
     - Para proporción
     - Para media

Cada resultado muestra texto formateado. Los IC de media opcionalmente
renderizan un gráfico de la distribución con la región sombreada.
"""
from tkinter import messagebox
import customtkinter as ctk

from views.theme import (
    FONT_SECTION, FONT_SMALL,
    PAD_XS, PAD_S, PAD_M, PAD_L,
    TOOLBAR_H, TOOLBAR_BG,
    CLR_BTN_SECONDARY, CLR_HOVER_SECONDARY,
    CLR_DIVIDER, CLR_PLACEHOLDER,
)
from views.components import clear_frame, CTkDropdown, ResultTextWidget, GraphCanvas, DataTreeview


def _parse_nc(text: str) -> float:
    """Convierte '95', '95%' o '0.95' a fracción (0, 1). Lanza ValueError si es inválido."""
    s = text.strip().rstrip("%").strip()
    v = float(s)
    if v <= 0:
        raise ValueError("El nivel de confianza debe ser mayor que 0.")
    if v >= 100:
        raise ValueError("El nivel de confianza debe ser menor que 100.")
    return v / 100 if v >= 1 else v


class InferencePanel:
    """Panel registrado en ContentStack bajo la clave 'inference'."""

    def __init__(self, parent, controller):
        self._ctrl = controller

        self._root = ctk.CTkFrame(parent, fg_color="transparent")
        self._root.grid(row=0, column=0, sticky="nsew")
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self._root.rowconfigure(1, weight=1)
        self._root.columnconfigure(0, weight=1)

        self._toolbar = ctk.CTkFrame(
            self._root, height=TOOLBAR_H, fg_color=TOOLBAR_BG, corner_radius=0
        )
        self._toolbar.grid(row=0, column=0, sticky="ew")

        self._content = ctk.CTkFrame(self._root, fg_color="transparent")
        self._content.grid(row=1, column=0, sticky="nsew")
        self._content.rowconfigure(1, weight=1)
        self._content.columnconfigure(0, weight=1)

        self._build_toolbar()

    # ── Toolbar ───────────────────────────────────────────────────────────────

    def _build_toolbar(self) -> None:
        CTkDropdown(
            self._toolbar, "IC — Proporción",
            items=[
                ("Calcular IC para Proporción (éxitos / n)", self._show_ic_prop),
                ("Calcular IC para Proporción (p directo)",  self._show_ic_prop_directa),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "IC — Media",
            items=[
                ("σ conocida (distribución Z)", self._show_ic_media_z),
                ("σ desconocida — datos cargados (t-Student)", self._show_ic_media_t_data),
                ("σ desconocida — valores manuales (t-Student)", self._show_ic_media_t_manual),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "IC — Varianza",
            items=[
                ("Desde datos cargados", self._show_ic_var_datos),
                ("Valores manuales (s, n)", self._show_ic_var_manual),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "IC — Dos Muestras",
            items=[
                ("σ conocidas — Caso 1 (Z)",                   self._show_ic_2m_caso1),
                ("σ desconocidas, varianzas iguales — Caso 2 (t)", self._show_ic_2m_caso2),
                ("σ desconocidas, varianzas distintas — Caso 3 (t Welch)", self._show_ic_2m_caso3),
                ("Muestras grandes n≥30 — Caso 4 (Z)",         self._show_ic_2m_caso4),
                ("Muestras pareadas",                           self._show_ic_2m_pareadas),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "Muestra — Con N",
            items=[
                ("Para proporción (Con N conocida)", self._show_ss_prop_con_n),
                ("Para media (Con N conocida)",      self._show_ss_media_con_n),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "Muestra — Sin N",
            items=[
                ("Para proporción (Sin N)", self._show_ss_prop_sin_n),
                ("Para media (Sin N)",      self._show_ss_media_sin_n),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "Estimación Puntual",
            items=[
                ("Proporciones — tabla n + IC", self._show_ep_proporciones),
                ("Medias — tabla n + IC",        self._show_ep_medias),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

    # ── Layout helpers ────────────────────────────────────────────────────────

    def _make_text_panel(self, titulo: str):
        """Retorna (control_frame, ResultTextWidget)."""
        clear_frame(self._content)
        for r in range(4):
            self._content.rowconfigure(r, weight=0)
        self._content.rowconfigure(2, weight=1)

        ctk.CTkLabel(self._content, text=titulo, font=FONT_SECTION, anchor="w").grid(
            row=0, column=0, sticky="w", padx=PAD_L, pady=(PAD_M, 0)
        )

        control = ctk.CTkFrame(self._content, fg_color="transparent")
        control.grid(row=1, column=0, sticky="ew", padx=PAD_M, pady=PAD_S)

        result_frame = ctk.CTkFrame(self._content, fg_color="transparent")
        result_frame.grid(row=2, column=0, sticky="nsew")
        result_frame.rowconfigure(0, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result = ResultTextWidget(result_frame, font=("Courier", 11))
        return control, result

    def _make_graph_panel(self, titulo: str):
        """Retorna (control_frame, result_widget, graph_canvas) en layout 40/30/30."""
        clear_frame(self._content)
        for row in range(4):
            self._content.rowconfigure(row, weight=0)
        self._content.rowconfigure(2, weight=2)
        self._content.rowconfigure(3, weight=3)
        self._content.columnconfigure(0, weight=1)

        ctk.CTkLabel(self._content, text=titulo, font=FONT_SECTION, anchor="w").grid(
            row=0, column=0, sticky="w", padx=PAD_L, pady=(PAD_M, 0)
        )

        control = ctk.CTkFrame(self._content, fg_color="transparent")
        control.grid(row=1, column=0, sticky="ew", padx=PAD_M, pady=PAD_S)

        result_frame = ctk.CTkFrame(self._content, fg_color="transparent")
        result_frame.grid(row=2, column=0, sticky="nsew")
        result_frame.rowconfigure(0, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result = ResultTextWidget(result_frame, font=("Courier", 11))

        graph_frame = ctk.CTkFrame(self._content, fg_color="transparent")
        graph_frame.grid(row=3, column=0, sticky="nsew")
        graph_frame.rowconfigure(0, weight=1)
        graph_frame.columnconfigure(0, weight=1)
        graph = GraphCanvas(graph_frame)

        return control, result, graph

    def _make_sample_panel(self, titulo: str):
        """Layout: title → controls → small text result → expandable sample table.
        Returns (control_frame, ResultTextWidget, DataTreeview)."""
        clear_frame(self._content)
        for r in range(4):
            self._content.rowconfigure(r, weight=0)
        self._content.rowconfigure(3, weight=1)
        self._content.columnconfigure(0, weight=1)

        ctk.CTkLabel(self._content, text=titulo, font=FONT_SECTION, anchor="w").grid(
            row=0, column=0, sticky="w", padx=PAD_L, pady=(PAD_M, 0)
        )
        control = ctk.CTkFrame(self._content, fg_color="transparent")
        control.grid(row=1, column=0, sticky="ew", padx=PAD_M, pady=PAD_S)

        # Fixed-height text result area
        result_outer = ctk.CTkFrame(self._content, fg_color="transparent", height=100)
        result_outer.grid(row=2, column=0, sticky="ew")
        result_outer.grid_propagate(False)
        result_outer.rowconfigure(0, weight=1)
        result_outer.columnconfigure(0, weight=1)
        result = ResultTextWidget(result_outer, font=("Courier", 11))

        # Sample table (expandable)
        table_frame = ctk.CTkFrame(self._content, fg_color="transparent")
        table_frame.grid(row=3, column=0, sticky="nsew")
        table_frame.rowconfigure(1, weight=1)
        table_frame.columnconfigure(0, weight=1)
        ctk.CTkLabel(
            table_frame,
            text="Muestra aleatoria extraída del dataset cargado:",
            font=FONT_SMALL, anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=PAD_M, pady=(PAD_S, 0))
        tree_inner = ctk.CTkFrame(table_frame, fg_color="transparent")
        tree_inner.grid(row=1, column=0, sticky="nsew")
        tree_inner.rowconfigure(0, weight=1)
        tree_inner.columnconfigure(0, weight=1)
        tree = DataTreeview(tree_inner)

        return control, result, tree

    def _nc_combo(self, parent) -> ctk.CTkEntry:
        ctk.CTkLabel(parent, text="Confianza %:", font=FONT_SMALL).pack(side="left", padx=PAD_S)
        entry = ctk.CTkEntry(parent, width=55, height=28, font=FONT_SMALL)
        entry.insert(0, "95")
        entry.pack(side="left", padx=PAD_S)
        return entry

    def _labeled_entry(self, parent, label: str, default: str, width: int = 90) -> ctk.CTkEntry:
        ctk.CTkLabel(parent, text=label, font=FONT_SMALL).pack(side="left", padx=(PAD_M, PAD_S))
        entry = ctk.CTkEntry(parent, width=width, height=28, font=FONT_SMALL)
        entry.insert(0, default)
        entry.pack(side="left", padx=PAD_S)
        return entry

    def _col_combo(self, parent, label: str = "Variable:") -> ctk.CTkComboBox:
        ctk.CTkLabel(parent, text=label, font=FONT_SMALL).pack(side="left", padx=PAD_S)
        combo = ctk.CTkComboBox(
            parent, values=list(self._ctrl.columns),
            state="readonly", font=FONT_SMALL, width=150, height=28,
        )
        if self._ctrl.columns:
            combo.set(self._ctrl.columns[0])
        combo.pack(side="left", padx=PAD_S)
        return combo

    # ── IC Proporción ─────────────────────────────────────────────────────────

    def _show_ic_prop(self) -> None:
        control, result = self._make_text_panel("IC para Proporción")

        nc_combo = self._nc_combo(control)
        exitos_e = self._labeled_entry(control, "Éxitos:", "50")
        n_e = self._labeled_entry(control, "n:", "100")

        ctk.CTkLabel(control, text="Método:", font=FONT_SMALL).pack(side="left", padx=PAD_S)
        met_combo = ctk.CTkComboBox(
            control, values=["normal (Wald)", "wilson"],
            state="readonly", font=FONT_SMALL, width=130, height=28,
        )
        met_combo.set("normal (Wald)")
        met_combo.pack(side="left", padx=PAD_S)

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                metodo = "wilson" if "wilson" in met_combo.get() else "normal"
                res = self._ctrl.ic_proporcion(int(exitos_e.get()), int(n_e.get()), nc, metodo)
                result.set(_fmt_ic(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("ic_proporcion.txt")).pack(
            side="left", padx=PAD_S)

    # ── IC Media σ conocida ───────────────────────────────────────────────────

    def _show_ic_media_z(self) -> None:
        control, result, graph = self._make_graph_panel("IC para Media — σ conocida (Z)")

        nc_combo = self._nc_combo(control)
        media_e = self._labeled_entry(control, "Media (x̄):", "0")
        sigma_e = self._labeled_entry(control, "σ:", "1")
        n_e = self._labeled_entry(control, "n:", "30")

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                res = self._ctrl.ic_media_z(
                    float(media_e.get()), float(sigma_e.get()), int(n_e.get()), nc
                )
                result.set(_fmt_ic(res))
                # Gráfico de distribución
                import utils.inference_graphs as ig
                fig, _ = ig.build_normal_dist_ic(
                    res["media_muestral"], res["error_estandar"],
                    res["z"], f"{nc*100:.4g}%",
                    "Distribución Normal — IC para Media"
                )
                graph.render(fig)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("ic_media_z.txt")).pack(
            side="left", padx=PAD_S)

    # ── IC Media σ desconocida — datos ────────────────────────────────────────

    def _show_ic_media_t_data(self) -> None:
        control, result, graph = self._make_graph_panel(
            "IC para Media — σ desconocida con datos (t-Student)")

        nc_combo = self._nc_combo(control)
        col_combo = self._col_combo(control)

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                datos = self._ctrl.get_numeric_column(col_combo.get())
                if not datos:
                    messagebox.showerror("Error", "No hay datos numéricos en esa columna.")
                    return
                res = self._ctrl.ic_media_t_datos(datos, nc)
                result.set(_fmt_ic(res))
                import utils.inference_graphs as ig
                fig, _ = ig.build_normal_dist_ic(
                    res["media_muestral"], res["error_estandar"],
                    res["t_critico"], f"{nc*100:.4g}%",
                    f"Distribución t-Student — IC para Media ({col_combo.get()})"
                )
                graph.render(fig)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("ic_media_t.txt")).pack(
            side="left", padx=PAD_S)

    # ── IC Media σ desconocida — manual ──────────────────────────────────────

    def _show_ic_media_t_manual(self) -> None:
        control, result, graph = self._make_graph_panel(
            "IC para Media — σ desconocida, valores manuales (t-Student)")

        nc_combo = self._nc_combo(control)
        media_e = self._labeled_entry(control, "Media (x̄):", "0")
        s_e = self._labeled_entry(control, "s (desv.):", "1")
        n_e = self._labeled_entry(control, "n:", "30")

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                res = self._ctrl.ic_media_t_manual(
                    float(media_e.get()), float(s_e.get()), int(n_e.get()), nc
                )
                result.set(_fmt_ic(res))
                import utils.inference_graphs as ig
                fig, _ = ig.build_normal_dist_ic(
                    res["media_muestral"], res["error_estandar"],
                    res["t_critico"], f"{nc*100:.4g}%",
                    "Distribución t-Student — IC para Media"
                )
                graph.render(fig)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("ic_media_t_manual.txt")).pack(
            side="left", padx=PAD_S)

    # ── IC Varianza — desde datos ─────────────────────────────────────────────

    def _show_ic_var_datos(self) -> None:
        control, result = self._make_text_panel(
            "IC para Varianza — desde datos cargados (χ²)")

        nc_combo = self._nc_combo(control)
        col_combo = self._col_combo(control)

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                datos = self._ctrl.get_numeric_column(col_combo.get())
                if not datos:
                    messagebox.showerror("Error", "No hay datos numéricos en esa columna.")
                    return
                res = self._ctrl.ic_varianza(nc, datos=datos)
                result.set(_fmt_ic_varianza(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("ic_varianza_datos.txt")).pack(
            side="left", padx=PAD_S)

    # ── IC Varianza — manual ──────────────────────────────────────────────────

    def _show_ic_var_manual(self) -> None:
        control, result = self._make_text_panel(
            "IC para Varianza — valores manuales (χ²)")

        nc_combo = self._nc_combo(control)
        s_entry = self._labeled_entry(control, "s (desv. muestral):", "3.5")
        n_entry = self._labeled_entry(control, "n:", "25")

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                res = self._ctrl.ic_varianza(
                    nc,
                    desv_muestral=float(s_entry.get()),
                    n=int(n_entry.get()),
                )
                result.set(_fmt_ic_varianza(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("ic_varianza_manual.txt")).pack(
            side="left", padx=PAD_S)

    # ── Tamaño de muestra — Proporción con N conocida ─────────────────────────

    def _show_ss_prop_con_n(self) -> None:
        control, result, tree = self._make_sample_panel(
            "Tamaño de Muestra — Proporción (Con N conocida)")

        nc_combo = self._nc_combo(control)
        e_entry  = self._labeled_entry(control, "Margen error (e):", "0.05")
        p_entry  = self._labeled_entry(control, "p esperada:", "0.5")
        n_entry  = self._labeled_entry(control, "N población:", "500", width=110)
        pe_entry = self._labeled_entry(control, "% pérdidas (0-1):", "", width=80)

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                N_txt = n_entry.get().strip()
                if not N_txt:
                    messagebox.showerror("Error", "Ingrese el tamaño de la población N.")
                    return
                pe_txt = pe_entry.get().strip()
                res = self._ctrl.sample_size_proportion(
                    float(e_entry.get()), float(p_entry.get()), nc,
                    int(N_txt), float(pe_txt) if pe_txt else None,
                )
                result.set(_fmt_sample_size(res))
                _draw_sample(res["n_recomendada"], self._ctrl, tree)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular y Muestrear", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar resultado", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("muestra_prop_con_n.txt")).pack(
            side="left", padx=PAD_S)

    # ── Tamaño de muestra — Proporción sin N ──────────────────────────────────

    def _show_ss_prop_sin_n(self) -> None:
        control, result = self._make_text_panel(
            "Tamaño de Muestra — Proporción (Sin N conocida)")

        nc_combo = self._nc_combo(control)
        e_entry  = self._labeled_entry(control, "Margen error (e):", "0.05")
        p_entry  = self._labeled_entry(control, "p esperada:", "0.5")
        pe_entry = self._labeled_entry(control, "% pérdidas (0-1):", "", width=80)

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                pe_txt = pe_entry.get().strip()
                res = self._ctrl.sample_size_proportion(
                    float(e_entry.get()), float(p_entry.get()), nc,
                    None, float(pe_txt) if pe_txt else None,
                )
                result.set(_fmt_sample_size(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("muestra_prop_sin_n.txt")).pack(
            side="left", padx=PAD_S)

    # ── Tamaño de muestra — Media con N conocida ──────────────────────────────

    def _show_ss_media_con_n(self) -> None:
        control, result, tree = self._make_sample_panel(
            "Tamaño de Muestra — Media (Con N conocida)")

        nc_combo = self._nc_combo(control)
        e_entry  = self._labeled_entry(control, "Margen error (e):", "5")
        s_entry  = self._labeled_entry(control, "σ (desv. estándar):", "15")
        n_entry  = self._labeled_entry(control, "N población:", "500", width=110)
        pe_entry = self._labeled_entry(control, "% pérdidas (0-1):", "", width=80)

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                N_txt = n_entry.get().strip()
                if not N_txt:
                    messagebox.showerror("Error", "Ingrese el tamaño de la población N.")
                    return
                pe_txt = pe_entry.get().strip()
                res = self._ctrl.sample_size_mean(
                    float(e_entry.get()), float(s_entry.get()), nc,
                    int(N_txt), float(pe_txt) if pe_txt else None,
                )
                result.set(_fmt_sample_size(res))
                _draw_sample(res["n_recomendada"], self._ctrl, tree)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular y Muestrear", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar resultado", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("muestra_media_con_n.txt")).pack(
            side="left", padx=PAD_S)

    # ── Tamaño de muestra — Media sin N ──────────────────────────────────────

    def _show_ss_media_sin_n(self) -> None:
        control, result = self._make_text_panel(
            "Tamaño de Muestra — Media (Sin N conocida)")

        nc_combo = self._nc_combo(control)
        e_entry  = self._labeled_entry(control, "Margen error (e):", "5")
        s_entry  = self._labeled_entry(control, "σ (desv. estándar):", "15")
        pe_entry = self._labeled_entry(control, "% pérdidas (0-1):", "", width=80)

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                pe_txt = pe_entry.get().strip()
                res = self._ctrl.sample_size_mean(
                    float(e_entry.get()), float(s_entry.get()), nc,
                    None, float(pe_txt) if pe_txt else None,
                )
                result.set(_fmt_sample_size(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("muestra_media_sin_n.txt")).pack(
            side="left", padx=PAD_S)


    # ── IC Proporción — p directo ─────────────────────────────────────────────

    def _show_ic_prop_directa(self) -> None:
        control, result = self._make_text_panel("IC para Proporción — p directo")

        nc_combo = self._nc_combo(control)
        p_e = self._labeled_entry(control, "p (0–1):", "0.45", width=80)
        n_e = self._labeled_entry(control, "n:", "100")

        ctk.CTkLabel(control, text="Método:", font=FONT_SMALL).pack(side="left", padx=PAD_S)
        met_combo = ctk.CTkComboBox(
            control, values=["normal (Wald)", "wilson"],
            state="readonly", font=FONT_SMALL, width=130, height=28,
        )
        met_combo.set("normal (Wald)")
        met_combo.pack(side="left", padx=PAD_S)

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                metodo = "wilson" if "wilson" in met_combo.get() else "normal"
                res = self._ctrl.ic_proporcion_directa(
                    float(p_e.get()), int(n_e.get()), nc, metodo
                )
                result.set(_fmt_ic_prop_directa(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("ic_proporcion_p.txt")).pack(
            side="left", padx=PAD_S)

    # ── IC Dos Muestras — helpers de layout ───────────────────────────────────

    def _two_sample_rows(self, control, label_a: str, label_b: str,
                         defaults_a: tuple, defaults_b: tuple, widths: tuple):
        """Crea filas Muestra A / B dentro del control frame. Retorna (nc_combo, entries_a, entries_b, btn_row)."""
        row0 = ctk.CTkFrame(control, fg_color="transparent")
        row0.pack(fill="x", pady=(0, PAD_XS))
        nc_combo = self._nc_combo(row0)

        w1, w2, w3 = widths

        row1 = ctk.CTkFrame(control, fg_color="transparent")
        row1.pack(fill="x", pady=PAD_XS)
        ctk.CTkLabel(row1, text="Muestra A:", font=FONT_SMALL, width=85,
                     anchor="w").pack(side="left", padx=(PAD_M, 0))
        entries_a = [
            self._labeled_entry(row1, lbl, dflt, width=w)
            for lbl, dflt, w in zip(label_a, defaults_a, (w1, w2, w3))
        ]

        row2 = ctk.CTkFrame(control, fg_color="transparent")
        row2.pack(fill="x", pady=PAD_XS)
        ctk.CTkLabel(row2, text="Muestra B:", font=FONT_SMALL, width=85,
                     anchor="w").pack(side="left", padx=(PAD_M, 0))
        entries_b = [
            self._labeled_entry(row2, lbl, dflt, width=w)
            for lbl, dflt, w in zip(label_b, defaults_b, (w1, w2, w3))
        ]

        row3 = ctk.CTkFrame(control, fg_color="transparent")
        row3.pack(fill="x", pady=PAD_XS)

        return nc_combo, entries_a, entries_b, row3

    # ── IC Dos Muestras — Caso 1 ─────────────────────────────────────────────

    def _show_ic_2m_caso1(self) -> None:
        control, result = self._make_text_panel(
            "IC — Diferencia de Medias: σ₁, σ₂ conocidas (Caso 1, Z)")

        labels  = ("n₁:", "x̄₁:", "σ₁:")
        defs_a  = ("50", "985", "12")
        defs_b  = ("60", "960", "18")
        nc_combo, ea, eb, btn_row = self._two_sample_rows(
            control, labels, labels, defs_a, defs_b, (55, 70, 70))

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                res = self._ctrl.ic_dos_medias_caso1(
                    int(ea[0].get()), float(ea[1].get()), float(ea[2].get()),
                    int(eb[0].get()), float(eb[1].get()), float(eb[2].get()),
                    nc,
                )
                result.set(_fmt_ic_dos_medias(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(btn_row, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(btn_row, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("ic_2m_caso1.txt")).pack(
            side="left", padx=PAD_S)

    # ── IC Dos Muestras — Caso 2 ─────────────────────────────────────────────

    def _show_ic_2m_caso2(self) -> None:
        control, result = self._make_text_panel(
            "IC — Diferencia de Medias: varianzas iguales (Caso 2, t sp²)")

        labels  = ("n:", "x̄:", "s:")
        defs_a  = ("12", "450", "30")
        defs_b  = ("10", "410", "25")
        nc_combo, ea, eb, btn_row = self._two_sample_rows(
            control, labels, labels, defs_a, defs_b, (55, 70, 70))

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                res = self._ctrl.ic_dos_medias_caso2(
                    int(ea[0].get()), float(ea[1].get()), float(ea[2].get()),
                    int(eb[0].get()), float(eb[1].get()), float(eb[2].get()),
                    nc,
                )
                result.set(_fmt_ic_dos_medias(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(btn_row, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(btn_row, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("ic_2m_caso2.txt")).pack(
            side="left", padx=PAD_S)

    # ── IC Dos Muestras — Caso 3 ─────────────────────────────────────────────

    def _show_ic_2m_caso3(self) -> None:
        control, result = self._make_text_panel(
            "IC — Diferencia de Medias: varianzas distintas (Caso 3, t Welch)")

        labels  = ("n:", "x̄:", "s:")
        defs_a  = ("8", "45", "3")
        defs_b  = ("10", "52", "8")
        nc_combo, ea, eb, btn_row = self._two_sample_rows(
            control, labels, labels, defs_a, defs_b, (55, 70, 70))

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                res = self._ctrl.ic_dos_medias_caso3(
                    int(ea[0].get()), float(ea[1].get()), float(ea[2].get()),
                    int(eb[0].get()), float(eb[1].get()), float(eb[2].get()),
                    nc,
                )
                result.set(_fmt_ic_dos_medias(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(btn_row, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(btn_row, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("ic_2m_caso3.txt")).pack(
            side="left", padx=PAD_S)

    # ── IC Dos Muestras — Caso 4 ─────────────────────────────────────────────

    def _show_ic_2m_caso4(self) -> None:
        control, result = self._make_text_panel(
            "IC — Diferencia de Medias: muestras grandes n≥30 (Caso 4, Z)")

        labels  = ("n≥30:", "x̄:", "s:")
        defs_a  = ("40", "120", "15")
        defs_b  = ("50", "132", "20")
        nc_combo, ea, eb, btn_row = self._two_sample_rows(
            control, labels, labels, defs_a, defs_b, (55, 70, 70))

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                res = self._ctrl.ic_dos_medias_caso4(
                    int(ea[0].get()), float(ea[1].get()), float(ea[2].get()),
                    int(eb[0].get()), float(eb[1].get()), float(eb[2].get()),
                    nc,
                )
                result.set(_fmt_ic_dos_medias(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(btn_row, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(btn_row, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("ic_2m_caso4.txt")).pack(
            side="left", padx=PAD_S)

    # ── IC Dos Muestras — Caso Pareadas ──────────────────────────────────────

    def _show_ic_2m_pareadas(self) -> None:
        control, result = self._make_text_panel(
            "IC — Diferencia de Medias: Muestras Pareadas (t)")

        nc_combo = self._nc_combo(control)
        n_e    = self._labeled_entry(control, "n (pares):", "10", width=60)
        dbar_e = self._labeled_entry(control, "d̄:", "5.2", width=80)
        sd_e   = self._labeled_entry(control, "Sd:", "2.8", width=70)

        def calcular():
            try:
                nc = _parse_nc(nc_combo.get())
                res = self._ctrl.ic_dos_medias_pareadas(
                    int(n_e.get()), float(dbar_e.get()), float(sd_e.get()), nc
                )
                result.set(_fmt_ic_dos_medias(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("ic_2m_pareadas.txt")).pack(
            side="left", padx=PAD_S)


    # ── Estimación Puntual — layout helper ───────────────────────────────────

    def _make_ep_panel(self, titulo: str):
        """Returns (ctrl_tabla, DataTreeview, ctrl_ic, ResultTextWidget).
        Layout: title → table params → expandable n-table → divider → IC params → IC result."""
        clear_frame(self._content)
        for r in range(7):
            self._content.rowconfigure(r, weight=0)
        self._content.rowconfigure(2, weight=2)
        self._content.rowconfigure(6, weight=1)
        self._content.columnconfigure(0, weight=1)

        ctk.CTkLabel(self._content, text=titulo, font=FONT_SECTION, anchor="w").grid(
            row=0, column=0, sticky="w", padx=PAD_L, pady=(PAD_M, 0))

        ctrl_tabla = ctk.CTkFrame(self._content, fg_color="transparent")
        ctrl_tabla.grid(row=1, column=0, sticky="ew", padx=PAD_M, pady=(PAD_S, 0))

        table_outer = ctk.CTkFrame(self._content, fg_color="transparent")
        table_outer.grid(row=2, column=0, sticky="nsew", padx=PAD_M, pady=PAD_S)
        table_outer.rowconfigure(0, weight=1)
        table_outer.columnconfigure(0, weight=1)
        tree = DataTreeview(table_outer)

        ctk.CTkFrame(self._content, height=1, fg_color=CLR_DIVIDER).grid(
            row=3, column=0, sticky="ew", padx=PAD_L, pady=(0, PAD_XS))
        ctk.CTkLabel(
            self._content,
            text="Desde la muestra observada — calcular intervalo de confianza:",
            font=FONT_SMALL, anchor="w", text_color=CLR_PLACEHOLDER,
        ).grid(row=4, column=0, sticky="w", padx=PAD_L, pady=(0, PAD_XS))

        ctrl_ic = ctk.CTkFrame(self._content, fg_color="transparent")
        ctrl_ic.grid(row=5, column=0, sticky="ew", padx=PAD_M, pady=(0, PAD_S))

        result_outer = ctk.CTkFrame(self._content, fg_color="transparent")
        result_outer.grid(row=6, column=0, sticky="nsew")
        result_outer.rowconfigure(0, weight=1)
        result_outer.columnconfigure(0, weight=1)
        result = ResultTextWidget(result_outer, font=("Courier", 11))

        return ctrl_tabla, tree, ctrl_ic, result

    # ── Estimación Puntual — Proporciones ─────────────────────────────────────

    def _show_ep_proporciones(self) -> None:
        ctrl_tabla, tree, ctrl_ic, result = self._make_ep_panel(
            "Estimación Puntual — Proporciones")

        nc_t = self._nc_combo(ctrl_tabla)
        n_t  = self._labeled_entry(ctrl_tabla, "N (opcional):", "", width=100)
        d_t  = self._labeled_entry(ctrl_tabla, "Error máx. d:", "0.03")

        def generar():
            try:
                nc    = _parse_nc(nc_t.get())
                N_txt = n_t.get().strip()
                N_val = int(N_txt) if N_txt else None
                d     = float(d_t.get())
                rows  = []
                for i in range(1, 10):
                    p   = round(i * 0.1, 1)
                    res = self._ctrl.sample_size_proportion(d, p, nc, N_val)
                    row = {
                        "p": p,
                        "q (1−p)": round(1 - p, 1),
                        "n (pob. infinita)": res["n_poblacion_infinita"],
                    }
                    if N_val is not None:
                        row["n ajustada (con N)"] = res.get("n_ajustada_finita", "—")
                    rows.append(row)
                import pandas as pd
                tree.load(pd.DataFrame(rows))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(ctrl_tabla, text="Generar Tabla", font=FONT_SMALL, height=28,
                      command=generar).pack(side="left", padx=PAD_M)

        nc_ic   = self._nc_combo(ctrl_ic)
        p_hat_e = self._labeled_entry(ctrl_ic, "p̂ observado (0–1):", "0.28", width=80)
        n_ic_e  = self._labeled_entry(ctrl_ic, "n muestra:", "200")
        ctk.CTkLabel(ctrl_ic, text="Método:", font=FONT_SMALL).pack(side="left", padx=PAD_S)
        met = ctk.CTkComboBox(ctrl_ic, values=["normal (Wald)", "wilson"],
                              state="readonly", font=FONT_SMALL, width=130, height=28)
        met.set("normal (Wald)")
        met.pack(side="left", padx=PAD_S)

        def calcular_ic():
            try:
                nc     = _parse_nc(nc_ic.get())
                metodo = "wilson" if "wilson" in met.get() else "normal"
                res    = self._ctrl.ic_proporcion_directa(
                    float(p_hat_e.get()), int(n_ic_e.get()), nc, metodo)
                result.set(_fmt_ic_prop_directa(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(ctrl_ic, text="Calcular IC", font=FONT_SMALL, height=28,
                      command=calcular_ic).pack(side="left", padx=PAD_M)
        ctk.CTkButton(ctrl_ic, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("ep_proporcion_ic.txt")).pack(
            side="left", padx=PAD_S)

    # ── Estimación Puntual — Medias ───────────────────────────────────────────

    def _show_ep_medias(self) -> None:
        ctrl_tabla, tree, ctrl_ic, result = self._make_ep_panel(
            "Estimación Puntual — Medias")

        nc_t    = self._nc_combo(ctrl_tabla)
        n_t     = self._labeled_entry(ctrl_tabla, "N (opcional):", "", width=100)
        d_t     = self._labeled_entry(ctrl_tabla, "Error máx. d:", "50")
        sigma_t = self._labeled_entry(ctrl_tabla, "σ referencia:", "100")

        def generar():
            try:
                nc     = _parse_nc(nc_t.get())
                N_txt  = n_t.get().strip()
                N_val  = int(N_txt) if N_txt else None
                d      = float(d_t.get())
                s_base = float(sigma_t.get())
                factors = [0.1, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0]
                rows = []
                for f in factors:
                    s_val = round(s_base * f, 4)
                    res   = self._ctrl.sample_size_mean(d, s_val, nc, N_val)
                    row   = {
                        "σ": s_val,
                        "n (pob. infinita)": res["n_poblacion_infinita"],
                    }
                    if N_val is not None:
                        row["n ajustada (con N)"] = res.get("n_ajustada_finita", "—")
                    rows.append(row)
                import pandas as pd
                tree.load(pd.DataFrame(rows))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(ctrl_tabla, text="Generar Tabla", font=FONT_SMALL, height=28,
                      command=generar).pack(side="left", padx=PAD_M)

        nc_ic   = self._nc_combo(ctrl_ic)
        x_bar_e = self._labeled_entry(ctrl_ic, "x̄ observado:", "3200", width=100)
        s_ic_e  = self._labeled_entry(ctrl_ic, "s muestral:", "500")
        n_ic_e  = self._labeled_entry(ctrl_ic, "n muestra:", "379")

        def calcular_ic():
            try:
                nc  = _parse_nc(nc_ic.get())
                res = self._ctrl.ic_media_t_manual(
                    float(x_bar_e.get()), float(s_ic_e.get()), int(n_ic_e.get()), nc)
                result.set(_fmt_ic(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(ctrl_ic, text="Calcular IC", font=FONT_SMALL, height=28,
                      command=calcular_ic).pack(side="left", padx=PAD_M)
        ctk.CTkButton(ctrl_ic, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=CLR_BTN_SECONDARY, hover_color=CLR_HOVER_SECONDARY,
                      command=lambda: result.export("ep_media_ic.txt")).pack(
            side="left", padx=PAD_S)


# ── Sample drawing helper ─────────────────────────────────────────────────────

def _draw_sample(n_recomendada: int, ctrl, tree: DataTreeview) -> None:
    """Draw n_recomendada random rows from the loaded dataset into the tree."""
    df = ctrl.get_dataframe()
    if df.empty:
        messagebox.showwarning(
            "Sin datos",
            f"n recomendada = {n_recomendada}.\n"
            "No hay dataset cargado para extraer la muestra.\n"
            "Importe un archivo desde la barra lateral.",
        )
        return
    actual_n = min(n_recomendada, len(df))
    sampled = df.sample(actual_n).reset_index(drop=True)
    tree.load(sampled)
    if actual_n < n_recomendada:
        messagebox.showwarning(
            "Dataset pequeño",
            f"El dataset solo tiene {len(df)} filas.\n"
            f"Se extrajeron {actual_n} en lugar de {n_recomendada}.",
        )


# ── Formatting helpers ────────────────────────────────────────────────────────

def _fmt_ic(r: dict) -> str:
    tipo = r.get("tipo", "")
    lineas = [
        "=" * 58,
        f"  INTERVALO DE CONFIANZA — {tipo.upper()}",
        "=" * 58,
        f"  Nivel de confianza  : {r['nivel_confianza']}",
    ]

    if "distribucion" in r:
        lineas.append(f"  Distribución        : {r['distribucion']}")
    if "metodo" in r:
        lineas.append(f"  Método              : {r['metodo']}")

    crit_key = "z" if "z" in r else "t_critico"
    crit_label = "Z crítico" if "z" in r else "t crítico"
    lineas.append(f"  {crit_label:<20}: {r[crit_key]}")
    lineas.append(f"  Tamaño muestra (n)  : {r['n']}")

    if tipo == "proporción":
        lineas += [
            f"  Éxitos              : {r['exitos']}",
            f"  p̂                   : {r['p_hat'] * 100:.4f}%",
            f"  Error estándar      : {r['error_estandar']}",
            f"  Margen de error     : ±{r['margen_error'] * 100:.4f}%",
            "",
            "  ┌──────────────────────────────────────────────┐",
            f"  │  IC: [ {r['limite_inferior'] * 100:.4f}%  ,  {r['limite_superior'] * 100:.4f}% ]  │",
            "  └──────────────────────────────────────────────┘",
        ]
    else:
        lineas.append(f"  Media muestral (x̄)  : {r['media_muestral']}")
        if "sigma" in r:
            lineas.append(f"  σ (poblacional)     : {r['sigma']}")
        if "desv_estandar_muestral" in r:
            lineas.append(f"  s (muestral)        : {r['desv_estandar_muestral']}")
        if "grados_libertad" in r:
            lineas.append(f"  Grados de libertad  : {r['grados_libertad']}")
        lineas += [
            f"  Error estándar      : {r['error_estandar']}",
            f"  Margen de error     : ±{r['margen_error']}",
            "",
            "  ┌──────────────────────────────────────────────┐",
            f"  │  IC: [ {r['limite_inferior']:.6f}  ,  {r['limite_superior']:.6f} ]  │",
            "  └──────────────────────────────────────────────┘",
        ]

    if r.get("advertencia"):
        lineas += ["", f"  {r['advertencia']}"]

    lineas.append("=" * 58)
    return "\n".join(lineas)


def _fmt_ic_varianza(r: dict) -> str:
    gl = r["grados_libertad"]
    lineas = [
        "=" * 62,
        "  INTERVALO DE CONFIANZA — VARIANZA POBLACIONAL (χ²)",
        "=" * 62,
        f"  Nivel de confianza       : {r['nivel_confianza']}",
        f"  Distribución             : {r['distribucion']}",
        f"  Tamaño muestra (n)       : {r['n']}",
        f"  Grados de libertad (n-1) : {gl}",
        f"  Desv. estándar muestral s: {r['desv_estandar_muestral']}",
        f"  Varianza muestral (s²)   : {r['varianza_muestral']}",
        "",
        "  ── VALORES CRÍTICOS ──────────────────────────────────",
        f"  χ²(α/2,   {gl}) [cola der.]  : {r['chi2_alpha_2']}",
        f"  χ²(1-α/2, {gl}) [cola izq.] : {r['chi2_1_alpha_2']}",
        "",
        "  ── FÓRMULAS ──────────────────────────────────────────",
        f"  LI(σ²) = (n-1)·s² / χ²(α/2)   = {gl}·{r['varianza_muestral']} / {r['chi2_alpha_2']}",
        f"  LS(σ²) = (n-1)·s² / χ²(1-α/2) = {gl}·{r['varianza_muestral']} / {r['chi2_1_alpha_2']}",
        "",
        "  ┌────────────────────────────────────────────────────────┐",
        f"  │  IC(σ²): [ {r['limite_inferior_varianza']:.6f}  ,  {r['limite_superior_varianza']:.6f} ]  │",
        f"  │  IC(σ) : [ {r['limite_inferior_desv']:.6f}  ,  {r['limite_superior_desv']:.6f} ]  │",
        "  └────────────────────────────────────────────────────────┘",
        "=" * 62,
    ]
    return "\n".join(lineas)


def _fmt_sample_size(r: dict) -> str:
    tipo = r.get("tipo", "")
    lineas = [
        "=" * 58,
        f"  TAMAÑO DE MUESTRA — {tipo.upper()}",
        "=" * 58,
        f"  Nivel de confianza  : {r['nivel_confianza']}",
        f"  Z crítico           : {r['z']}",
        f"  Margen de error (e) : ±{r['margen_error']}",
    ]

    if tipo == "proporción":
        lineas.append(f"  Proporción esperada : {r['proporcion_esperada']}")
    else:
        lineas.append(f"  Desv. estándar (σ)  : {r['desv_estandar']}")

    lineas += [
        "",
        f"  Fórmula: {r['formula']}",
        "",
        f"  n (pobl. infinita)  : {r['n_poblacion_infinita']}",
    ]

    if "poblacion_N" in r:
        lineas += [
            f"  Población N         : {r['poblacion_N']}",
            f"  n ajustada (finita) : {r['n_ajustada_finita']}",
        ]

    if "perdidas_esperadas" in r:
        lineas += [
            "",
            f"  Pérdidas esperadas  : {r['perdidas_esperadas'] * 100:.1f}%",
            f"  Fórmula: nc = n / (1 − pe)",
            f"  n con pérdidas      : {r['n_con_perdidas']}",
        ]

    lineas += [
        "",
        f"  ★ n RECOMENDADA     : {r['n_recomendada']}",
        "=" * 58,
    ]
    return "\n".join(lineas)


def _fmt_ic_prop_directa(r: dict) -> str:
    lineas = [
        "=" * 58,
        "  INTERVALO DE CONFIANZA — PROPORCIÓN (p directo)",
        "=" * 58,
        f"  Nivel de confianza  : {r['nivel_confianza']}",
        f"  Método              : {r['metodo']}",
        f"  Z crítico (Zα/2)    : {r['z']}",
        f"  Tamaño muestra (n)  : {r['n']}",
        f"  Proporción (p)      : {r['p'] * 100:.4f}%",
        f"  q = 1 − p           : {r['q'] * 100:.4f}%",
        f"  p × q               : {r['p_por_q']}",
        f"  p × q / n           : {r['p_por_q_div_n']}",
        f"  Error estándar SE   : {r['error_estandar']}",
        f"  Margen de error E   : ±{r['margen_error'] * 100:.4f}%",
        "",
        "  ┌──────────────────────────────────────────────┐",
        f"  │  IC: [ {r['limite_inferior'] * 100:.4f}%  ,  {r['limite_superior'] * 100:.4f}% ]  │",
        "  └──────────────────────────────────────────────┘",
    ]
    if r.get("advertencia"):
        lineas += ["", f"  {r['advertencia']}"]
    lineas.append("=" * 58)
    return "\n".join(lineas)


def _fmt_ic_dos_medias(r: dict) -> str:
    w = 64
    lineas = [
        "=" * w,
        f"  {r['caso']}",
        "=" * w,
        f"  Nivel de confianza    : {r['nivel_confianza']}",
        f"  Distribución          : {r['distribucion']}",
    ]

    if "z" in r:
        lineas.append(f"  Z crítico (Zα/2)      : {r['z']}")
    if "t_critico" in r:
        lineas.append(f"  t crítico (tα/2, gl)  : {r['t_critico']}")
        gl_key = "grados_libertad" if "grados_libertad" in r else "grados_libertad_welch"
        lineas.append(f"  Grados de libertad    : {r[gl_key]}")

    lineas.append("")

    is_paired = "d_bar" in r
    if is_paired:
        lineas += [
            f"  n (pares)             : {r['n']}",
            f"  d̄ (media diferencias) : {r['d_bar']}",
            f"  Sd (desv. diferencias): {r['sd']}",
        ]
    else:
        sp_a = "sigma1" if "sigma1" in r else "s1"
        sp_b = "sigma2" if "sigma2" in r else "s2"
        lbl_a = "σ₁" if "sigma1" in r else "s₁"
        lbl_b = "σ₂" if "sigma2" in r else "s₂"
        lineas += [
            f"  Muestra A: n₁={r['n1']}, x̄₁={r['x1']}, {lbl_a}={r[sp_a]}",
            f"  Muestra B: n₂={r['n2']}, x̄₂={r['x2']}, {lbl_b}={r[sp_b]}",
        ]

    if "varianza_ponderada_sp2" in r:
        lineas.append(f"  Varianza ponderada sp²: {r['varianza_ponderada_sp2']}")
    if "s1_cuad_div_n1" in r:
        lineas += [
            f"  s₁²/n₁                : {r['s1_cuad_div_n1']}",
            f"  s₂²/n₂                : {r['s2_cuad_div_n2']}",
        ]

    lineas += [
        "",
        f"  Diferencia (x̄₁−x̄₂)   : {r['diferencia_medias']}",
        f"  Error estándar SE     : {r['error_estandar']}",
        f"  Margen de error E     : ±{r['margen_error']}",
        "",
        "  ┌──────────────────────────────────────────────────────┐",
        f"  │  IC: [ {r['limite_inferior']:.6f}  ,  {r['limite_superior']:.6f} ]  │",
        "  └──────────────────────────────────────────────────────┘",
        "",
        f"  ▶ {r['interpretacion']}",
        "=" * w,
    ]
    return "\n".join(lineas)
