import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from views.theme import FONT_SECTION, FONT_NORMAL, FONT_SMALL, FONT_MONO_SM, PAD_S, PAD_M, PAD_L
from views.components import clear_frame, ResultTextWidget, CTkDropdown


class StatisticsPanel:
    """Panel for dispersion and shape measures."""

    def __init__(self, parent, controller):
        self._ctrl = controller

        self._root = ctk.CTkFrame(parent, fg_color="transparent")
        self._root.grid(row=0, column=0, sticky="nsew")
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        self._root.rowconfigure(1, weight=1)
        self._root.columnconfigure(0, weight=1)

        self._toolbar = ctk.CTkFrame(self._root, height=44, fg_color=("gray88", "gray18"),
                                     corner_radius=0)
        self._toolbar.grid(row=0, column=0, sticky="ew")

        self._content = ctk.CTkFrame(self._root, fg_color="transparent")
        self._content.grid(row=1, column=0, sticky="nsew")
        self._content.rowconfigure(0, weight=1)
        self._content.columnconfigure(0, weight=1)

        self._build_toolbar()

    def _build_toolbar(self) -> None:
        CTkDropdown(
            self._toolbar, "Medidas de Dispersión",
            items=[("Calcular Dispersión", self._show_dispersion)],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "Medidas de Forma",
            items=[("Calcular Asimetría y Curtosis", self._show_shape)],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "Resumen Completo",
            items=[("Ver Resumen Estadístico", self._show_full_summary)],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _make_panel(self, title: str):
        """Returns (control_frame, result_widget) inside a fresh CTkFrame."""
        clear_frame(self._content)

        outer = ctk.CTkFrame(self._content, fg_color="transparent")
        outer.grid(row=0, column=0, sticky="nsew")
        outer.rowconfigure(1, weight=1)
        outer.columnconfigure(0, weight=1)

        ctk.CTkLabel(outer, text=title, font=FONT_SECTION, anchor="w").grid(
            row=0, column=0, sticky="w", padx=PAD_L, pady=(PAD_M, 0))

        control = ctk.CTkFrame(outer, fg_color="transparent", height=40)
        control.grid(row=1, column=0, sticky="ew", padx=PAD_M, pady=PAD_S)

        result_frame = ctk.CTkFrame(outer, fg_color="transparent")
        result_frame.grid(row=2, column=0, sticky="nsew")
        result_frame.rowconfigure(0, weight=1)
        result_frame.columnconfigure(0, weight=1)
        outer.rowconfigure(2, weight=1)

        result = ResultTextWidget(result_frame, font=FONT_MONO_SM)
        return control, result

    def _variable_combo(self, parent) -> ctk.CTkComboBox:
        ctk.CTkLabel(parent, text="Variable:", font=FONT_SMALL).pack(side="left", padx=PAD_S)
        combo = ctk.CTkComboBox(parent, values=list(self._ctrl.columns),
                                state="readonly", font=FONT_SMALL, width=200, height=28)
        if self._ctrl.columns:
            combo.set(self._ctrl.columns[0])
        combo.pack(side="left", padx=PAD_S)
        return combo

    # ── Dispersion ────────────────────────────────────────────────────────────

    def _show_dispersion(self) -> None:
        control, result = self._make_panel("Medidas de Dispersión")
        combo = self._variable_combo(control)

        def calcular():
            try:
                m = self._ctrl.get_dispersion_measures(combo.get())
                result.set(_format_dispersion(combo.get(), m))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"),
                      hover_color=("gray60", "gray45"),
                      command=lambda: result.export("dispersion.txt")).pack(side="left", padx=PAD_S)

    # ── Shape ──────────────────────────────────────────────────────────────────

    def _show_shape(self) -> None:
        control, result = self._make_panel("Medidas de Forma")
        combo = self._variable_combo(control)

        def calcular():
            try:
                m = self._ctrl.get_shape_measures(combo.get())
                result.set(_format_shape(combo.get(), m))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"),
                      hover_color=("gray60", "gray45"),
                      command=lambda: result.export("forma.txt")).pack(side="left", padx=PAD_S)

    # ── Full summary ───────────────────────────────────────────────────────────

    def _show_full_summary(self) -> None:
        control, result = self._make_panel("Resumen Estadístico Completo")
        combo = self._variable_combo(control)

        def calcular():
            try:
                m = self._ctrl.get_full_summary(combo.get())
                result.set(_format_full_summary(combo.get(), m))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Generar Resumen", font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_M)
        ctk.CTkButton(control, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray70", "gray35"),
                      hover_color=("gray60", "gray45"),
                      command=lambda: result.export("resumen_estadistico.txt")).pack(side="left", padx=PAD_S)


# ── Formatting helpers (pure functions, no UI) ────────────────────────────────

