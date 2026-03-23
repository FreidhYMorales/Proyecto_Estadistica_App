import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from views.theme import FONT_SECTION, FONT_NORMAL, FONT_SMALL, FONT_MONO_SM, PAD_S, PAD_M, PAD_L
from views.components import clear_frame, GraphCanvas, ResultTextWidget, CTkDropdown
import utils.regression as reg_utils
import utils.graphs as graph_utils


class RegressionPanel:
    """Panel for correlation and regression analysis."""

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
            self._toolbar, "Correlación",
            items=[("Análisis de Correlación", self._show_correlation)],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "Regresión Simple",
            items=[
                ("Regresión Lineal",    self._show_linear),
                ("Regresión No Lineal", self._show_nonlinear),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "Regresión Múltiple",
            items=[("Regresión Lineal Múltiple", self._show_multiple)],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _clear(self) -> None:
        clear_frame(self._content)
        self._content.rowconfigure(0, weight=0)
        self._content.rowconfigure(1, weight=1)
        self._content.columnconfigure(0, weight=1)

    def _xy_combos(self, parent) -> tuple:
        cols = list(self._ctrl.columns)
        ctk.CTkLabel(parent, text="Variable X:", font=FONT_SMALL).grid(
            row=0, column=0, padx=PAD_S, pady=PAD_S)
        combo_x = ctk.CTkComboBox(parent, values=cols, state="readonly",
                                  font=FONT_SMALL, width=160, height=28)
        if cols:
            combo_x.set(cols[0])
        combo_x.grid(row=0, column=1, padx=PAD_S, pady=PAD_S)

        ctk.CTkLabel(parent, text="Variable Y:", font=FONT_SMALL).grid(
            row=0, column=2, padx=(PAD_M, PAD_S), pady=PAD_S)
        combo_y = ctk.CTkComboBox(parent, values=cols, state="readonly",
                                  font=FONT_SMALL, width=160, height=28)
        if len(cols) > 1:
            combo_y.set(cols[1])
        elif cols:
            combo_y.set(cols[0])
        combo_y.grid(row=0, column=3, padx=PAD_S, pady=PAD_S)
        return combo_x, combo_y

    def _get_paired(self, col_x: str, col_y: str) -> tuple:
        x = self._ctrl.get_numeric_column(col_x)
        y = self._ctrl.get_numeric_column(col_y)
        n = min(len(x), len(y))
        if n < 2:
            raise ValueError("Se necesitan al menos 2 pares de datos numéricos.")
        return x[:n], y[:n]

    # ── Correlation ───────────────────────────────────────────────────────────

    def _show_correlation(self) -> None:
        self._clear()
        ctrl = ctk.CTkFrame(self._content, fg_color="transparent")
        ctrl.grid(row=0, column=0, sticky="ew", padx=PAD_M, pady=PAD_S)
        combo_x, combo_y = self._xy_combos(ctrl)

        result_frame = ctk.CTkFrame(self._content, fg_color="transparent")
        result_frame.grid(row=1, column=0, sticky="nsew")
        result_frame.rowconfigure(0, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_widget = ResultTextWidget(result_frame, font=FONT_MONO_SM)

        def calcular():
            try:
                x, y = self._get_paired(combo_x.get(), combo_y.get())
                pearson  = reg_utils.pearson_correlation(x, y)
                spearman = reg_utils.spearman_correlation(x, y)
                result_widget.set(_format_correlation(
                    combo_x.get(), combo_y.get(), len(x), pearson, spearman))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(ctrl, text="Calcular Correlación", font=FONT_SMALL, height=28,
                      command=calcular).grid(row=0, column=4, padx=PAD_M, pady=PAD_S)
        ctk.CTkButton(ctrl, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray65", "gray35"),
                      command=lambda: result_widget.export("correlacion.txt")).grid(
            row=0, column=5, padx=PAD_S, pady=PAD_S)

    # ── Linear regression ─────────────────────────────────────────────────────

    def _show_linear(self) -> None:
        self._clear()
        ctrl = ctk.CTkFrame(self._content, fg_color="transparent")
        ctrl.grid(row=0, column=0, sticky="ew", padx=PAD_M, pady=PAD_S)
        combo_x, combo_y = self._xy_combos(ctrl)

        main = ctk.CTkFrame(self._content, fg_color="transparent")
        main.grid(row=1, column=0, sticky="nsew", padx=PAD_M, pady=PAD_S)
        main.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)

        # Left: text results
        left = ctk.CTkFrame(main, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, PAD_S))
        left.rowconfigure(0, weight=1)
        left.columnconfigure(0, weight=1)
        result_widget = ResultTextWidget(left, font=FONT_MONO_SM)

        # Right: predictor + graph
        right = ctk.CTkFrame(main, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew")

        pred_card = ctk.CTkFrame(right, corner_radius=8)
        pred_card.pack(fill="x", padx=PAD_S, pady=PAD_S)
        ctk.CTkLabel(pred_card, text="Predicción", font=FONT_SMALL,
                     text_color=("gray40", "gray70")).pack(anchor="w", padx=PAD_M, pady=(PAD_S, 0))

        pred_row = ctk.CTkFrame(pred_card, fg_color="transparent")
        pred_row.pack(fill="x", padx=PAD_M, pady=PAD_S)
        ctk.CTkLabel(pred_row, text="X:", font=FONT_SMALL).pack(side="left")
        pred_x_entry = ctk.CTkEntry(pred_row, width=90, height=26, font=FONT_SMALL)
        pred_x_entry.pack(side="left", padx=PAD_S)

        pred_result_lbl = ctk.CTkLabel(pred_card, text="", font=FONT_SMALL,
                                       text_color=("#d4a017", "#f0c040"))
        pred_result_lbl.pack(padx=PAD_M, pady=(0, PAD_S))

        graph_container = ctk.CTkFrame(right, fg_color="transparent")
        graph_container.pack(fill="both", expand=True, padx=PAD_S, pady=PAD_S)
        graph_container.rowconfigure(0, weight=1)
        graph_container.columnconfigure(0, weight=1)
        canvas_widget = GraphCanvas(graph_container)

        _reg_result: dict = {}

        def calcular():
            try:
                x, y = self._get_paired(combo_x.get(), combo_y.get())
                res = reg_utils.linear_regression(x, y)
                _reg_result.update(res)
                result_widget.set(_format_linear_regression(combo_x.get(), combo_y.get(), res))
                fig, _ = graph_utils.build_regression_plot(
                    x, y, res["y_pred"], res["a"], res["b"], res["r"],
                    combo_x.get(), combo_y.get())
                canvas_widget.render(fig)

                def predecir():
                    try:
                        x_val = float(pred_x_entry.get())
                        y_val = reg_utils.predict_linear(_reg_result["a"], _reg_result["b"], x_val)
                        pred_result_lbl.configure(
                            text=f"Para X = {x_val:.2f}  →  Y = {y_val:.2f}")
                    except ValueError:
                        pred_result_lbl.configure(text="Ingrese un valor numérico válido.")

                # Replace or create the predict button
                for w in pred_row.winfo_children():
                    if isinstance(w, ctk.CTkButton):
                        w.destroy()
                ctk.CTkButton(pred_row, text="Calcular Y", font=FONT_SMALL, height=26,
                              width=80, command=predecir).pack(side="left", padx=PAD_S)

            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(ctrl, text="Calcular Regresión Lineal", font=FONT_SMALL, height=28,
                      command=calcular).grid(row=0, column=4, padx=PAD_M, pady=PAD_S)
        ctk.CTkButton(ctrl, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray65", "gray35"),
                      command=lambda: result_widget.export("regresion_lineal.txt")).grid(
            row=0, column=5, padx=PAD_S, pady=PAD_S)

    # ── Non-linear regression ─────────────────────────────────────────────────

    def _show_nonlinear(self) -> None:
        self._clear()
        ctrl = ctk.CTkFrame(self._content, fg_color="transparent")
        ctrl.grid(row=0, column=0, sticky="ew", padx=PAD_M, pady=PAD_S)
        combo_x, combo_y = self._xy_combos(ctrl)

        ctk.CTkLabel(ctrl, text="Tipo:", font=FONT_SMALL).grid(
            row=0, column=4, padx=(PAD_M, PAD_S), pady=PAD_S)
        tipo_combo = ctk.CTkComboBox(ctrl, values=["Exponencial", "Logarítmica"],
                                     state="readonly", font=FONT_SMALL, width=140, height=28)
        tipo_combo.set("Exponencial")
        tipo_combo.grid(row=0, column=5, padx=PAD_S, pady=PAD_S)

        content = ctk.CTkFrame(self._content, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=PAD_M, pady=PAD_S)
        content.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)

        left = ctk.CTkFrame(content, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, PAD_S))
        left.rowconfigure(0, weight=1)
        left.columnconfigure(0, weight=1)
        result_widget = ResultTextWidget(left, font=FONT_MONO_SM)

        graph_container = ctk.CTkFrame(content, fg_color="transparent")
        graph_container.grid(row=0, column=1, sticky="nsew")
        graph_container.rowconfigure(0, weight=1)
        graph_container.columnconfigure(0, weight=1)
        canvas_widget = GraphCanvas(graph_container)

        def calcular():
            try:
                x, y = self._get_paired(combo_x.get(), combo_y.get())
                tipo = tipo_combo.get()
                if tipo == "Exponencial":
                    res = reg_utils.exponential_regression(x, y)
                else:
                    res = reg_utils.logarithmic_regression(x, y)

                result_widget.set(_format_nonlinear(combo_x.get(), combo_y.get(), tipo, res))

                from matplotlib.figure import Figure
                import math as m
                fig = Figure(figsize=(8, 6), dpi=100)
                ax = fig.add_subplot(111)
                x_sorted = sorted(x)
                if tipo == "Exponencial":
                    y_curve = [res["a"] * m.exp(res["b"] * xi) for xi in x_sorted]
                else:
                    y_curve = [res["a"] + res["b"] * m.log(xi) for xi in x_sorted if xi > 0]
                    x_sorted = [xi for xi in x_sorted if xi > 0]
                ax.scatter(x, y, color="steelblue", alpha=0.7, s=60,
                           edgecolors="white", label="Datos", zorder=3)
                ax.plot(x_sorted, y_curve, color="tomato", linewidth=2.5,
                        label=res["equation"], zorder=2)
                ax.set_xlabel(combo_x.get(), fontsize=11, fontweight="bold")
                ax.set_ylabel(combo_y.get(), fontsize=11, fontweight="bold")
                ax.set_title(f"Regresión {tipo}\nr² = {res['r_squared']:.4f}",
                             fontsize=12, fontweight="bold")
                ax.legend(fontsize=10)
                ax.grid(True, alpha=0.3, linestyle="--")
                canvas_widget.render(fig)

            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(ctrl, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).grid(row=0, column=6, padx=PAD_M, pady=PAD_S)
        ctk.CTkButton(ctrl, text="Exportar", font=FONT_SMALL, height=28,
                      fg_color=("gray65", "gray35"),
                      command=lambda: result_widget.export("regresion_no_lineal.txt")).grid(
            row=0, column=7, padx=PAD_S, pady=PAD_S)

    # ── Multiple regression ───────────────────────────────────────────────────

    def _show_multiple(self) -> None:
        self._clear()
        cols = list(self._ctrl.columns)

        ctrl = ctk.CTkFrame(self._content, fg_color="transparent")
        ctrl.grid(row=0, column=0, sticky="ew", padx=PAD_M, pady=PAD_S)

        ctk.CTkLabel(ctrl, text="Variable Y (dependiente):", font=FONT_SMALL).pack(
            side="left", padx=PAD_S)
        combo_y = ctk.CTkComboBox(ctrl, values=cols, state="readonly",
                                  font=FONT_SMALL, width=180, height=28)
        if cols:
            combo_y.set(cols[0])
        combo_y.pack(side="left", padx=PAD_S)

        content = ctk.CTkFrame(self._content, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=PAD_M, pady=PAD_S)
        content.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=1)

        # Left: X variable selector (CTkScrollableFrame + checkboxes)
        left = ctk.CTkFrame(content, corner_radius=8)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, PAD_S))
        left.rowconfigure(1, weight=1)
        left.columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="Variables X (independientes)",
                     font=FONT_SMALL).grid(
            row=0, column=0, sticky="w", padx=PAD_M, pady=(PAD_M, PAD_S))

        lb_scroll = ctk.CTkScrollableFrame(left, fg_color=("gray80", "gray22"),
                                           corner_radius=4)
        lb_scroll.grid(row=1, column=0, sticky="nsew", padx=PAD_M, pady=PAD_S)

        check_vars: dict[str, ctk.BooleanVar] = {}
        for col in cols:
            var = ctk.BooleanVar()
            check_vars[col] = var
            ctk.CTkCheckBox(lb_scroll, text=col, variable=var,
                            font=FONT_SMALL, height=24).pack(anchor="w")

        # Right: results
        right = ctk.CTkFrame(content, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew")
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)
        result_widget = ResultTextWidget(right, font=FONT_MONO_SM)

        def calcular():
            try:
                vars_x = [c for c, v in check_vars.items() if v.get()]
                if not vars_x:
                    messagebox.showwarning(
                        "Advertencia", "Selecciona al menos una variable independiente.")
                    return
                y_data = self._ctrl.get_numeric_column(combo_y.get())
                if not y_data:
                    raise ValueError(f"No hay datos numéricos en '{combo_y.get()}'.")
                x_lists = []
                for var in vars_x:
                    cd = self._ctrl.get_numeric_column(var)
                    if not cd:
                        raise ValueError(f"No hay datos numéricos en '{var}'.")
                    x_lists.append(cd)

                min_len = min(len(y_data), *(len(x) for x in x_lists))
                if min_len < len(vars_x) + 2:
                    raise ValueError(f"Se necesitan al menos {len(vars_x) + 2} observaciones.")

                res = reg_utils.multiple_regression(
                    [x[:min_len] for x in x_lists], y_data[:min_len], vars_x)
                result_widget.set(_format_multiple(combo_y.get(), vars_x, res))
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(left, text="Calcular Regresión Múltiple", font=FONT_SMALL, height=28,
                      command=calcular).grid(
            row=2, column=0, sticky="ew", padx=PAD_M, pady=PAD_S)
        ctk.CTkButton(left, text="Exportar resultados", font=FONT_SMALL, height=28,
                      fg_color=("gray65", "gray35"),
                      command=lambda: result_widget.export("regresion_multiple.txt")).grid(
            row=3, column=0, sticky="ew", padx=PAD_M, pady=(0, PAD_M))


