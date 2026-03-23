"""
Reusable UI components built with CustomTkinter.

All widgets in this module inherit from CTK classes so they participate in
automatic dark/light theming. Plain tk/ttk widgets (Treeview, Canvas) are
kept where CTK has no equivalent but receive manual dark styling.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from views.theme import (
    FONT_NORMAL, FONT_SMALL, FONT_MONO,
    PAD_S, PAD_M,
    apply_treeview_dark_style,
)


# ── Utility ───────────────────────────────────────────────────────────────────

def clear_frame(frame) -> None:
    """Destroys all child widgets inside a CTK or tk frame."""
    for widget in frame.winfo_children():
        widget.destroy()


# ── CTkDropdown ───────────────────────────────────────────────────────────────

class CTkDropdown:
    """
    A CTkButton that shows a floating dropdown list of action buttons on click.
    Replaces tk.Menubutton + tk.Menu with a CTK-native equivalent.

    Usage::

        dropdown = CTkDropdown(toolbar, text="Gráficos de Frecuencia", items=[
            ("Histograma",          self._show_histogram),
            ("Polígono de Frecuencia", self._show_polygon),
        ])
        dropdown.pack(side="left", padx=PAD_S)
    """

    def __init__(self, parent, text: str, items: list, **btn_kwargs):
        """
        Args:
            parent: CTK or tk container.
            text:   Label shown on the button (an arrow indicator is appended).
            items:  List of (label, callback) tuples for each menu entry.
            **btn_kwargs: Forwarded to CTkButton (e.g. font=, width=).
        """
        self._items = items
        self._popup: ctk.CTkFrame | None = None
        self._close_binding: str | None = None  # funcid returned by root.bind()

        default_kwargs = dict(font=FONT_NORMAL, height=32)
        default_kwargs.update(btn_kwargs)

        self._btn = ctk.CTkButton(
            parent,
            text=f"{text}  ▾",
            command=self._toggle,
            **default_kwargs,
        )

    # ── Geometry delegates ────────────────────────────────────────────────────

    def pack(self, **kw) -> None:
        self._btn.pack(**kw)

    def grid(self, **kw) -> None:
        self._btn.grid(**kw)

    def place(self, **kw) -> None:
        self._btn.place(**kw)

    # ── Dropdown logic ────────────────────────────────────────────────────────

    def _toggle(self) -> None:
        if self._popup and self._popup.winfo_exists():
            self._close()
        else:
            self._open()

    def _open(self) -> None:
        root = self._btn.winfo_toplevel()
        rx, ry = root.winfo_rootx(), root.winfo_rooty()
        bx = self._btn.winfo_rootx() - rx
        by = self._btn.winfo_rooty() - ry + self._btn.winfo_height()

        popup = ctk.CTkFrame(root, corner_radius=8, border_width=1)
        popup.lift()
        popup.place(x=bx, y=by)

        for label, cmd in self._items:
            ctk.CTkButton(
                popup,
                text=label,
                anchor="w",
                height=30,
                font=FONT_SMALL,
                fg_color="transparent",
                hover_color=("gray80", "gray30"),
                text_color=("gray10", "gray90"),
                command=self._make_cb(cmd),
            ).pack(fill="x", padx=3, pady=2)

        self._popup = popup
        self._close_binding = root.bind("<Button-1>", self._close_if_outside, add=True)

    def _close(self) -> None:
        if self._popup and self._popup.winfo_exists():
            self._popup.destroy()
        self._popup = None
        if self._close_binding is not None:
            try:
                self._btn.winfo_toplevel().unbind("<Button-1>", self._close_binding)
            except Exception:
                pass
            self._close_binding = None

    def _close_if_outside(self, event: tk.Event) -> None:
        if not (self._popup and self._popup.winfo_exists()):
            return
        px, py = self._popup.winfo_rootx(), self._popup.winfo_rooty()
        pw, ph = self._popup.winfo_width(), self._popup.winfo_height()
        if not (px <= event.x_root <= px + pw and py <= event.y_root <= py + ph):
            self._close()

    def _make_cb(self, cmd):
        def cb():
            self._close()
            cmd()
        return cb


# ── CTkLabelSection ───────────────────────────────────────────────────────────

class CTkLabelSection(ctk.CTkFrame):
    """
    A CTkFrame with a bold title label at the top.
    Replaces tk.LabelFrame for a cleaner CTK look.
    """

    def __init__(self, parent, title: str, **kwargs):
        kwargs.setdefault("corner_radius", 8)
        super().__init__(parent, **kwargs)

        self._header = ctk.CTkLabel(
            self, text=title, font=FONT_NORMAL,
            anchor="w", text_color=("gray20", "gray80"),
        )
        self._header.grid(row=0, column=0, sticky="ew", padx=PAD_M, pady=(PAD_S, 0))
        self.columnconfigure(0, weight=1)

    @property
    def inner_row(self) -> int:
        """First row available for content (below the title label)."""
        return 1


# ── GraphCanvas ───────────────────────────────────────────────────────────────

class GraphCanvas:
    """
    Embeds a matplotlib Figure inside a CTkFrame with a navigation toolbar.

    Uses grid() so it participates correctly in grid-managed parent frames.
    The parent must have rowconfigure(0, weight=1) and columnconfigure(0, weight=1)
    (as returned by the _graph_container() helpers in each panel).
    """

    def __init__(self, parent):
        self._frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=6)
        self._frame.grid(row=0, column=0, sticky="nsew", padx=PAD_M, pady=PAD_M)
        self._canvas = None

    def render(self, fig: Figure) -> None:
        """Replaces any existing graph with a new Figure."""
        clear_frame(self._frame)
        canvas = FigureCanvasTkAgg(fig, master=self._frame)
        canvas.draw()
        toolbar = NavigationToolbar2Tk(canvas, self._frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self._canvas = canvas


# ── ScrollableCanvas ──────────────────────────────────────────────────────────

class ScrollableCanvas(ctk.CTkFrame):
    """
    tk.Canvas with always-present CTkScrollbars in a grid layout.

    Coordinate model
    ─────────────────
    All items are drawn in a fixed "virtual" space (virtual_w × virtual_h px).
    The widget viewport is a scrollable window into that space.
    On window resize only the *viewport size* changes — item coordinates never
    need to be recalculated.

    Usage::

        sc = ScrollableCanvas(parent, virtual_w=2000, virtual_h=1400, bg="#1e1e2e")
        sc.grid(row=0, column=0, sticky="nsew")
        sc.canvas.create_rectangle(...)   # draw in virtual coordinates
        sc.expand_scrollregion()          # call after drawing

    Mouse-wheel scrolling is NOT bound automatically so consumers can define
    their own wheel handlers (e.g. Ctrl+wheel for zoom).
    """

    def __init__(self, parent, virtual_w: int = 2000, virtual_h: int = 1400,
                 bg: str = "#1e1e2e", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._virtual_w = virtual_w
        self._virtual_h = virtual_h

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            self,
            bg=bg,
            highlightthickness=0,
            scrollregion=(0, 0, virtual_w, virtual_h),
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        _sb_y = ctk.CTkScrollbar(self, orientation="vertical",
                                  command=self.canvas.yview)
        _sb_y.grid(row=0, column=1, sticky="ns")

        _sb_x = ctk.CTkScrollbar(self, orientation="horizontal",
                                  command=self.canvas.xview)
        _sb_x.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(
            yscrollcommand=_sb_y.set,
            xscrollcommand=_sb_x.set,
        )

    def expand_scrollregion(self) -> None:
        """Expands scrollregion to tightly enclose all drawn items (+ 20 px margin)."""
        bbox = self.canvas.bbox("all")
        if bbox:
            self.canvas.configure(scrollregion=(
                bbox[0] - 20, bbox[1] - 20,
                max(bbox[2] + 20, self._virtual_w),
                max(bbox[3] + 20, self._virtual_h),
            ))


# ── ResultTextWidget ──────────────────────────────────────────────────────────

class ResultTextWidget:
    """
    A scrollable, read-only CTkTextbox for displaying formatted statistical results.
    Supports exporting content to a .txt file.
    """

    def __init__(self, parent, font: tuple = FONT_MONO, **kwargs):
        self._textbox = ctk.CTkTextbox(
            parent,
            font=font,
            wrap="none",
            state="disabled",
            **kwargs,
        )
        self._textbox.pack(fill=tk.BOTH, expand=True, padx=PAD_M, pady=PAD_M)

    def set(self, content: str) -> None:
        """Replaces the current text content."""
        self._textbox.configure(state="normal")
        self._textbox.delete("1.0", tk.END)
        self._textbox.insert(tk.END, content)
        self._textbox.configure(state="disabled")

    def get(self) -> str:
        """Returns the current text content."""
        return self._textbox.get("1.0", tk.END).strip()

    def clear(self) -> None:
        self._textbox.configure(state="normal")
        self._textbox.delete("1.0", tk.END)
        self._textbox.configure(state="disabled")

    def export(self, default_filename: str = "resultados.txt") -> None:
        """Opens a save-as dialog and writes the content to a .txt file."""
        content = self.get()
        if not content:
            messagebox.showwarning("Exportar", "No hay resultados para exportar.")
            return
        path = filedialog.asksaveasfilename(
            title="Guardar resultados",
            defaultextension=".txt",
            initialfile=default_filename,
            filetypes=(("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")),
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Exportar", f"Resultados guardados en:\n{path}")
        except OSError as e:
            messagebox.showerror("Error al guardar", str(e))


# ── DataTreeview ──────────────────────────────────────────────────────────────

class DataTreeview:
    """
    Displays a pandas DataFrame in a dark-styled ttk.Treeview.
    Uses the 'Dark.Treeview' ttk style defined in views/theme.py.
    """

    def __init__(self, parent):
        apply_treeview_dark_style()

        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill=tk.BOTH, expand=True, padx=PAD_S, pady=PAD_S)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        sb_y = ttk.Scrollbar(frame, orient="vertical",
                              style="Dark.Vertical.TScrollbar")
        sb_y.grid(row=0, column=1, sticky="ns")
        sb_x = ttk.Scrollbar(frame, orient="horizontal",
                              style="Dark.Horizontal.TScrollbar")
        sb_x.grid(row=1, column=0, sticky="ew")

        self._tree = ttk.Treeview(
            frame, style="Dark.Treeview",
            yscrollcommand=sb_y.set,
            xscrollcommand=sb_x.set,
        )
        self._tree.grid(row=0, column=0, sticky="nsew")
        sb_y.config(command=self._tree.yview)
        sb_x.config(command=self._tree.xview)

    def load(self, dataframe) -> None:
        """Loads a pandas DataFrame into the treeview."""
        self._tree.delete(*self._tree.get_children())
        self._tree["columns"] = list(dataframe.columns)
        self._tree["show"] = "headings"
        for col in dataframe.columns:
            self._tree.heading(col, text=col)
            self._tree.column(col, anchor="center", width=90, minwidth=60)
        for _, row in dataframe.iterrows():
            self._tree.insert("", "end", values=list(row))


# ── VariableSelector ──────────────────────────────────────────────────────────

class VariableSelector:
    """A labeled CTkComboBox for selecting a column from the data table."""

    def __init__(self, parent, label: str, columns: tuple, side=tk.LEFT):
        ctk.CTkLabel(
            parent, text=label, font=FONT_SMALL, anchor="w",
        ).pack(side=side, padx=PAD_S)
        self._combo = ctk.CTkComboBox(
            parent, values=list(columns), state="readonly", width=180, font=FONT_SMALL,
        )
        if columns:
            self._combo.set(columns[0])
        self._combo.pack(side=side, padx=PAD_S)

    def get(self) -> str:
        return self._combo.get()

    def set_columns(self, columns: tuple) -> None:
        self._combo.configure(values=list(columns))
        if columns:
            self._combo.set(columns[0])
