import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def build_histogram(data: list, bins: int, variable_name: str) -> tuple:
    fig = Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.hist(data, bins=bins, color="skyblue", edgecolor="black", alpha=0.7)
    ax.set_xlabel("Valores", fontsize=12)
    ax.set_ylabel("Frecuencia", fontsize=12)
    ax.set_title(f"Histograma de {variable_name}", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    return fig, ax


def build_frequency_polygon(data: list, bins: int, variable_name: str) -> tuple:
    hist, bin_edges = np.histogram(data, bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    fig = Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(bin_centers, hist, marker="o", color="blue", linewidth=2, markersize=8)
    ax.fill_between(bin_centers, hist, alpha=0.3, color="skyblue")
    ax.set_xlabel("Valores", fontsize=12)
    ax.set_ylabel("Frecuencia", fontsize=12)
    ax.set_title(f"Polígono de Frecuencia de {variable_name}", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    return fig, ax


def build_ogive(data: list, ascending: bool, variable_name: str) -> tuple:
    sorted_data = np.sort(data)
    n = len(sorted_data)
    y_values = np.arange(1, n + 1) / n * 100 if ascending else np.arange(n, 0, -1) / n * 100
    title = (
        f"Ojiva Ascendente (Menor que) - {variable_name}"
        if ascending
        else f"Ojiva Descendente (Mayor que) - {variable_name}"
    )

    fig = Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(sorted_data, y_values, marker="o", color="green", linewidth=2, markersize=6)
    ax.set_xlabel("Valores", fontsize=12)
    ax.set_ylabel("Frecuencia Acumulada (%)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    return fig, ax


def build_bar_chart(data: list, variable_name: str) -> tuple:
    freq = pd.Series(data).value_counts().sort_index()

    fig = Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    x = range(len(freq))
    ax.bar(x, freq.values, color="coral", edgecolor="black", alpha=0.7)
    ax.set_xticks(list(x))
    ax.set_xticklabels(freq.index, rotation=45, ha="right")
    ax.set_xlabel("Categorías", fontsize=12)
    ax.set_ylabel("Frecuencia", fontsize=12)
    ax.set_title(f"Gráfico de Barras - {variable_name}", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    return fig, ax


def build_pie_chart(data: list, max_categories: int, variable_name: str) -> tuple:
    freq = pd.Series(data).value_counts()
    if len(freq) > max_categories:
        others = freq.iloc[max_categories:].sum()
        freq = freq.head(max_categories).copy()
        if others > 0:
            freq["Otros"] = others

    fig = Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    colors = plt.cm.Set3(range(len(freq)))
    wedges, texts, autotexts = ax.pie(
        freq.values, labels=freq.index, autopct="%1.1f%%",
        colors=colors, startangle=90,
    )
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")
        autotext.set_fontsize(9)
    ax.set_title(f"Gráfico Circular - {variable_name}", fontsize=14, fontweight="bold")
    return fig, ax


def build_boxplot(data_groups: list, labels: list) -> tuple:
    fig = Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    bp = ax.boxplot(data_groups, labels=labels, patch_artist=True, showmeans=True, meanline=True)
    for patch in bp["boxes"]:
        patch.set_facecolor("lightblue")
        patch.set_alpha(0.7)
    for median in bp["medians"]:
        median.set_color("red")
        median.set_linewidth(2)
    for mean in bp["means"]:
        mean.set_color("green")
        mean.set_linewidth(2)
    ax.set_xlabel("Variables", fontsize=12)
    ax.set_ylabel("Valores", fontsize=12)
    ax.set_title("Diagrama de Caja", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    return fig, ax


def build_scatter(x: list, y: list, x_name: str, y_name: str) -> tuple:
    fig = Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.scatter(x, y, color="purple", alpha=0.6, s=50, edgecolors="black")
    ax.set_xlabel(x_name, fontsize=12)
    ax.set_ylabel(y_name, fontsize=12)
    ax.set_title(f"Diagrama de Dispersión: {x_name} vs {y_name}", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    return fig, ax


def build_regression_plot(
    x: list, y: list, y_pred: list,
    a: float, b: float, r: float,
    x_name: str, y_name: str,
) -> tuple:
    fig = Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)
    ax.scatter(x, y, color="blue", alpha=0.6, s=60, edgecolors="black",
               linewidth=1.5, label="Datos observados", zorder=3)
    ax.plot(x, y_pred, color="red", linewidth=2.5,
            label=f"Y = {a:.2f} + {b:.2f}X", zorder=2)
    ax.set_xlabel(x_name, fontsize=12, fontweight="bold")
    ax.set_ylabel(y_name, fontsize=12, fontweight="bold")
    ax.set_title(f"Regresión Lineal Simple\nr = {r:.4f}", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3, linestyle="--")
    return fig, ax