# ── Formatting helpers ────────────────────────────────────────────────────────

def _format_correlation(x_name: str, y_name: str, n: int, pearson: dict, spearman: dict) -> str:
    r, r2, p = pearson["r"], pearson["r_squared"], pearson["p_value"]
    rho, p_s = spearman["rho"], spearman["p_value"]

    def strength(v):
        v = abs(v)
        return "fuerte" if v >= 0.7 else "moderada" if v >= 0.3 else "débil"

    return "\n".join([
        "=" * 70,
        "  ANÁLISIS DE CORRELACIÓN",
        "=" * 70,
        f"\nVariable X: {x_name}",
        f"Variable Y: {y_name}",
        f"Número de pares: {n}\n",
        "--- CORRELACIÓN DE PEARSON (lineal) ---",
        f"Coeficiente r:         {r:.6f}",
        f"Coeficiente r²:        {r2:.6f}",
        f"Valor p:               {p:.6f}",
        f"Fuerza:                Correlación {strength(r)}",
        f"Dirección:             {'Positiva (directa)' if r > 0 else 'Negativa (inversa)'}",
        f"Significancia:         {'Sí (p < 0.05)' if p < 0.05 else 'No (p ≥ 0.05)'}",
        f"r² → {r2 * 100:.2f}% de variabilidad de Y explicada por X.\n",
        "--- CORRELACIÓN DE SPEARMAN (rangos) ---",
        f"Coeficiente ρ:         {rho:.6f}",
        f"Valor p:               {p_s:.6f}",
        f"Fuerza:                Correlación {strength(rho)}",
        "\nNOTAS:",
        "• Pearson mide relaciones lineales.",
        "• Spearman mide relaciones monótonas (lineales o no).",
        "• Si |Spearman| > |Pearson|: relación probablemente no lineal.",
        "\n" + "=" * 70,
    ])


