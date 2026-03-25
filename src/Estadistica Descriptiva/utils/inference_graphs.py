"""
Módulo: inference_graphs.py
Gráficos para intervalos de confianza y muestreo estratificado.
Todas las funciones devuelven (fig, ax) usando matplotlib.figure.Figure
para integración con el panel GUI (FigureCanvasTkAgg).
"""
import numpy as np
from scipy import stats
from matplotlib.figure import Figure

_COLORES = {
    "azul":    "#2196F3",
    "verde":   "#4CAF50",
    "rojo":    "#F44336",
    "naranja": "#FF9800",
    "fondo":   "#1e1e2e",
}


def build_ic_plot(
    estimacion: float,
    limite_inf: float,
    limite_sup: float,
    nombre_parametro: str = "Parámetro",
    nivel_confianza: str = "95%",
    titulo: str = "Intervalo de Confianza",
) -> tuple:
    """Error bar mostrando estimación central y límites del IC."""
    fig = Figure(figsize=(8, 3), dpi=100, facecolor=_COLORES["fondo"])
    ax = fig.add_subplot(111, facecolor=_COLORES["fondo"])

    ax.errorbar(
        x=estimacion, y=1,
        xerr=[[estimacion - limite_inf], [limite_sup - estimacion]],
        fmt="o", color=_COLORES["azul"],
        ecolor=_COLORES["naranja"],
        elinewidth=3, capsize=10, capthick=2, markersize=10,
        label=f"Estimación = {estimacion:.4f}",
    )
    ax.text(limite_inf, 1.15, f"LI={limite_inf:.4f}", ha="center", fontsize=8, color="white")
    ax.text(limite_sup, 1.15, f"LS={limite_sup:.4f}", ha="center", fontsize=8, color="white")
    ax.text(estimacion, 0.82, f"{estimacion:.4f}", ha="center", fontsize=8,
            color=_COLORES["azul"], fontweight="bold")

    ax.set_ylim(0.5, 1.5)
    ax.set_yticks([])
    ax.set_xlabel(nombre_parametro, fontsize=10, color="white")
    ax.set_title(f"{titulo} — Confianza {nivel_confianza}", fontsize=11,
                 fontweight="bold", color="white")
    ax.legend(fontsize=8, labelcolor="white",
              facecolor=_COLORES["fondo"], edgecolor="gray")
    ax.tick_params(colors="white")
    for sp in ["top", "right", "left"]:
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("gray")
    fig.tight_layout()
    return fig, ax


def build_normal_dist_ic(
    media: float,
    error_estandar: float,
    z_critico: float,
    nivel_confianza: str = "95%",
    titulo: str = "Distribución Normal — Región de Confianza",
) -> tuple:
    """Distribución muestral con región de confianza sombreada."""
    li = media - z_critico * error_estandar
    ls = media + z_critico * error_estandar
    x = np.linspace(media - 4 * error_estandar, media + 4 * error_estandar, 400)
    y = stats.norm.pdf(x, loc=media, scale=error_estandar)

    fig = Figure(figsize=(8, 4.5), dpi=100, facecolor=_COLORES["fondo"])
    ax = fig.add_subplot(111, facecolor=_COLORES["fondo"])

    ax.plot(x, y, color=_COLORES["azul"], linewidth=2.5, label="Dist. muestral")

    x_ic = np.linspace(li, ls, 300)
    y_ic = stats.norm.pdf(x_ic, loc=media, scale=error_estandar)
    ax.fill_between(x_ic, y_ic, alpha=0.35, color=_COLORES["verde"],
                    label=f"IC {nivel_confianza}")

    ax.axvline(media, color=_COLORES["azul"], linestyle="--", linewidth=1.5,
               label=f"Media = {media:.4f}")
    ax.axvline(li, color=_COLORES["naranja"], linestyle=":", linewidth=1.5,
               label=f"LI = {li:.4f}")
    ax.axvline(ls, color=_COLORES["rojo"], linestyle=":", linewidth=1.5,
               label=f"LS = {ls:.4f}")

    ax.set_xlabel("Valor del parámetro", fontsize=10, color="white")
    ax.set_ylabel("Densidad", fontsize=10, color="white")
    ax.set_title(titulo, fontsize=11, fontweight="bold", color="white")
    ax.legend(fontsize=8, labelcolor="white",
              facecolor=_COLORES["fondo"], edgecolor="gray")
    ax.tick_params(colors="white")
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("gray")
    ax.spines["left"].set_color("gray")
    fig.tight_layout()
    return fig, ax


