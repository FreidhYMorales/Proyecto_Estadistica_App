import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

from views.theme import FONT_SMALL, PAD_S, PAD_M
from views.components import clear_frame, GraphCanvas, CTkDropdown
import utils.graphs as graph_utils


class GraphsPanel:
    """Panel for all statistical graphs."""

    def __init__(self, parent: ctk.CTkFrame, controller):
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
        self._content.rowconfigure(1, weight=1)
        self._content.columnconfigure(0, weight=1)

        self._build_toolbar()

    def _build_toolbar(self) -> None:
        CTkDropdown(
            self._toolbar, "Gráficos de Frecuencia",
            items=[
                ("Histograma",            self._show_histogram),
                ("Polígono de Frecuencia", self._show_polygon),
                ("Ojiva",                 self._show_ogive),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "Gráficos Categóricos",
            items=[
                ("Gráfico de Barras",    self._show_bar_chart),
                ("Gráfico Circular",     self._show_pie_chart),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "Gráficos Comparativos",
            items=[
                ("Diagrama de Caja",      self._show_boxplot),
                ("Diagrama de Dispersión", self._show_scatter),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

    # ── Layout helpers ────────────────────────────────────────────────────────

    def _make_panel(self):
        """Returns a fresh control frame; sets up graph container below it."""
        clear_frame(self._content)
        self._content.rowconfigure(0, weight=0)
        self._content.rowconfigure(1, weight=1)

        control = ctk.CTkFrame(self._content, fg_color="transparent", height=44)
        control.grid(row=0, column=0, sticky="ew", padx=PAD_M, pady=PAD_S)
        return control

    def _column_combo(self, parent, label: str = "Variable:") -> ctk.CTkComboBox:
        ctk.CTkLabel(parent, text=label, font=FONT_SMALL).pack(side="left", padx=PAD_S)
        combo = ctk.CTkComboBox(parent, values=list(self._ctrl.columns),
                                state="readonly", font=FONT_SMALL, width=180, height=28)
        if self._ctrl.columns:
            combo.set(self._ctrl.columns[0])
        combo.pack(side="left", padx=PAD_S)
        return combo

    def _graph_container(self) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self._content, fg_color="transparent")
        frame.grid(row=1, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        return frame

    # ── Frequency charts ──────────────────────────────────────────────────────

    def _show_histogram(self) -> None:
        control = self._make_panel()
        combo = self._column_combo(control)

        ctk.CTkLabel(control, text="Bins:", font=FONT_SMALL).pack(side="left", padx=(PAD_M, PAD_S))
        bins_entry = ctk.CTkEntry(control, width=60, height=28, font=FONT_SMALL)
        bins_entry.insert(0, "10")
        bins_entry.pack(side="left", padx=PAD_S)

        canvas_widget = GraphCanvas(self._graph_container())

        def generar():
            try:
                data = self._ctrl.get_numeric_column(combo.get())
                if not data:
                    messagebox.showerror("Error", "No hay datos numéricos disponibles.")
                    return
                fig, _ = graph_utils.build_histogram(data, int(bins_entry.get()), combo.get())
                canvas_widget.render(fig)
            except ValueError:
                messagebox.showerror("Error", "Número de bins inválido.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Generar Histograma", font=FONT_SMALL, height=28,
                      command=generar).pack(side="left", padx=PAD_M)

    def _show_polygon(self) -> None:
        control = self._make_panel()
        combo = self._column_combo(control)

        ctk.CTkLabel(control, text="Bins:", font=FONT_SMALL).pack(side="left", padx=(PAD_M, PAD_S))
        bins_entry = ctk.CTkEntry(control, width=60, height=28, font=FONT_SMALL)
        bins_entry.insert(0, "10")
        bins_entry.pack(side="left", padx=PAD_S)

        canvas_widget = GraphCanvas(self._graph_container())

        def generar():
            try:
                data = self._ctrl.get_numeric_column(combo.get())
                if not data:
                    messagebox.showerror("Error", "No hay datos numéricos disponibles.")
                    return
                fig, _ = graph_utils.build_frequency_polygon(
                    data, int(bins_entry.get()), combo.get())
                canvas_widget.render(fig)
            except ValueError:
                messagebox.showerror("Error", "Número de bins inválido.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Generar Polígono", font=FONT_SMALL, height=28,
                      command=generar).pack(side="left", padx=PAD_M)

    def _show_ogive(self) -> None:
        control = self._make_panel()
        combo = self._column_combo(control)

        ctk.CTkLabel(control, text="Tipo:", font=FONT_SMALL).pack(side="left", padx=(PAD_M, PAD_S))
        tipo_combo = ctk.CTkComboBox(control, values=["Ascendente", "Descendente"],
                                     state="readonly", font=FONT_SMALL, width=140, height=28)
        tipo_combo.set("Ascendente")
        tipo_combo.pack(side="left", padx=PAD_S)

        canvas_widget = GraphCanvas(self._graph_container())

        def generar():
            try:
                data = self._ctrl.get_numeric_column(combo.get())
                if not data:
                    messagebox.showerror("Error", "No hay datos numéricos disponibles.")
                    return
                fig, _ = graph_utils.build_ogive(
                    data, tipo_combo.get() == "Ascendente", combo.get())
                canvas_widget.render(fig)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Generar Ojiva", font=FONT_SMALL, height=28,
                      command=generar).pack(side="left", padx=PAD_M)

    # ── Categorical charts ────────────────────────────────────────────────────

    def _show_bar_chart(self) -> None:
        control = self._make_panel()
        combo = self._column_combo(control)
        canvas_widget = GraphCanvas(self._graph_container())

        def generar():
            try:
                data = self._ctrl.get_column(combo.get())
                if not data:
                    messagebox.showerror("Error", "No hay datos disponibles.")
                    return
                if len(set(data)) > 50:
                    messagebox.showwarning(
                        "Advertencia",
                        "Demasiadas categorías (>50). El gráfico puede no ser legible.")
                fig, _ = graph_utils.build_bar_chart(data, combo.get())
                canvas_widget.render(fig)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Generar Gráfico de Barras", font=FONT_SMALL, height=28,
                      command=generar).pack(side="left", padx=PAD_M)

    def _show_pie_chart(self) -> None:
        control = self._make_panel()
        combo = self._column_combo(control)

        ctk.CTkLabel(control, text="Máx. categorías:", font=FONT_SMALL).pack(side="left", padx=(PAD_M, PAD_S))
        max_entry = ctk.CTkEntry(control, width=60, height=28, font=FONT_SMALL)
        max_entry.insert(0, "10")
        max_entry.pack(side="left", padx=PAD_S)

        canvas_widget = GraphCanvas(self._graph_container())

        def generar():
            try:
                data = self._ctrl.get_column(combo.get())
                if not data:
                    messagebox.showerror("Error", "No hay datos disponibles.")
                    return
                fig, _ = graph_utils.build_pie_chart(data, int(max_entry.get()), combo.get())
                canvas_widget.render(fig)
            except ValueError:
                messagebox.showerror("Error", "Número máximo de categorías inválido.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Generar Gráfico Circular", font=FONT_SMALL, height=28,
                      command=generar).pack(side="left", padx=PAD_M)

    # ── Comparative charts ────────────────────────────────────────────────────

    def _show_boxplot(self) -> None:
        control = self._make_panel()
        ctk.CTkLabel(control, text="Variable(s):", font=FONT_SMALL).pack(
            side="left", padx=PAD_S)

        # CTkScrollableFrame as multi-select listbox replacement
        lb_wrap = ctk.CTkScrollableFrame(control, width=200, height=80,
                                         fg_color=("gray80", "gray25"), corner_radius=4)
        lb_wrap.pack(side="left", padx=PAD_S)

        check_vars: dict[str, ctk.BooleanVar] = {}
        for col in self._ctrl.columns:
            var = ctk.BooleanVar()
            check_vars[col] = var
            ctk.CTkCheckBox(lb_wrap, text=col, variable=var, font=FONT_SMALL,
                            height=22).pack(anchor="w")

        canvas_widget = GraphCanvas(self._graph_container())

        def generar():
            try:
                selected = [c for c, v in check_vars.items() if v.get()]
                if not selected:
                    messagebox.showwarning("Advertencia", "Selecciona al menos una variable.")
                    return
                groups, labels = [], []
                for var in selected:
                    data = self._ctrl.get_numeric_column(var)
                    if data:
                        groups.append(data)
                        labels.append(var)
                if not groups:
                    messagebox.showerror("Error", "No hay datos numéricos disponibles.")
                    return
                fig, _ = graph_utils.build_boxplot(groups, labels)
                canvas_widget.render(fig)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Generar Diagrama de Caja", font=FONT_SMALL, height=28,
                      command=generar).pack(side="left", padx=PAD_M)

    def _show_scatter(self) -> None:
        control = self._make_panel()
        combo_x = self._column_combo(control, "Variable X:")
        combo_y = self._column_combo(control, "Variable Y:")
        if len(self._ctrl.columns) > 1:
            combo_y.set(self._ctrl.columns[1])

        canvas_widget = GraphCanvas(self._graph_container())

        def generar():
            try:
                x_data = self._ctrl.get_numeric_column(combo_x.get())
                y_data = self._ctrl.get_numeric_column(combo_y.get())
                if not x_data or not y_data:
                    messagebox.showerror("Error", "No hay datos numéricos disponibles.")
                    return
                n = min(len(x_data), len(y_data))
                fig, _ = graph_utils.build_scatter(
                    x_data[:n], y_data[:n], combo_x.get(), combo_y.get())
                canvas_widget.render(fig)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(control, text="Generar Diagrama", font=FONT_SMALL, height=28,
                      command=generar).pack(side="left", padx=PAD_M)