def _format_linear_regression(x_name: str, y_name: str, res: dict) -> str:
    n = res["n"]
    lines = [
        "=" * 95,
        " " * 25 + "REGRESIÓN LINEAL SIMPLE",
        "=" * 95,
        f"\nVariable X: {x_name}",
        f"Variable Y: {y_name}\n",
        "TABLA DE DATOS:",
        "-" * 95,
        f"{'No':>4s} {'X':>10s} {'Y':>10s} {'dx':>12s} {'dy':>12s} "
        f"{'dx²':>12s} {'dy²':>14s} {'dx*dy':>14s}",
        "-" * 95,
    ]
    for i in range(n):
        lines.append(
            f"{i + 1:4d} {res['x'][i]:10.2f} {res['y'][i]:10.2f} "
            f"{res['dx'][i]:12.4f} {res['dy'][i]:12.4f} {res['dx2'][i]:12.4f} "
            f"{res['dy2'][i]:14.4f} {res['dxdy'][i]:14.4f}"
        )
    lines += [
        "-" * 95,
        f"{'Σ':>4s} {res['sum_x']:10.2f} {res['sum_y']:10.2f} {'':12s} {'':12s} "
        f"{res['sum_dx2']:12.4f} {res['sum_dy2']:14.4f} {res['sum_dxdy']:14.4f}",
        "=" * 95,
        "\nESTADÍSTICOS BÁSICOS:",
        "-" * 50,
        f"  n = {n}",
        f"  X̄ = {res['x_mean']:.6f}",
        f"  Ȳ = {res['y_mean']:.6f}",
        f"  Sx = {res['sx']:.6f}",
        f"  Sy = {res['sy']:.6f}",
        f"  Sxy = {res['sxy']:.6f}",
        "-" * 50,
        "\nCOEFICIENTE DE CORRELACIÓN:",
        f"  r = {res['r']:.6f}",
        f"  {'Alta' if abs(res['r']) >= 0.7 else 'Media' if abs(res['r']) > 0.4 else 'Baja'} correlación",
        f"  {'Positiva (directa)' if res['r'] > 0 else 'Negativa (inversa)'}",
        "\nCOEFICIENTES DE REGRESIÓN:",
        f"  b (pendiente)  = {res['b']:.6f}",
        f"  a (intercepto) = {res['a']:.6f}",
        "\nECUACIÓN:",
        f"  Y = {res['a']:.2f} {'+ ' if res['b'] >= 0 else '- '}{abs(res['b']):.2f}X",
        "\nBONDAD DE AJUSTE:",
        f"  R² = {res['r_squared']:.6f}",
        f"  RMSE = {res['rmse']:.6f}",
        "=" * 95,
    ]
    return "\n".join(lines)


