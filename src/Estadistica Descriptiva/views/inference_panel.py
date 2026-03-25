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

from views.theme import FONT_SECTION, FONT_SMALL, PAD_S, PAD_M, PAD_L
from views.components import clear_frame, CTkDropdown, ResultTextWidget, GraphCanvas


# Opciones de nivel de confianza
_NC_OPTIONS = ["90%", "95%", "99%"]
_NC_MAP = {"90%": 0.90, "95%": 0.95, "99%": 0.99}


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
            self._root, height=44, fg_color=("gray88", "gray18"), corner_radius=0
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
            items=[("Calcular IC para Proporción", self._show_ic_prop)],
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
            self._toolbar, "Tamaño de Muestra",
            items=[
                ("Para proporción", self._show_ss_prop),
                ("Para media", self._show_ss_media),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

    # ── Layout helpers ────────────────────────────────────────────────────────

    def _make_text_panel(self, titulo: str):
        """Retorna (control_frame, ResultTextWidget)."""
        clear_frame(self._content)
        self._content.rowconfigure(0, weight=0)
        self._content.rowconfigure(1, weight=0)
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

    def _nc_combo(self, parent) -> ctk.CTkComboBox:
        ctk.CTkLabel(parent, text="Confianza:", font=FONT_SMALL).pack(side="left", padx=PAD_S)
        combo = ctk.CTkComboBox(
            parent, values=_NC_OPTIONS,
            state="readonly", font=FONT_SMALL, width=80, height=28,
        )
        combo.set("95%")
        combo.pack(side="left", padx=PAD_S)
        return combo

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
                nc = _NC_MAP[nc_combo.get()]
                metodo = "wilson" if "wilson" in met_combo.get() else "normal"
                res = self._ctrl.ic_proporcion(int(exitos_e.get()), int(n_e.get()), nc, metodo)
                result.set(_fmt_ic(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
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
                nc = _NC_MAP[nc_combo.get()]
                res = self._ctrl.ic_media_z(
                    float(media_e.get()), float(sigma_e.get()), int(n_e.get()), nc
                )
                result.set(_fmt_ic(res))
                # Gráfico de distribución
                import utils.inference_graphs as ig
                fig, _ = ig.build_normal_dist_ic(
                    res["media_muestral"], res["error_estandar"],
                    res["z"], nc_combo.get(),
                    "Distribución Normal — IC para Media"
                )
                graph.render(fig)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
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
                nc = _NC_MAP[nc_combo.get()]
                datos = self._ctrl.get_numeric_column(col_combo.get())
                if not datos:
                    messagebox.showerror("Error", "No hay datos numéricos en esa columna.")
                    return
                res = self._ctrl.ic_media_t_datos(datos, nc)
                result.set(_fmt_ic(res))
                import utils.inference_graphs as ig
                fig, _ = ig.build_normal_dist_ic(
                    res["media_muestral"], res["error_estandar"],
                    res["t_critico"], nc_combo.get(),
                    f"Distribución t-Student — IC para Media ({col_combo.get()})"
                )
                graph.render(fig)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
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
                nc = _NC_MAP[nc_combo.get()]
                res = self._ctrl.ic_media_t_manual(
                    float(media_e.get()), float(s_e.get()), int(n_e.get()), nc
                )
                result.set(_fmt_ic(res))
                import utils.inference_graphs as ig
                fig, _ = ig.build_normal_dist_ic(
                    res["media_muestral"], res["error_estandar"],
                    res["t_critico"], nc_combo.get(),
                    "Distribución t-Student — IC para Media"
                )
                graph.render(fig)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
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
                nc = _NC_MAP[nc_combo.get()]
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
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
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
                nc = _NC_MAP[nc_combo.get()]
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
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
                      command=lambda: result.export("ic_varianza_manual.txt")).pack(
            side="left", padx=PAD_S)

    # ── Tamaño de muestra — Proporción ────────────────────────────────────────

    def _show_ss_prop(self) -> None:
        control, result = self._make_text_panel("Tamaño de Muestra — Para Proporción")

        nc_combo = self._nc_combo(control)
        e_entry = self._labeled_entry(control, "Margen error (e):", "0.05")
        p_entry = self._labeled_entry(control, "p esperada:", "0.5")
        n_entry = self._labeled_entry(control, "N pobl. (opcional):", "", width=110)
        pe_entry = self._labeled_entry(control, "% pérdidas (0-1):", "", width=80)

        def calcular():
            try:
                nc = _NC_MAP[nc_combo.get()]
                N_txt = n_entry.get().strip()
                pe_txt = pe_entry.get().strip()
                poblacion = int(N_txt) if N_txt else None
                perdidas = float(pe_txt) if pe_txt else None
                res = self._ctrl.sample_size_proportion(
                    float(e_entry.get()), float(p_entry.get()), nc, poblacion, perdidas
                )
                result.set(_fmt_sample_size(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
                      command=lambda: result.export("tamano_muestra_prop.txt")).pack(
            side="left", padx=PAD_S)

    # ── Tamaño de muestra — Media ─────────────────────────────────────────────

    def _show_ss_media(self) -> None:
        control, result = self._make_text_panel("Tamaño de Muestra — Para Media")

        nc_combo = self._nc_combo(control)
        e_entry = self._labeled_entry(control, "Margen error (e):", "5")
        s_entry = self._labeled_entry(control, "σ (desv. estándar):", "15")
        n_entry = self._labeled_entry(control, "N pobl. (opcional):", "", width=110)
        pe_entry = self._labeled_entry(control, "% pérdidas (0-1):", "", width=80)

        def calcular():
            try:
                nc = _NC_MAP[nc_combo.get()]
                N_txt = n_entry.get().strip()
                pe_txt = pe_entry.get().strip()
                poblacion = int(N_txt) if N_txt else None
                perdidas = float(pe_txt) if pe_txt else None
                res = self._ctrl.sample_size_mean(
                    float(e_entry.get()), float(s_entry.get()), nc, poblacion, perdidas
                )
                result.set(_fmt_sample_size(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
                      command=lambda: result.export("tamano_muestra_media.txt")).pack(
            side="left", padx=PAD_S)


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
            f"  p̂                   : {r['p_hat']}",
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
