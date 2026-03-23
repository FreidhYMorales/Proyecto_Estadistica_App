"""
Centralized theme configuration for the CustomTkinter UI.

Import this module BEFORE creating any CTK widgets so that
appearance mode and color theme are set globally.
"""
import sys
import customtkinter as ctk
from tkinter import ttk

# ── Global appearance ─────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Platform-aware font scale ──────────────────────────────────────────────────
# macOS renders fonts ~15% larger than Windows/Linux at 1× DPI.
_SCALE: float = 1.15 if sys.platform == "darwin" else 1.0


def scaled(size: int) -> int:
    """Returns a platform-scaled font/padding size (minimum 8)."""
    return max(8, int(size * _SCALE))


# ── Font presets ───────────────────────────────────────────────────────────────
FONT_TITLE   = ("Arial", scaled(18), "bold")
FONT_SECTION = ("Arial", scaled(12), "bold")
FONT_NORMAL  = ("Arial", scaled(11))
FONT_SMALL   = ("Arial", scaled(10))
FONT_MONO    = ("Courier New", scaled(10))
FONT_MONO_SM = ("Courier New", scaled(9))

# ── Padding presets ────────────────────────────────────────────────────────────
PAD_XS = scaled(3)
PAD_S  = scaled(5)
PAD_M  = scaled(10)
PAD_L  = scaled(16)

# ── Semantic color aliases (used in plain tk/ttk widgets only) ─────────────────
# CTK widgets pick up their own colors from the active theme.
COLOR_TREEVIEW_BG       = "#2b2b2b"
COLOR_TREEVIEW_FG       = "#dcddde"
COLOR_TREEVIEW_HEADING  = "#1f6aa5"
COLOR_TREEVIEW_SELECT   = "#144870"
COLOR_CANVAS_BG         = "#1e1e2e"


# ── TTK dark style for Treeview ────────────────────────────────────────────────
def apply_treeview_dark_style() -> None:
    """
    Applies a dark theme to all ttk.Treeview widgets tagged 'Dark.Treeview'.
    Call once after the Tk root is created.
    """
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    row_h = scaled(26)

    style.configure(
        "Dark.Treeview",
        background=COLOR_TREEVIEW_BG,
        foreground=COLOR_TREEVIEW_FG,
        fieldbackground=COLOR_TREEVIEW_BG,
        bordercolor="#3a3a3a",
        lightcolor=COLOR_TREEVIEW_BG,
        darkcolor=COLOR_TREEVIEW_BG,
        rowheight=row_h,
        font=("Arial", scaled(10)),
    )
    style.configure(
        "Dark.Treeview.Heading",
        background=COLOR_TREEVIEW_HEADING,
        foreground="white",
        relief="flat",
        font=("Arial", scaled(10), "bold"),
    )
    style.map(
        "Dark.Treeview",
        background=[("selected", COLOR_TREEVIEW_SELECT)],
        foreground=[("selected", "white")],
    )
    style.map(
        "Dark.Treeview.Heading",
        background=[("active", "#0d3a5c")],
    )
    # Scrollbar matching dark palette
    style.configure(
        "Dark.Vertical.TScrollbar",
        background="#3a3a3a",
        troughcolor=COLOR_TREEVIEW_BG,
        arrowcolor=COLOR_TREEVIEW_FG,
    )
    style.configure(
        "Dark.Horizontal.TScrollbar",
        background="#3a3a3a",
        troughcolor=COLOR_TREEVIEW_BG,
        arrowcolor=COLOR_TREEVIEW_FG,
    )