def build_stratified_bars(tabla_asignacion, titulo: str = "Muestreo Estratificado") -> tuple:
    """Barras comparando N_h (población) vs n_h (muestra) por estrato."""
    estratos = tabla_asignacion["Estrato"].astype(str).tolist()
    N_h = tabla_asignacion["N_h (pobl.)"].tolist()
    n_h = tabla_asignacion["n_h (muestra)"].tolist()

    x = np.arange(len(estratos))
    ancho = 0.35

    fig = Figure(figsize=(9, 4.5), dpi=100, facecolor=_COLORES["fondo"])
    ax = fig.add_subplot(111, facecolor=_COLORES["fondo"])

    barras_N = ax.bar(x - ancho / 2, N_h, ancho, label="Población (N_h)",
                      color=_COLORES["azul"], alpha=0.85)
    barras_n = ax.bar(x + ancho / 2, n_h, ancho, label="Muestra (n_h)",
                      color=_COLORES["verde"], alpha=0.85)

    for barra in barras_N:
        ax.text(barra.get_x() + barra.get_width() / 2, barra.get_height() + 0.5,
                str(int(barra.get_height())), ha="center", va="bottom",
                fontsize=8, color="white")
    for barra in barras_n:
        ax.text(barra.get_x() + barra.get_width() / 2, barra.get_height() + 0.5,
                str(int(barra.get_height())), ha="center", va="bottom",
                fontsize=8, color="white")

    ax.set_xticks(x)
    ax.set_xticklabels(estratos, rotation=30, ha="right", color="white")
    ax.set_xlabel("Estrato", fontsize=10, color="white")
    ax.set_ylabel("Cantidad", fontsize=10, color="white")
    ax.set_title(titulo, fontsize=11, fontweight="bold", color="white")
    ax.legend(fontsize=9, labelcolor="white",
              facecolor=_COLORES["fondo"], edgecolor="gray")
    ax.tick_params(colors="white")
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("gray")
    ax.spines["left"].set_color("gray")
    fig.tight_layout()
    return fig, ax


def build_compare_ic(
    media: float,
    error_estandar: float,
    titulo: str = "Comparación de Intervalos de Confianza",
) -> tuple:
    """Muestra IC al 90%, 95% y 99% en un mismo gráfico."""
    niveles = {
        "90%": (stats.norm.ppf(0.95), _COLORES["verde"]),
        "95%": (stats.norm.ppf(0.975), _COLORES["azul"]),
        "99%": (stats.norm.ppf(0.995), _COLORES["rojo"]),
    }

    fig = Figure(figsize=(8, 3.5), dpi=100, facecolor=_COLORES["fondo"])
    ax = fig.add_subplot(111, facecolor=_COLORES["fondo"])

    for i, (nivel, (z, color)) in enumerate(niveles.items()):
        margen = z * error_estandar
        li = media - margen
        ls = media + margen
        y_pos = i + 1
        ax.errorbar(
            x=media, y=y_pos,
            xerr=[[margen], [margen]],
            fmt="o", color=color, ecolor=color,
            elinewidth=3, capsize=8, capthick=2, markersize=8,
            label=f"IC {nivel}: [{li:.4f}, {ls:.4f}]",
        )

    ax.axvline(media, color="white", linestyle="--", linewidth=1, alpha=0.5)
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(list(niveles.keys()), fontsize=10, color="white")
    ax.set_xlabel("Valor del parámetro", fontsize=10, color="white")
    ax.set_title(titulo, fontsize=11, fontweight="bold", color="white")
    ax.legend(fontsize=8, labelcolor="white",
              facecolor=_COLORES["fondo"], edgecolor="gray")
    ax.tick_params(colors="white")
    for sp in ["top", "right", "left"]:
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("gray")
    fig.tight_layout()
    return fig, ax
