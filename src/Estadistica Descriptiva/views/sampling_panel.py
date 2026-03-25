"""
Panel de Muestreo Probabilístico.

Ofrece tres métodos de selección de muestra desde los datos cargados en la app:
  - Muestreo Aleatorio Simple (MAS)
  - Muestreo Sistemático
  - Muestreo Estratificado (proporcional u óptimo)

Los resultados se muestran en texto; el estratificado además renderiza
un gráfico de barras N_h vs n_h.
"""
from tkinter import messagebox
import customtkinter as ctk

from views.theme import FONT_SECTION, FONT_SMALL, PAD_XS, PAD_S, PAD_M, PAD_L
from views.components import clear_frame, CTkDropdown, ResultTextWidget, GraphCanvas


class SamplingPanel:
    """Panel registrado en ContentStack bajo la clave 'sampling'."""

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
        # ── Probabilístico ────────────────────────────────────────────────────
        CTkDropdown(
            self._toolbar, "Aleatorio Simple",
            items=[("Seleccionar muestra aleatoria", self._show_simple)],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "Sistemático",
            items=[("Seleccionar muestra sistemática", self._show_systematic)],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "Estratificado",
            items=[
                ("Asignación proporcional", lambda: self._show_stratified("proporcional")),
                ("Asignación simple",       lambda: self._show_stratified("simple")),
                ("Asignación óptima (Neyman)", lambda: self._show_stratified("optima")),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "Conglomerados",
            items=[("Seleccionar conglomerados", self._show_conglomerados)],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        # Separador visual
        ctk.CTkFrame(self._toolbar, width=1, fg_color=("gray70", "gray40")).pack(
            side="left", fill="y", padx=PAD_S, pady=PAD_XS)

        # ── No Probabilístico ─────────────────────────────────────────────────
        CTkDropdown(
            self._toolbar, "No Probabilístico",
            items=[
                ("Por Conveniencia",    self._show_conveniencia),
                ("Por Juicio",          self._show_juicio),
                ("Por Cuotas",          self._show_cuotas),
                ("Bola de Nieve",       self._show_bola_de_nieve),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        # Separador visual
        ctk.CTkFrame(self._toolbar, width=1, fg_color=("gray70", "gray40")).pack(
            side="left", fill="y", padx=PAD_S, pady=PAD_XS)

        # ── Errores ───────────────────────────────────────────────────────────
        CTkDropdown(
            self._toolbar, "Errores de Muestreo",
            items=[
                ("Error para Media (desde datos)", self._show_error_media),
                ("Error para Proporción",           self._show_error_prop),
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

        control = ctk.CTkFrame(self._content, fg_color="transparent", height=44)
        control.grid(row=1, column=0, sticky="ew", padx=PAD_M, pady=PAD_S)

        result_frame = ctk.CTkFrame(self._content, fg_color="transparent")
        result_frame.grid(row=2, column=0, sticky="nsew")
        result_frame.rowconfigure(0, weight=1)
        result_frame.columnconfigure(0, weight=1)

        result = ResultTextWidget(result_frame, font=("Courier", 11))
        return control, result

    def _make_graph_panel(self, titulo: str):
        """Retorna (control_frame, result_widget, graph_canvas)."""
        clear_frame(self._content)
        self._content.rowconfigure(0, weight=0)
        self._content.rowconfigure(1, weight=0)
        self._content.rowconfigure(2, weight=1)
        self._content.rowconfigure(3, weight=2)

        ctk.CTkLabel(self._content, text=titulo, font=FONT_SECTION, anchor="w").grid(
            row=0, column=0, sticky="w", padx=PAD_L, pady=(PAD_M, 0)
        )

        control = ctk.CTkFrame(self._content, fg_color="transparent", height=52)
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

    def _col_combo(self, parent, label: str = "Columna:") -> ctk.CTkComboBox:
        ctk.CTkLabel(parent, text=label, font=FONT_SMALL).pack(side="left", padx=PAD_S)
        combo = ctk.CTkComboBox(
            parent, values=list(self._ctrl.columns),
            state="readonly", font=FONT_SMALL, width=150, height=28,
        )
        if self._ctrl.columns:
            combo.set(self._ctrl.columns[0])
        combo.pack(side="left", padx=PAD_S)
        return combo

    def _n_entry(self, parent, default: str = "10") -> ctk.CTkEntry:
        ctk.CTkLabel(parent, text="n (muestra):", font=FONT_SMALL).pack(side="left", padx=PAD_S)
        entry = ctk.CTkEntry(parent, width=70, height=28, font=FONT_SMALL)
        entry.insert(0, default)
        entry.pack(side="left", padx=PAD_S)
        return entry

    # ── Aleatorio Simple ──────────────────────────────────────────────────────

    def _show_simple(self) -> None:
        control, result = self._make_text_panel("Muestreo Aleatorio Simple")

        combo = self._col_combo(control)
        n_entry = self._n_entry(control)

        reemplazo_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            control, text="Con reemplazo", variable=reemplazo_var,
            font=FONT_SMALL, width=28, height=28,
        ).pack(side="left", padx=(PAD_M, PAD_S))

        def ejecutar():
            try:
                n = int(n_entry.get())
                datos = self._ctrl.get_numeric_column(combo.get())
                if not datos:
                    messagebox.showerror("Error", "No hay datos numéricos en esa columna.")
                    return
                res = self._ctrl.sampling_simple(combo.get(), n, reemplazo_var.get())
                result.set(_fmt_simple(res))
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Ejecutar", font=FONT_SMALL, height=28,
                      command=ejecutar).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
                      command=lambda: result.export("muestreo_simple.txt")).pack(
            side="left", padx=PAD_S)

    # ── Sistemático ───────────────────────────────────────────────────────────

    def _show_systematic(self) -> None:
        control, result = self._make_text_panel("Muestreo Sistemático")

        combo = self._col_combo(control)
        n_entry = self._n_entry(control)

        def ejecutar():
            try:
                n = int(n_entry.get())
                datos = self._ctrl.get_numeric_column(combo.get())
                if not datos:
                    messagebox.showerror("Error", "No hay datos numéricos en esa columna.")
                    return
                res = self._ctrl.sampling_systematic(combo.get(), n)
                result.set(_fmt_systematic(res))
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Ejecutar", font=FONT_SMALL, height=28,
                      command=ejecutar).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
                      command=lambda: result.export("muestreo_sistematico.txt")).pack(
            side="left", padx=PAD_S)

    # ── Estratificado ─────────────────────────────────────────────────────────

    def _show_stratified(self, tipo: str) -> None:
        _titulos = {
            "proporcional": "Muestreo Estratificado — Asignación Proporcional",
            "simple":       "Muestreo Estratificado — Asignación Simple",
            "optima":       "Muestreo Estratificado — Asignación Óptima (Neyman)",
        }
        titulo = _titulos.get(tipo, "Muestreo Estratificado")
        control, result, graph = self._make_graph_panel(titulo)

        # Row 0: strata column + n
        r0 = ctk.CTkFrame(control, fg_color="transparent")
        r0.pack(fill="x")

        strata_combo = self._col_combo(r0, "Estrato:")
        n_entry = self._n_entry(r0)

        # Row 1: variable column (for Neyman) or empty
        r1 = ctk.CTkFrame(control, fg_color="transparent")
        r1.pack(fill="x", pady=(PAD_XS, 0))

        var_combo = None
        if tipo == "optima":  # noqa: E501  (solo Neyman necesita variable de interés)
            ctk.CTkLabel(r1, text="Variable de interés:", font=FONT_SMALL).pack(
                side="left", padx=PAD_S)
            var_combo = ctk.CTkComboBox(
                r1, values=list(self._ctrl.columns),
                state="readonly", font=FONT_SMALL, width=150, height=28,
            )
            if self._ctrl.columns:
                var_combo.set(self._ctrl.columns[0])
            var_combo.pack(side="left", padx=PAD_S)

        def ejecutar():
            try:
                n = int(n_entry.get())
                col_var = var_combo.get() if var_combo else None
                res = self._ctrl.sampling_stratified(
                    strata_combo.get(), n, tipo, col_var
                )
                result.set(_fmt_stratified(res))
                # Render bar chart
                import utils.inference_graphs as ig
                fig, _ = ig.build_stratified_bars(
                    res["tabla_asignacion"], titulo
                )
                graph.render(fig)
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(r1, text="Ejecutar", font=FONT_SMALL, height=28,
                      command=ejecutar).pack(side="left", padx=PAD_M)
        ctk.CTkButton(r1, text="Exportar tabla", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
                      command=lambda: result.export("muestreo_estratificado.txt")).pack(
            side="left", padx=PAD_S)

    # ── Conveniencia ──────────────────────────────────────────────────────────

    def _show_conveniencia(self) -> None:
        control, result = self._make_text_panel("Muestreo por Conveniencia")

        combo = self._col_combo(control)
        n_entry = self._n_entry(control)

        ctk.CTkLabel(control, text="Índice inicio:", font=FONT_SMALL).pack(
            side="left", padx=(PAD_M, PAD_S))
        inicio_entry = ctk.CTkEntry(control, width=60, height=28, font=FONT_SMALL)
        inicio_entry.insert(0, "0")
        inicio_entry.pack(side="left", padx=PAD_S)

        def ejecutar():
            try:
                n = int(n_entry.get())
                inicio = int(inicio_entry.get())
                res = self._ctrl.sampling_conveniencia(combo.get(), n, inicio)
                result.set(_fmt_no_prob(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Ejecutar", font=FONT_SMALL, height=28,
                      command=ejecutar).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
                      command=lambda: result.export("muestreo_conveniencia.txt")).pack(
            side="left", padx=PAD_S)

    # ── Juicio ────────────────────────────────────────────────────────────────

    def _show_juicio(self) -> None:
        control, result = self._make_text_panel("Muestreo por Juicio (Intencional)")

        # Row 0
        r0 = ctk.CTkFrame(control, fg_color="transparent")
        r0.pack(fill="x")

        combo = self._col_combo(r0)

        ctk.CTkLabel(r0, text="Índices (ej: 0,3,7,12):", font=FONT_SMALL).pack(
            side="left", padx=(PAD_M, PAD_S))
        idx_entry = ctk.CTkEntry(r0, width=200, height=28, font=FONT_SMALL,
                                 placeholder_text="0,3,7,12,25")
        idx_entry.pack(side="left", padx=PAD_S)

        # Row 1 — criterio
        r1 = ctk.CTkFrame(control, fg_color="transparent")
        r1.pack(fill="x", pady=(PAD_XS, 0))

        ctk.CTkLabel(r1, text="Criterio de selección:", font=FONT_SMALL).pack(
            side="left", padx=PAD_S)
        criterio_entry = ctk.CTkEntry(r1, width=300, height=28, font=FONT_SMALL,
                                      placeholder_text="Ej: Mayores ingresos del sector norte")
        criterio_entry.pack(side="left", padx=PAD_S)

        def ejecutar():
            try:
                raw = idx_entry.get().strip()
                if not raw:
                    messagebox.showerror("Error", "Ingresa al menos un índice.")
                    return
                indices = [int(x.strip()) for x in raw.split(",") if x.strip()]
                res = self._ctrl.sampling_juicio(
                    combo.get(), indices, criterio_entry.get().strip()
                )
                result.set(_fmt_no_prob(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(r1, text="Ejecutar", font=FONT_SMALL, height=28,
                      command=ejecutar).pack(side="left", padx=PAD_M)
        ctk.CTkButton(r1, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
                      command=lambda: result.export("muestreo_juicio.txt")).pack(
            side="left", padx=PAD_S)

    # ── Cuotas ────────────────────────────────────────────────────────────────

    def _show_cuotas(self) -> None:
        control, result, graph = self._make_graph_panel("Muestreo por Cuotas")

        r0 = ctk.CTkFrame(control, fg_color="transparent")
        r0.pack(fill="x")

        strata_combo = self._col_combo(r0, "Estrato:")
        n_entry = self._n_entry(r0)

        r1 = ctk.CTkFrame(control, fg_color="transparent")
        r1.pack(fill="x", pady=(PAD_XS, 0))

        ctk.CTkLabel(r1, text="Cuotas manuales (opcional, ej: A:10,B:15):",
                     font=FONT_SMALL).pack(side="left", padx=PAD_S)
        cuotas_entry = ctk.CTkEntry(r1, width=220, height=28, font=FONT_SMALL,
                                    placeholder_text="Vacío = distribución proporcional")
        cuotas_entry.pack(side="left", padx=PAD_S)

        def ejecutar():
            try:
                n = int(n_entry.get())
                raw_cuotas = cuotas_entry.get().strip()
                cuotas_dict = None
                if raw_cuotas:
                    cuotas_dict = {}
                    for par in raw_cuotas.split(","):
                        if ":" in par:
                            k, v = par.split(":", 1)
                            cuotas_dict[k.strip()] = int(v.strip())
                res = self._ctrl.sampling_cuotas(
                    strata_combo.get(),
                    cuotas=cuotas_dict,
                    n_total=None if cuotas_dict else n,
                )
                result.set(_fmt_cuotas(res))
                import utils.inference_graphs as ig
                fig, _ = ig.build_stratified_bars(
                    res["tabla_cuotas"].rename(columns={
                        "N_h (pobl.)": "N_h (pobl.)",
                        "n_h (obtenidos)": "n_h (muestra)",
                    }),
                    "Muestreo por Cuotas"
                )
                graph.render(fig)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(r1, text="Ejecutar", font=FONT_SMALL, height=28,
                      command=ejecutar).pack(side="left", padx=PAD_M)
        ctk.CTkButton(r1, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
                      command=lambda: result.export("muestreo_cuotas.txt")).pack(
            side="left", padx=PAD_S)

    # ── Bola de Nieve ─────────────────────────────────────────────────────────

    def _show_bola_de_nieve(self) -> None:
        control, result = self._make_text_panel("Muestreo Bola de Nieve")

        r0 = ctk.CTkFrame(control, fg_color="transparent")
        r0.pack(fill="x")

        combo = self._col_combo(r0)

        ctk.CTkLabel(r0, text="Semillas (índices, ej: 0,1,2):", font=FONT_SMALL).pack(
            side="left", padx=(PAD_M, PAD_S))
        semillas_entry = ctk.CTkEntry(r0, width=160, height=28, font=FONT_SMALL,
                                      placeholder_text="0,1,2")
        semillas_entry.pack(side="left", padx=PAD_S)

        r1 = ctk.CTkFrame(control, fg_color="transparent")
        r1.pack(fill="x", pady=(PAD_XS, 0))

        ctk.CTkLabel(r1, text="Ondas:", font=FONT_SMALL).pack(side="left", padx=PAD_S)
        ondas_entry = ctk.CTkEntry(r1, width=50, height=28, font=FONT_SMALL)
        ondas_entry.insert(0, "3")
        ondas_entry.pack(side="left", padx=PAD_S)

        ctk.CTkLabel(r1, text="Referidos/onda:", font=FONT_SMALL).pack(
            side="left", padx=(PAD_M, PAD_S))
        refs_entry = ctk.CTkEntry(r1, width=50, height=28, font=FONT_SMALL)
        refs_entry.insert(0, "2")
        refs_entry.pack(side="left", padx=PAD_S)

        def ejecutar():
            try:
                raw = semillas_entry.get().strip()
                if not raw:
                    messagebox.showerror("Error", "Ingresa al menos un índice semilla.")
                    return
                semillas = [int(x.strip()) for x in raw.split(",") if x.strip()]
                res = self._ctrl.sampling_bola_de_nieve(
                    combo.get(), semillas,
                    int(ondas_entry.get()), int(refs_entry.get())
                )
                result.set(_fmt_bola_de_nieve(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(r1, text="Ejecutar", font=FONT_SMALL, height=28,
                      command=ejecutar).pack(side="left", padx=PAD_M)
        ctk.CTkButton(r1, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
                      command=lambda: result.export("muestreo_bola_nieve.txt")).pack(
            side="left", padx=PAD_S)

    # ── Conglomerados ─────────────────────────────────────────────────────────

    def _show_conglomerados(self) -> None:
        control, result, graph = self._make_graph_panel("Muestreo por Conglomerados")

        r0 = ctk.CTkFrame(control, fg_color="transparent")
        r0.pack(fill="x")

        cluster_combo = self._col_combo(r0, "Conglomerado:")

        ctk.CTkLabel(r0, text="k (grupos a seleccionar):", font=FONT_SMALL).pack(
            side="left", padx=(PAD_M, PAD_S))
        k_entry = ctk.CTkEntry(r0, width=60, height=28, font=FONT_SMALL)
        k_entry.insert(0, "2")
        k_entry.pack(side="left", padx=PAD_S)

        def ejecutar():
            try:
                k = int(k_entry.get())
                res = self._ctrl.sampling_conglomerados(cluster_combo.get(), k)
                result.set(_fmt_conglomerados(res))
                import utils.inference_graphs as ig
                fig, _ = ig.build_stratified_bars(
                    res["tabla_conglomerados"].rename(columns={
                        "Elementos (n_c)": "n_h (muestra)",
                        "Conglomerado": "Estrato",
                    }).assign(**{"N_h (pobl.)": res["tabla_conglomerados"]["Elementos (n_c)"]}),
                    "Conglomerados Seleccionados — Elementos"
                )
                graph.render(fig)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(r0, text="Ejecutar", font=FONT_SMALL, height=28,
                      command=ejecutar).pack(side="left", padx=PAD_M)
        ctk.CTkButton(r0, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
                      command=lambda: result.export("muestreo_conglomerados.txt")).pack(
            side="left", padx=PAD_S)

    # ── Errores de Muestreo — Media ────────────────────────────────────────────

    def _show_error_media(self) -> None:
        control, result = self._make_text_panel("Errores de Muestreo — Media")

        r0 = ctk.CTkFrame(control, fg_color="transparent")
        r0.pack(fill="x")

        combo = self._col_combo(r0)

        ctk.CTkLabel(r0, text="Confianza:", font=FONT_SMALL).pack(
            side="left", padx=(PAD_M, PAD_S))
        nc_combo = ctk.CTkComboBox(r0, values=["90%", "95%", "99%"],
                                   state="readonly", font=FONT_SMALL, width=70, height=28)
        nc_combo.set("95%")
        nc_combo.pack(side="left", padx=PAD_S)

        r1 = ctk.CTkFrame(control, fg_color="transparent")
        r1.pack(fill="x", pady=(PAD_XS, 0))

        ctk.CTkLabel(r1, text="N pobl. (opcional):", font=FONT_SMALL).pack(
            side="left", padx=PAD_S)
        N_entry = ctk.CTkEntry(r1, width=90, height=28, font=FONT_SMALL,
                               placeholder_text="vacío = ∞")
        N_entry.pack(side="left", padx=PAD_S)

        ctk.CTkLabel(r1, text="μ real (opcional):", font=FONT_SMALL).pack(
            side="left", padx=(PAD_M, PAD_S))
        mu_entry = ctk.CTkEntry(r1, width=90, height=28, font=FONT_SMALL,
                                placeholder_text="vacío = desconocida")
        mu_entry.pack(side="left", padx=PAD_S)

        _NC = {"90%": 0.90, "95%": 0.95, "99%": 0.99}

        def ejecutar():
            try:
                nc = _NC[nc_combo.get()]
                N_txt = N_entry.get().strip()
                mu_txt = mu_entry.get().strip()
                N = int(N_txt) if N_txt else None
                mu = float(mu_txt) if mu_txt else None
                res = self._ctrl.errores_media(combo.get(), nc, N, mu)
                result.set(_fmt_errores(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(r1, text="Calcular", font=FONT_SMALL, height=28,
                      command=ejecutar).pack(side="left", padx=PAD_M)
        ctk.CTkButton(r1, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
                      command=lambda: result.export("errores_media.txt")).pack(
            side="left", padx=PAD_S)

    # ── Errores de Muestreo — Proporción ───────────────────────────────────────

    def _show_error_prop(self) -> None:
        control, result = self._make_text_panel("Errores de Muestreo — Proporción")

        r0 = ctk.CTkFrame(control, fg_color="transparent")
        r0.pack(fill="x")

        ctk.CTkLabel(r0, text="Éxitos:", font=FONT_SMALL).pack(side="left", padx=PAD_S)
        exitos_e = ctk.CTkEntry(r0, width=70, height=28, font=FONT_SMALL)
        exitos_e.insert(0, "50")
        exitos_e.pack(side="left", padx=PAD_S)

        ctk.CTkLabel(r0, text="n:", font=FONT_SMALL).pack(side="left", padx=(PAD_M, PAD_S))
        n_e = ctk.CTkEntry(r0, width=70, height=28, font=FONT_SMALL)
        n_e.insert(0, "100")
        n_e.pack(side="left", padx=PAD_S)

        ctk.CTkLabel(r0, text="Confianza:", font=FONT_SMALL).pack(
            side="left", padx=(PAD_M, PAD_S))
        nc_combo = ctk.CTkComboBox(r0, values=["90%", "95%", "99%"],
                                   state="readonly", font=FONT_SMALL, width=70, height=28)
        nc_combo.set("95%")
        nc_combo.pack(side="left", padx=PAD_S)

        r1 = ctk.CTkFrame(control, fg_color="transparent")
        r1.pack(fill="x", pady=(PAD_XS, 0))

        ctk.CTkLabel(r1, text="N pobl. (opcional):", font=FONT_SMALL).pack(
            side="left", padx=PAD_S)
        N_entry = ctk.CTkEntry(r1, width=90, height=28, font=FONT_SMALL,
                               placeholder_text="vacío = ∞")
        N_entry.pack(side="left", padx=PAD_S)

        ctk.CTkLabel(r1, text="p real (opcional):", font=FONT_SMALL).pack(
            side="left", padx=(PAD_M, PAD_S))
        p_entry = ctk.CTkEntry(r1, width=90, height=28, font=FONT_SMALL,
                               placeholder_text="0.0 – 1.0")
        p_entry.pack(side="left", padx=PAD_S)

        _NC = {"90%": 0.90, "95%": 0.95, "99%": 0.99}

        def ejecutar():
            try:
                nc = _NC[nc_combo.get()]
                N_txt = N_entry.get().strip()
                p_txt = p_entry.get().strip()
                N = int(N_txt) if N_txt else None
                p_real = float(p_txt) if p_txt else None
                res = self._ctrl.errores_proporcion(
                    int(exitos_e.get()), int(n_e.get()), nc, N, p_real
                )
                result.set(_fmt_errores(res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(r1, text="Calcular", font=FONT_SMALL, height=28,
                      command=ejecutar).pack(side="left", padx=PAD_M)
        ctk.CTkButton(r1, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"), hover_color=("gray60", "gray45"),
                      command=lambda: result.export("errores_proporcion.txt")).pack(
            side="left", padx=PAD_S)


# ── Formatting helpers ────────────────────────────────────────────────────────

def _fmt_simple(r: dict) -> str:
    muestra = r["muestra"]
    if hasattr(muestra, "__len__"):
        primeros = list(muestra[:10]) if not hasattr(muestra, "iloc") else muestra.head(10).to_string()
    else:
        primeros = str(muestra)

    idx = r["indices_seleccionados"]
    lines = [
        "=" * 58,
        "  MUESTREO ALEATORIO SIMPLE",
        "=" * 58,
        f"  Población (N)         : {r['N']}",
        f"  Muestra (n)           : {r['n']}",
        f"  Con reemplazo         : {r['con_reemplazo']}",
        f"  P(selección)          : {r['probabilidad_seleccion']:.4f}",
        "",
        f"  Índices seleccionados ({len(idx)}):",
        f"  {idx[:15]}{'...' if len(idx) > 15 else ''}",
        "",
        "  Muestra (primeros 10 elementos):",
    ]
    if hasattr(r["muestra"], "iloc"):
        lines.append(r["muestra"].head(10).to_string())
    else:
        lines.append(f"  {list(r['muestra'][:10])}")
    lines.append("=" * 58)
    return "\n".join(lines)


def _fmt_systematic(r: dict) -> str:
    idx = r["indices_seleccionados"]
    lines = [
        "=" * 58,
        "  MUESTREO SISTEMÁTICO",
        "=" * 58,
        f"  Población (N)         : {r['N']}",
        f"  Muestra (n)           : {r['n']}",
        f"  Intervalo (K)         : {r['intervalo_K']}",
        f"  Punto de inicio       : {r['punto_inicio']}",
        "",
        f"  Índices seleccionados ({len(idx)}):",
        f"  {idx[:15]}{'...' if len(idx) > 15 else ''}",
        "",
        "  Muestra (primeros 10 elementos):",
    ]
    if hasattr(r["muestra"], "iloc"):
        lines.append(r["muestra"].head(10).to_string())
    else:
        lines.append(f"  {list(r['muestra'][:10])}")
    lines.append("=" * 58)
    return "\n".join(lines)


def _fmt_stratified(r: dict) -> str:
    lines = [
        "=" * 58,
        "  MUESTREO ESTRATIFICADO",
        "=" * 58,
        f"  Población (N)         : {r['N']}",
        f"  Muestra total (n)     : {r['n_total']}",
        f"  Asignación            : {r['tipo_asignacion']}",
        f"  Número de estratos    : {r['num_estratos']}",
        "",
        "  TABLA DE ASIGNACIÓN:",
    ]
    lines.append(r["tabla_asignacion"].to_string(index=False))
    lines += [
        "",
        "  MUESTRA (primeras filas):",
        r["muestra"].head(10).to_string(),
        "=" * 58,
    ]
    return "\n".join(lines)


def _fmt_no_prob(r: dict) -> str:
    """Formateador genérico para conveniencia y juicio."""
    idx = r["indices_seleccionados"]
    lines = [
        "=" * 58,
        f"  MUESTREO {r['metodo'].upper()}",
        f"  Tipo: {r['tipo']}",
        "=" * 58,
        f"  Población (N)         : {r['N']}",
        f"  Muestra (n)           : {r['n']}",
    ]
    if "inicio" in r:
        lines.append(f"  Índice de inicio      : {r['inicio']}")
    if "criterio_aplicado" in r:
        lines.append(f"  Criterio aplicado     : {r['criterio_aplicado']}")

    lines += [
        "",
        f"  Índices seleccionados ({len(idx)}):",
        f"  {idx[:15]}{'...' if len(idx) > 15 else ''}",
        "",
        "  Muestra (primeros 10 elementos):",
    ]
    muestra = r["muestra"]
    if hasattr(muestra, "iloc"):
        lines.append(muestra.head(10).to_string())
    else:
        lines.append(f"  {list(muestra[:10])}")

    lines += ["", f"  {r['advertencia']}", "=" * 58]
    return "\n".join(lines)


def _fmt_cuotas(r: dict) -> str:
    lines = [
        "=" * 58,
        "  MUESTREO POR CUOTAS",
        "  Tipo: No probabilístico",
        "=" * 58,
        f"  Población (N)         : {r['N']}",
        f"  Muestra total (n)     : {r['n_total']}",
        f"  Número de estratos    : {r['num_estratos']}",
        "",
        "  TABLA DE CUOTAS:",
    ]
    lines.append(r["tabla_cuotas"].to_string(index=False))
    lines += [
        "",
        "  MUESTRA (primeras filas):",
        r["muestra"].head(10).to_string(),
        "",
        f"  {r['advertencia']}",
        "=" * 58,
    ]
    return "\n".join(lines)


def _fmt_bola_de_nieve(r: dict) -> str:
    lines = [
        "=" * 58,
        "  MUESTREO BOLA DE NIEVE",
        "  Tipo: No probabilístico",
        "=" * 58,
        f"  Población (N)              : {r['N']}",
        f"  Muestra total (n)          : {r['n_total']}",
        f"  Ondas realizadas           : {r['n_ondas_reales']}",
        f"  Referidos por onda (máx)   : {r['refs_por_onda']}",
        "",
        "  PROGRESIÓN POR OLA:",
    ]
    lines.append(r["tabla_ondas"].to_string(index=False))

    idx = r["indices_seleccionados"]
    lines += [
        "",
        f"  Todos los índices seleccionados ({len(idx)}):",
        f"  {idx[:20]}{'...' if len(idx) > 20 else ''}",
        "",
        "  Muestra (primeros 10 elementos):",
    ]
    muestra = r["muestra"]
    if hasattr(muestra, "iloc"):
        lines.append(muestra.head(10).to_string())
    else:
        lines.append(f"  {list(muestra[:10])}")

    lines += ["", f"  {r['advertencia']}", "=" * 58]
    return "\n".join(lines)


def _fmt_conglomerados(r: dict) -> str:
    selec = r["conglomerados_seleccionados"]
    lines = [
        "=" * 58,
        "  MUESTREO POR CONGLOMERADOS",
        "=" * 58,
        f"  Población (N)              : {r['N']}",
        f"  Total conglomerados (K)    : {r['K_total']}",
        f"  Conglomerados seleccionados: {r['k_seleccionados']}",
        f"  Muestra total (n)          : {r['n_total']}",
        "",
        f"  Conglomerados elegidos: {selec}",
        "",
        "  TABLA DE CONGLOMERADOS:",
    ]
    lines.append(r["tabla_conglomerados"].to_string(index=False))
    lines += [
        "",
        "  MUESTRA (primeras filas):",
        r["muestra"].head(10).to_string(),
        "=" * 58,
    ]
    return "\n".join(lines)


def _fmt_errores(r: dict) -> str:
    tipo = r["tipo"]
    lines = [
        "=" * 60,
        f"  ERRORES DE MUESTREO — {tipo.upper()}",
        "=" * 60,
        f"  Nivel de confianza         : {r['nivel_confianza']}",
        f"  Z crítico                  : {r['z']}",
        f"  Tamaño de muestra (n)      : {r['n']}",
    ]

    if r.get("N_poblacional"):
        lines.append(f"  Tamaño poblacional (N)     : {r['N_poblacional']}")

    if tipo == "media":
        lines += [
            f"  Media muestral (x̄)         : {r['media_muestral']}",
            f"  Desv. estándar muestral (s) : {r['desv_estandar_muestral']}",
        ]
    else:
        lines += [
            f"  Éxitos                     : {r['exitos']}",
            f"  p̂                          : {r['p_hat']}",
            f"  q̂                          : {r['q_hat']}",
        ]

    lines += [
        "",
        "  ── ERROR ESTÁNDAR ──────────────────────────────────",
        f"  SE = {'s/√n' if tipo == 'media' else '√(p̂·q̂/n)'}",
        f"  SE                         : {r['error_estandar']}",
    ]

    if r.get("fpc") is not None:
        lines += [
            f"  FPC = √(1 − n/N)           : {r['fpc']}",
            f"  SE corregido (× FPC)       : {r['error_estandar_corregido']}",
        ]

    lines += [
        "",
        "  ── MARGEN DE ERROR Y ERROR RELATIVO ────────────────",
        f"  Margen de error (ME = Z·SE): ±{r['margen_error']}",
    ]

    if r.get("error_relativo_pct") is not None:
        lines.append(f"  Error relativo (ME/θ·100)  : {r['error_relativo_pct']:.4f}%")

    if r.get("error_real") is not None:
        ref = r.get("mu_real") or r.get("p_real")
        lines += [
            "",
            "  ── ERROR VERDADERO (valor real conocido) ───────────",
            f"  Valor real (μ o p)         : {ref}",
            f"  Error = |θ̂ − θ|            : {r['error_real']}",
        ]

    lines += [
        "",
        "  ── INTERVALO DE CONFIANZA ──────────────────────────",
        f"  IC: [{r['limite_inferior']:.6f} , {r['limite_superior']:.6f}]",
    ]

    if tipo == "proporción" and not r.get("condicion_normal_valida", True):
        lines.append("  ⚠ n·p̂ o n·q̂ < 5: aproximación normal puede no ser válida.")

    lines += [
        "",
        "  ── CLASIFICACIÓN DE ERRORES DE MUESTREO ────────────",
        "  Tipo                  Descripción                  Reducible con n",
        "  ─────────────────────────────────────────────────────────────────",
        "  Aleatorio (muestreo)  Variabilidad por selección   Sí (↑n → ↓SE)",
        "  Sistemático (sesgo)   Defecto en diseño/marco      No",
        "  No respuesta          Unidades que no responden    Parcialmente",
        "  Cobertura             Marco no cubre la población  No",
        "  Medición              Instrumento impreciso        No",
        "=" * 60,
    ]
    return "\n".join(lines)