def _format_nonlinear(x_name: str, y_name: str, tipo: str, res: dict) -> str:
    return "\n".join([
        "=" * 60,
        f"  REGRESIÓN {tipo.upper()}",
        "=" * 60,
        f"\nVariable X: {x_name}",
        f"Variable Y: {y_name}\n",
        f"Ecuación: {res['equation']}",
        f"r (correlación linealizada): {res['r']:.6f}",
        f"R² = {res['r_squared']:.6f}",
        f"\nEl modelo explica {res['r_squared'] * 100:.2f}% de la variabilidad en Y.",
        "\n" + "=" * 60,
    ])


def _format_multiple(y_name: str, var_names: list, res: dict) -> str:
    equation = f"Y = {res['intercept']:.6f}"
    for var, beta in res["betas"].items():
        sign = "+ " if beta >= 0 else ""
        equation += f" {sign}{beta:.6f}*{var}"

    interp_lines = [
        f"  • {var}: Por c/unidad que aumenta, Y "
        f"{'aumenta' if b > 0 else 'disminuye'} {abs(b):.4f} unidades."
        for var, b in res["betas"].items()
    ]
    lines = [
        "=" * 70,
        "  REGRESIÓN LINEAL MÚLTIPLE",
        "=" * 70,
        f"\nVariable dependiente: {y_name}",
        f"Variables independientes: {', '.join(var_names)}",
        f"Observaciones: {res['n']}   Variables: {res['k']}\n",
        "ECUACIÓN:",
        f"  {equation}\n",
        "COEFICIENTES:",
        f"  Intercepto (β₀): {res['intercept']:.6f}",
    ]
    for i, (var, beta) in enumerate(res["betas"].items()):
        lines.append(f"  β{i + 1} ({var}): {beta:.6f}")
    lines += [
        "\nBONDAD DE AJUSTE:",
        f"  R²:          {res['r_squared']:.6f}",
        f"  R² ajustado: {res['r_squared_adj']:.6f}",
        f"  RMSE:        {res['rmse']:.6f}",
        f"  MSE:         {res['mse']:.6f}",
        f"\nEl modelo explica {res['r_squared'] * 100:.2f}% de la variabilidad en {y_name}.\n",
        "INTERPRETACIÓN:",
        *interp_lines,
        "\n" + "=" * 70,
    ]
    return "\n".join(lines)
