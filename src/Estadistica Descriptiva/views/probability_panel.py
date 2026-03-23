import tkinter as tk
from tkinter import ttk, messagebox
import math
import customtkinter as ctk

from views.theme import (
    FONT_SECTION, FONT_NORMAL, FONT_SMALL,
    PAD_XS, PAD_S, PAD_M, PAD_L,
    COLOR_CANVAS_BG,
)
from views.components import CTkDropdown, ScrollableCanvas
import utils.probability as prob_utils


class ProbabilityPanel:
    """Panel for probability calculations and tree diagrams."""

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
            self._toolbar, "Eventos",
            items=[
                ("Sucesos Simples",        self._show_simple),
                ("Sucesos Excluyentes",    self._show_exclusive),
                ("Sucesos No Excluyentes", self._show_non_exclusive),
                ("Sucesos Independientes", self._show_independent),
                ("Teorema de Bayes",       self._show_bayes),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "Diagrama",
            items=[("Diagrama de Árbol", self._show_tree_diagram)],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

        CTkDropdown(
            self._toolbar, "Distribuciones",
            items=[
                ("Distribución de Bernoulli", self._show_bernoulli),
                ("Distribución Binomial",     self._show_binomial),
                ("Distribución de Poisson",   self._show_poisson),
                ("Distribución Normal",       self._show_normal),
            ],
            font=FONT_SMALL,
        ).pack(side="left", padx=PAD_S, pady=PAD_S)

    # ── Layout helpers ────────────────────────────────────────────────────────

    def _clear(self) -> None:
        for w in self._content.winfo_children():
            w.destroy()

    def _make_card(self, title: str) -> ctk.CTkFrame:
        """Returns a fresh card frame with title label."""
        self._clear()
        self._content.rowconfigure(0, weight=1)
        self._content.columnconfigure(0, weight=1)

        card = ctk.CTkFrame(self._content, corner_radius=10)
        card.grid(row=0, column=0, sticky="nsew", padx=PAD_L, pady=PAD_L)
        card.rowconfigure(0, weight=0)
        card.rowconfigure(1, weight=1)
        card.columnconfigure(0, weight=1)

        ctk.CTkLabel(card, text=title, font=FONT_SECTION, anchor="w").grid(
            row=0, column=0, sticky="w", padx=PAD_L, pady=(PAD_M, PAD_S))

        return card

    # ── Sample space input (shared) ───────────────────────────────────────────

    def _build_sample_space(self, card: ctk.CTkFrame) -> dict:
        """Builds sample space entry UI; returns state dict."""
        state: dict = {"samples": []}

        entry_row = ctk.CTkFrame(card, fg_color="transparent")
        entry_row.grid(row=1, column=0, sticky="ew", padx=PAD_L, pady=PAD_S)

        ctk.CTkLabel(entry_row, text="Nombre:", font=FONT_SMALL).pack(side="left", padx=PAD_S)
        name_e = ctk.CTkEntry(entry_row, width=120, height=28, font=FONT_SMALL,
                               placeholder_text="Ej: Cara")
        name_e.pack(side="left", padx=PAD_S)
        ctk.CTkLabel(entry_row, text="Cantidad:", font=FONT_SMALL).pack(side="left", padx=(PAD_M, PAD_S))
        qty_e = ctk.CTkEntry(entry_row, width=60, height=28, font=FONT_SMALL)
        qty_e.pack(side="left", padx=PAD_S)

        # Dark-styled Treeview for sample list
        tree_frame = ctk.CTkFrame(card, fg_color="transparent")
        tree_frame.grid(row=2, column=0, sticky="ew", padx=PAD_L, pady=PAD_S)
        tree_frame.columnconfigure(0, weight=1)

        from views.theme import apply_treeview_dark_style
        apply_treeview_dark_style()
        tree = ttk.Treeview(tree_frame, columns=("Muestra", "Cantidad"),
                            show="headings", height=5, style="Dark.Treeview")
        tree.heading("Muestra", text="Muestra")
        tree.heading("Cantidad", text="Cantidad")
        tree.column("Muestra", width=150)
        tree.column("Cantidad", width=80)
        tree.grid(row=0, column=0, sticky="ew")

        def refresh():
            tree.delete(*tree.get_children())
            for name, qty in state["samples"]:
                tree.insert("", "end", values=(name, qty))

        def add_sample():
            name = name_e.get().strip()
            try:
                qty = int(qty_e.get())
                if not name or qty <= 0:
                    raise ValueError
                state["samples"].append((name, qty))
                name_e.delete(0, "end")
                qty_e.delete(0, "end")
                refresh()
            except (ValueError, TypeError):
                messagebox.showerror("Error", "Nombre y cantidad válidos requeridos.")

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.grid(row=3, column=0, sticky="ew", padx=PAD_L, pady=PAD_S)

        ctk.CTkButton(btn_row, text="Agregar Muestra", font=FONT_SMALL, height=28,
                      fg_color=("gray65", "gray35"),
                      command=add_sample).pack(side="left", padx=PAD_S)

        state["btn_row"] = btn_row
        state["result_label"] = ctk.CTkLabel(
            card, text="", font=FONT_NORMAL,
            text_color=("#d4a017", "#f0c040"),
        )
        state["result_label"].grid(row=4, column=0, sticky="ew", padx=PAD_L, pady=PAD_S)
        return state

    def _get_universe(self, samples: list) -> list:
        universe = []
        for name, qty in samples:
            universe.extend([name] * qty)
        return universe

    # ── Event panels ──────────────────────────────────────────────────────────

    def _show_simple(self) -> None:
        card = self._make_card("Sucesos Simples")
        card.rowconfigure(2, weight=1)
        state = self._build_sample_space(card)

        def calcular():
            if not state["samples"]:
                state["result_label"].configure(text="Primero ingrese el espacio muestral.")
                return
            muestras: dict = {}
            for name, qty in state["samples"]:
                muestras[name] = muestras.get(name, 0) + qty

            win = ctk.CTkToplevel()
            win.title("Seleccionar Evento A")
            win.resizable(False, False)
            win.grab_set()

            sel_frame = ctk.CTkScrollableFrame(win, width=260, height=200)
            sel_frame.pack(padx=PAD_L, pady=PAD_M)

            check_vars: dict[str, ctk.BooleanVar] = {}
            for name in muestras:
                var = ctk.BooleanVar()
                check_vars[name] = var
                ctk.CTkCheckBox(sel_frame, text=name, variable=var,
                                font=FONT_SMALL).pack(anchor="w", pady=PAD_XS)

            def confirmar():
                total = sum(muestras.values())
                favorable = sum(muestras[n] for n, v in check_vars.items() if v.get())
                p = prob_utils.simple_probability(favorable, total)
                state["result_label"].configure(text=f"P(A) = {p * 100:.2f}%")
                win.destroy()

            ctk.CTkButton(win, text="Calcular P(A)", font=FONT_SMALL,
                          command=confirmar).pack(pady=PAD_M)

        ctk.CTkButton(state["btn_row"], text="Seleccionar Evento A y Calcular",
                      font=FONT_SMALL, height=28, command=calcular).pack(
            side="left", padx=PAD_S)

    def _show_exclusive(self) -> None:
        card = self._make_card("Sucesos Excluyentes")
        card.rowconfigure(2, weight=1)
        state = self._build_sample_space(card)
        self._add_two_event_button(state, "exclusive")

    def _show_non_exclusive(self) -> None:
        card = self._make_card("Sucesos No Excluyentes")
        card.rowconfigure(2, weight=1)
        state = self._build_sample_space(card)
        self._add_two_event_button(state, "non_exclusive")

    def _show_independent(self) -> None:
        card = self._make_card("Sucesos Independientes")
        card.rowconfigure(2, weight=1)
        state = self._build_sample_space(card)
        self._add_two_event_button(state, "independent")

    def _show_bayes(self) -> None:
        card = self._make_card("Teorema de Bayes")
        card.rowconfigure(2, weight=1)
        state = self._build_sample_space(card)
        self._add_two_event_button(state, "bayes")

    def _add_two_event_button(self, state: dict, mode: str) -> None:
        labels = {
            "exclusive":     "Seleccionar Eventos y Calcular",
            "non_exclusive": "Seleccionar Eventos y Calcular",
            "independent":   "Seleccionar Eventos A y B",
            "bayes":         "Seleccionar Eventos — Calcular P(A|B)",
        }

        def calcular():
            if not state["samples"]:
                state["result_label"].configure(text="Primero ingrese el espacio muestral.")
                return
            universe = self._get_universe(state["samples"])
            unique = sorted(set(universe))
            total = len(universe)

            win = ctk.CTkToplevel()
            win.title("Seleccionar Eventos A y B")
            win.geometry("400x420")
            win.grab_set()

            content = ctk.CTkFrame(win, fg_color="transparent")
            content.pack(fill="both", expand=True, padx=PAD_L, pady=PAD_M)
            content.columnconfigure((0, 1), weight=1)

            ctk.CTkLabel(content, text="Evento A", font=FONT_SMALL).grid(
                row=0, column=0, sticky="w", pady=PAD_S)
            ctk.CTkLabel(content, text="Evento B", font=FONT_SMALL).grid(
                row=0, column=1, sticky="w", pady=PAD_S)

            vars_a: dict[str, ctk.BooleanVar] = {}
            vars_b: dict[str, ctk.BooleanVar] = {}
            for i, name in enumerate(unique, start=1):
                va, vb = ctk.BooleanVar(), ctk.BooleanVar()
                vars_a[name] = va
                vars_b[name] = vb
                ctk.CTkCheckBox(content, text=name, variable=va,
                                font=FONT_SMALL).grid(row=i, column=0, sticky="w")
                ctk.CTkCheckBox(content, text=name, variable=vb,
                                font=FONT_SMALL).grid(row=i, column=1, sticky="w")

            result_lbl = ctk.CTkLabel(win, text="", font=FONT_SMALL,
                                      text_color=("#d4a017", "#f0c040"))
            result_lbl.pack(pady=PAD_S)

            def compute():
                A = {n for n, v in vars_a.items() if v.get()}
                B = {n for n, v in vars_b.items() if v.get()}
                if not A or not B:
                    result_lbl.configure(text="Selecciona al menos un elemento para A y B.")
                    return
                count_a  = sum(1 for x in universe if x in A)
                count_b  = sum(1 for x in universe if x in B)
                count_ab = sum(1 for x in universe if x in A and x in B)
                p_a, p_b, p_ab = count_a / total, count_b / total, count_ab / total

                if mode == "exclusive":
                    if A.isdisjoint(B):
                        r = prob_utils.exclusive_probability(p_a, p_b)
                        result_lbl.configure(text=f"P(A ∪ B) = {r * 100:.2f}%")
                    else:
                        result_lbl.configure(text="Los eventos NO son excluyentes.")
                elif mode == "non_exclusive":
                    r = prob_utils.non_exclusive_probability(p_a, p_b, p_ab)
                    result_lbl.configure(
                        text=f"P(A)={p_a:.4f}, P(B)={p_b:.4f}, P(A∩B)={p_ab:.4f}\n"
                             f"P(A ∪ B) = {r:.4f} ({r * 100:.2f}%)")
                elif mode == "independent":
                    r = prob_utils.independent_probability(p_a, p_b)
                    result_lbl.configure(
                        text=f"P(A)={p_a:.4f}, P(B)={p_b:.4f}\n"
                             f"P(A ∩ B) = {r:.4f} ({r * 100:.2f}%)")
                elif mode == "bayes":
                    p_b_given_a = p_ab / p_a if p_a > 0 else 0.0
                    try:
                        r = prob_utils.bayes(p_b_given_a, p_a, p_b)
                        result_lbl.configure(text=f"P(A | B) = {r:.4f} ({r * 100:.2f}%)")
                    except ZeroDivisionError as e:
                        result_lbl.configure(text=str(e))

            ctk.CTkButton(win, text="Calcular", font=FONT_SMALL,
                          command=compute).pack(pady=PAD_S)

        ctk.CTkButton(state["btn_row"], text=labels[mode], font=FONT_SMALL, height=28,
                      command=calcular).pack(side="left", padx=PAD_S)

    # ── Distributions ─────────────────────────────────────────────────────────

    def _show_bernoulli(self) -> None:
        card = self._make_card("Distribución de Bernoulli")
        card.columnconfigure(1, weight=1)

        _lbl = lambda t, r: ctk.CTkLabel(card, text=t, font=FONT_SMALL, anchor="w").grid(
            row=r, column=0, sticky="w", padx=PAD_L, pady=PAD_S)
        _lbl("Probabilidad de éxito (p):", 1)
        p_entry = ctk.CTkEntry(card, width=120, height=28, font=FONT_SMALL)
        p_entry.grid(row=1, column=1, sticky="w", padx=PAD_S, pady=PAD_S)

        _lbl("Resultado (0=fracaso, 1=éxito):", 2)
        r_combo = ctk.CTkComboBox(card, values=["0", "1"], state="readonly",
                                  font=FONT_SMALL, width=80, height=28)
        r_combo.set("1")
        r_combo.grid(row=2, column=1, sticky="w", padx=PAD_S, pady=PAD_S)

        result_lbl = ctk.CTkLabel(card, text="", font=FONT_NORMAL,
                                  text_color=("#d4a017", "#f0c040"))
        result_lbl.grid(row=4, column=0, columnspan=2, pady=PAD_M)

        def calcular():
            try:
                res = prob_utils.bernoulli(float(p_entry.get()), int(r_combo.get()))
                result_lbl.configure(
                    text=f"P(X={res['success']}) = {res['probability']:.6f}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(card, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).grid(
            row=3, column=0, columnspan=2, pady=PAD_M, padx=PAD_L, sticky="ew")

    def _show_binomial(self) -> None:
        card = self._make_card("Distribución Binomial")
        card.columnconfigure(1, weight=1)
        fields = [("Número de ensayos (n):", "n"), ("Número de éxitos (k):", "k"),
                  ("Probabilidad de éxito (p):", "p")]
        entries: dict[str, ctk.CTkEntry] = {}
        for i, (label, key) in enumerate(fields, start=1):
            ctk.CTkLabel(card, text=label, font=FONT_SMALL, anchor="w").grid(
                row=i, column=0, sticky="w", padx=PAD_L, pady=PAD_S)
            e = ctk.CTkEntry(card, width=120, height=28, font=FONT_SMALL)
            e.grid(row=i, column=1, sticky="w", padx=PAD_S, pady=PAD_S)
            entries[key] = e

        result_lbl = ctk.CTkLabel(card, text="", font=FONT_SMALL,
                                  text_color=("#d4a017", "#f0c040"))
        result_lbl.grid(row=len(fields) + 2, column=0, columnspan=2, pady=PAD_M)

        def calcular():
            try:
                res = prob_utils.binomial(int(entries["n"].get()), int(entries["k"].get()),
                                          float(entries["p"].get()))
                result_lbl.configure(
                    text=f"P(X={res['k']}) = {res['probability']:.6f}\n"
                         f"Media = {res['mean']:.4f}   "
                         f"Varianza = {res['variance']:.4f}   σ = {res['std']:.4f}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(card, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).grid(
            row=len(fields) + 1, column=0, columnspan=2,
            pady=PAD_M, padx=PAD_L, sticky="ew")

    def _show_poisson(self) -> None:
        card = self._make_card("Distribución de Poisson")
        card.columnconfigure(1, weight=1)

        ctk.CTkLabel(card, text="Tasa media (λ):", font=FONT_SMALL, anchor="w").grid(
            row=1, column=0, sticky="w", padx=PAD_L, pady=PAD_S)
        lam_e = ctk.CTkEntry(card, width=120, height=28, font=FONT_SMALL)
        lam_e.grid(row=1, column=1, sticky="w", padx=PAD_S, pady=PAD_S)

        ctk.CTkLabel(card, text="Número de eventos (k):", font=FONT_SMALL, anchor="w").grid(
            row=2, column=0, sticky="w", padx=PAD_L, pady=PAD_S)
        k_e = ctk.CTkEntry(card, width=120, height=28, font=FONT_SMALL)
        k_e.grid(row=2, column=1, sticky="w", padx=PAD_S, pady=PAD_S)

        result_lbl = ctk.CTkLabel(card, text="", font=FONT_SMALL,
                                  text_color=("#d4a017", "#f0c040"))
        result_lbl.grid(row=4, column=0, columnspan=2, pady=PAD_M)

        def calcular():
            try:
                res = prob_utils.poisson(float(lam_e.get()), int(k_e.get()))
                result_lbl.configure(
                    text=f"P(X={res['k']}) = {res['probability']:.6f}\n"
                         f"Media = λ = {res['mean']:.4f}   "
                         f"Varianza = {res['variance']:.4f}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(card, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).grid(
            row=3, column=0, columnspan=2, pady=PAD_M, padx=PAD_L, sticky="ew")

    def _show_normal(self) -> None:
        card = self._make_card("Distribución Normal")
        card.columnconfigure(1, weight=1)
        fields = [("Valor (x):", "x"), ("Media (μ):", "mu"),
                  ("Desviación estándar (σ):", "sigma")]
        entries: dict[str, ctk.CTkEntry] = {}
        for i, (label, key) in enumerate(fields, start=1):
            ctk.CTkLabel(card, text=label, font=FONT_SMALL, anchor="w").grid(
                row=i, column=0, sticky="w", padx=PAD_L, pady=PAD_S)
            e = ctk.CTkEntry(card, width=120, height=28, font=FONT_SMALL)
            e.grid(row=i, column=1, sticky="w", padx=PAD_S, pady=PAD_S)
            entries[key] = e

        result_lbl = ctk.CTkLabel(card, text="", font=FONT_SMALL,
                                  text_color=("#d4a017", "#f0c040"))
        result_lbl.grid(row=len(fields) + 2, column=0, columnspan=2, pady=PAD_M)

        def calcular():
            try:
                res = prob_utils.normal_distribution(
                    float(entries["x"].get()),
                    float(entries["mu"].get()),
                    float(entries["sigma"].get()))
                result_lbl.configure(
                    text=f"Z = {res['z']:.4f}\n"
                         f"PDF f(x) = {res['pdf']:.6f}\n"
                         f"CDF P(X ≤ x) = {res['cdf']:.6f} ({res['cdf'] * 100:.2f}%)")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        ctk.CTkButton(card, text="Calcular", font=FONT_SMALL, height=28,
                      command=calcular).grid(
            row=len(fields) + 1, column=0, columnspan=2,
            pady=PAD_M, padx=PAD_L, sticky="ew")

    # ── Tree diagram ──────────────────────────────────────────────────────────

    def _show_tree_diagram(self) -> None:
        """Interactive tree diagram with zoom, pan, and branch probability calculations."""
        self._clear()
        self._content.rowconfigure(0, weight=1)
        self._content.columnconfigure(0, weight=1)

        outer = ctk.CTkFrame(self._content, fg_color="transparent")
        outer.grid(row=0, column=0, sticky="nsew")
        outer.rowconfigure(0, weight=1)
        outer.columnconfigure(0, weight=1)

        # Canvas wrapped in ScrollableCanvas (CTkScrollbar + virtual coordinate space)
        sc = ScrollableCanvas(outer, virtual_w=2000, virtual_h=1400, bg=COLOR_CANVAS_BG)
        sc.grid(row=0, column=0, sticky="nsew")
        canvas = sc.canvas  # all drawing calls use this reference

        # Control panel on the right
        ctrl = ctk.CTkScrollableFrame(outer, width=200, fg_color=("gray88", "gray18"))
        ctrl.grid(row=0, column=1, sticky="nsew", padx=(PAD_S, 0))

        # Node storage
        nodos: dict = {}
        counter = [0]
        selected: dict = {"id": None}
        current_scale = [1.0]
        min_scale, max_scale = 0.2, 4.0

        def new_id() -> int:
            counter[0] += 1
            return counter[0]

        def draw_tree() -> None:
            canvas.delete("all")
            if not nodos:
                return
            roots = [nid for nid, d in nodos.items()
                     if not any(nid in d2["hijos"] for d2 in nodos.values())]
            x_start, y_start, x_gap, y_gap = 80, 60, 180, 80

            def draw_node(nid, x, y, depth, sibling_idx):
                data = nodos[nid]
                x_pos = x_start + depth * x_gap
                y_pos = y + sibling_idx * y_gap
                r = 28
                color = "#e8a020" if selected["id"] == nid else "#1f6aa5"
                rect = canvas.create_rectangle(
                    x_pos - r, y_pos - r // 2, x_pos + r, y_pos + r // 2,
                    fill=color, outline="#ffffff", width=2)
                canvas.create_text(x_pos, y_pos - 6, text=data["evento"],
                                   font=("Arial", 9, "bold"), fill="white")
                canvas.create_text(x_pos, y_pos + 8, text=f"p={data['prob']}",
                                   font=("Arial", 8), fill="#cccccc")
                data["obj"] = (rect,)

                for ci, child_id in enumerate(data["hijos"]):
                    child_x = x_start + (depth + 1) * x_gap
                    child_y = y + sibling_idx * y_gap + ci * y_gap
                    canvas.create_line(x_pos + r, y_pos, child_x - r, child_y,
                                       fill="#555577", width=2)
                    draw_node(child_id, x, y + sibling_idx * y_gap, depth + 1, ci)

            for ri, root_id in enumerate(roots):
                draw_node(root_id, x_start, y_start, 0, ri)

            sc.expand_scrollregion()

        # Controls
        ctk.CTkLabel(ctrl, text="Evento:", font=FONT_SMALL, anchor="w").pack(
            fill="x", padx=PAD_S, pady=(PAD_M, PAD_XS))
        evento_entry = ctk.CTkEntry(ctrl, font=FONT_SMALL, height=28,
                                    placeholder_text="Nombre del evento")
        evento_entry.pack(fill="x", padx=PAD_S, pady=PAD_XS)

        ctk.CTkLabel(ctrl, text="Probabilidad:", font=FONT_SMALL, anchor="w").pack(
            fill="x", padx=PAD_S, pady=PAD_XS)
        prob_entry = ctk.CTkEntry(ctrl, font=FONT_SMALL, height=28)
        prob_entry.insert(0, "0.5")
        prob_entry.pack(fill="x", padx=PAD_S, pady=PAD_XS)

        def add_root():
            try:
                evento = evento_entry.get().strip()
                prob = float(prob_entry.get())
                if not evento:
                    return
                nid = new_id()
                nodos[nid] = {"evento": evento, "prob": prob, "hijos": [], "obj": ()}
                draw_tree()
                evento_entry.delete(0, "end")
            except ValueError:
                messagebox.showerror("Error", "Probabilidad inválida.")

        def add_child():
            if selected["id"] is None:
                messagebox.showwarning("", "Selecciona un nodo primero.")
                return
            try:
                evento = evento_entry.get().strip()
                prob = float(prob_entry.get())
                if not evento:
                    return
                nid = new_id()
                nodos[nid] = {"evento": evento, "prob": prob, "hijos": [], "obj": ()}
                nodos[selected["id"]]["hijos"].append(nid)
                draw_tree()
                evento_entry.delete(0, "end")
            except ValueError:
                messagebox.showerror("Error", "Probabilidad inválida.")

        def delete_node():
            if selected["id"] is None:
                return
            nid = selected["id"]

            def remove(n):
                for h in list(nodos[n]["hijos"]):
                    remove(h)
                nodos.pop(n, None)
            remove(nid)
            for d in nodos.values():
                if nid in d["hijos"]:
                    d["hijos"].remove(nid)
            selected["id"] = None
            draw_tree()

        def show_branches():
            results = []

            def traverse(nid, cumulative, path, probs):
                cp = cumulative * nodos[nid]["prob"]
                cur_path = path + [nodos[nid]["evento"]]
                cur_probs = probs + [nodos[nid]["prob"]]
                if not nodos[nid]["hijos"]:
                    results.append((cur_path, cur_probs, cp))
                else:
                    for child in nodos[nid]["hijos"]:
                        traverse(child, cp, cur_path, cur_probs)

            roots = [nid for nid, d in nodos.items()
                     if not any(nid in d2["hijos"] for d2 in nodos.values())]
            start_id = (selected["id"] if selected["id"] in roots
                        else (roots[0] if roots else None))
            if start_id is None:
                return
            traverse(start_id, 1.0, [], [])

            win = ctk.CTkToplevel()
            win.title("Ramas del Árbol")
            win.geometry("540x400")
            textbox = ctk.CTkTextbox(win, font=("Courier New", 10), wrap="none")
            textbox.pack(fill="both", expand=True, padx=PAD_L, pady=PAD_L)
            textbox.insert("end", "Ramas y probabilidades:\n" + "=" * 50 + "\n")
            for path, probs, total_prob in results:
                branch   = " → ".join(path)
                prob_str = " × ".join(str(p) for p in probs)
                textbox.insert("end", f"{branch}\n  {prob_str} = {total_prob:.6f}\n\n")
            textbox.configure(state="disabled")

        btn_cfg = dict(font=FONT_SMALL, height=30, corner_radius=6)
        for text, cmd in [
            ("Agregar Nodo Raíz",  add_root),
            ("Agregar Nodo Hijo",  add_child),
            ("Eliminar Nodo",      delete_node),
            ("Ver Ramas",          show_branches),
        ]:
            ctk.CTkButton(ctrl, text=text, command=cmd, **btn_cfg).pack(
                fill="x", padx=PAD_S, pady=PAD_XS)

        def on_click(event: tk.Event) -> None:
            cx, cy = canvas.canvasx(event.x), canvas.canvasy(event.y)
            clicked = canvas.find_overlapping(cx - 2, cy - 2, cx + 2, cy + 2)
            found = None
            for item in clicked:
                for nid, data in nodos.items():
                    if data.get("obj") and item == data["obj"][0]:
                        found = nid
                        break
                if found:
                    break

            # Only update colors — no full redraw
            if selected["id"] is not None:
                old = nodos.get(selected["id"])
                if old and old.get("obj"):
                    canvas.itemconfig(old["obj"][0], fill="#1f6aa5")

            selected["id"] = found
            if found is not None:
                new = nodos.get(found)
                if new and new.get("obj"):
                    canvas.itemconfig(new["obj"][0], fill="#e8a020")

        def on_wheel(event: tk.Event) -> None:
            delta = (event.delta if hasattr(event, "delta")
                     else (120 if getattr(event, "num", 0) == 4 else -120))
            state_flag = getattr(event, "state", 0)
            if state_flag & 0x0004:  # Ctrl held → zoom
                factor = 1.1 if delta > 0 else 0.9
                new_scale = current_scale[0] * factor
                if min_scale <= new_scale <= max_scale:
                    current_scale[0] = new_scale
                    cx, cy = canvas.canvasx(event.x), canvas.canvasy(event.y)
                    canvas.scale("all", cx, cy, factor, factor)
                    bbox = canvas.bbox("all")
                    if bbox:
                        canvas.configure(scrollregion=bbox)
                return "break"
            step = 1 if delta > 0 else -1
            if state_flag & 0x0001:
                canvas.xview_scroll(-step, "units")
            else:
                canvas.yview_scroll(-step, "units")
            return "break"

        canvas.bind("<Button-1>", on_click)
        canvas.bind("<Button-4>", on_wheel)
        canvas.bind("<Button-5>", on_wheel)
        canvas.bind_all("<MouseWheel>", on_wheel)
        canvas.bind("<Enter>", lambda e: canvas.focus_set())


def _count_descendants(nid: int, nodos: dict) -> int:
    return sum(1 + _count_descendants(child, nodos) for child in nodos[nid]["hijos"])