def _format_dispersion(variable: str, m: dict) -> str:
    lines = [
        "=" * 60,
        "  MEDIDAS DE DISPERSIÓN",
        "=" * 60,
        f"\nVariable: {variable}",
        f"Tamaño de la muestra (n): {m['n']}\n",
        "--- Medidas de Tendencia Central ---",
        f"Media: {m['mean']:.4f}\n",
        "--- Medidas de Dispersión Absoluta ---",
        f"Rango: {m['range']:.4f}",
        f"  Mínimo: {m['min']:.4f}",
        f"  Máximo: {m['max']:.4f}\n",
        f"Rango Intercuartílico (IQR): {m['iqr']:.4f}",
        f"  Q1 (percentil 25): {m['q1']:.4f}",
        f"  Q3 (percentil 75): {m['q3']:.4f}\n",
        "--- Varianza ---",
        f"Varianza Poblacional (σ²): {m['variance_population']:.4f}",
        f"Varianza Muestral (s²):   {m['variance_sample']:.4f}\n",
        "--- Desviación Estándar ---",
        f"Desviación Estándar Poblacional (σ): {m['std_population']:.4f}",
        f"Desviación Estándar Muestral (s):    {m['std_sample']:.4f}\n",
        "--- Medidas de Dispersión Relativa ---",
        f"Coeficiente de Variación (CV): {m['cv']:.2f}%\n",
        "Interpretación del CV:",
    ]
    if m["cv"] < 15:
        lines.append("  → Baja dispersión (datos homogéneos)")
    elif m["cv"] < 30:
        lines.append("  → Dispersión moderada")
    else:
        lines.append("  → Alta dispersión (datos heterogéneos)")
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def _format_shape(variable: str, m: dict) -> str:
    lines = [
        "=" * 60,
        "  MEDIDAS DE FORMA",
        "=" * 60,
        f"\nVariable: {variable}\n",
        "--- ASIMETRÍA (SKEWNESS) ---",
        f"Coeficiente de Asimetría: {m['skewness']:.4f}",
        f"Interpretación: {m['skewness_label']}\n",
    ]
    skew = m["skewness"]
    if skew > 0:
        lines += ["  → La distribución tiene cola más larga a la derecha",
                  "  → La media es mayor que la mediana"]
    elif skew < 0:
        lines += ["  → La distribución tiene cola más larga a la izquierda",
                  "  → La media es menor que la mediana"]
    else:
        lines.append("  → La distribución es simétrica")

    lines += [
        "",
        "--- CURTOSIS (KURTOSIS) ---",
        f"Coeficiente de Curtosis: {m['kurtosis']:.4f}",
        f"Interpretación: {m['kurtosis_label']}\n",
    ]
    kurt = m["kurtosis"]
    if kurt > 0:
        lines += ["  → La distribución es más puntiaguda que la normal",
                  "  → Mayor concentración de datos en el centro"]
    elif kurt < 0:
        lines += ["  → La distribución es más achatada que la normal",
                  "  → Menor concentración de datos en el centro"]
    else:
        lines.append("  → Forma similar a la distribución normal")

    lines += [
        "",
        "NOTA: Curtosis calculada como exceso respecto a la distribución",
        "normal (valor 0 = distribución normal).",
        "\n" + "=" * 60,
    ]
    return "\n".join(lines)


def _format_full_summary(variable: str, m: dict) -> str:
    W = 52
    lines = [
        "╔" + "═" * W + "╗",
        "║" + " RESUMEN ESTADÍSTICO COMPLETO".center(W) + "║",
        "╚" + "═" * W + "╝",
        f"\nVariable: {variable}",
        f"Tamaño de muestra: {m['n']} observaciones\n",
        "┌─ MEDIDAS DE TENDENCIA CENTRAL " + "─" * (W - 31) + "┐",
        f"│ Media:                    {m['mean']:>{W - 28}.4f} │",
        "└" + "─" * W + "┘\n",
        "┌─ MEDIDAS DE DISPERSIÓN " + "─" * (W - 24) + "┐",
        f"│ Rango:                    {m['range']:>{W - 28}.4f} │",
        f"│   Mínimo:                 {m['min']:>{W - 28}.4f} │",
        f"│   Máximo:                 {m['max']:>{W - 28}.4f} │",
        f"│ IQR:                      {m['iqr']:>{W - 28}.4f} │",
        f"│   Q1:                     {m['q1']:>{W - 28}.4f} │",
        f"│   Q3:                     {m['q3']:>{W - 28}.4f} │",
        f"│ Varianza (s²):            {m['variance_sample']:>{W - 28}.4f} │",
        f"│ Desv. Estándar (s):       {m['std_sample']:>{W - 28}.4f} │",
        f"│ Coef. de Variación:       {m['cv']:>{W - 29}.2f}% │",
        "└" + "─" * W + "┘\n",
        "┌─ MEDIDAS DE FORMA " + "─" * (W - 19) + "┐",
        f"│ Asimetría:                {m['skewness']:>{W - 28}.4f} │",
        f"│   → {m['skewness_label']:<{W - 6}} │",
        f"│ Curtosis:                 {m['kurtosis']:>{W - 28}.4f} │",
        f"│   → {m['kurtosis_label']:<{W - 6}} │",
        "└" + "─" * W + "┘",
    ]
    return "\n".join(lines)
