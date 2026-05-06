"""
Base class for all modal dialogs.

Usage
-----
Subclass BaseDialog, implement _build_ui(), call super().__init__() last,
and use get_result() to wait for the user's choice::

    class MyDialog(BaseDialog):
        def _build_ui(self):
            ctk.CTkLabel(self, text="Hello").pack(padx=20, pady=20)
            ctk.CTkButton(self, text="OK", command=self._on_confirm).pack()

        def _on_confirm(self):
            self._result = "confirmed"
            super()._on_confirm()

    dlg = MyDialog(parent, "My dialog", width=300, height=150)
    result = dlg.get_result()   # blocks until closed
"""
import customtkinter as ctk


class BaseDialog(ctk.CTkToplevel):
    """
    Modal CTkToplevel.  Subclasses implement _build_ui().

    _result is None until _on_confirm() stores a value.
    get_result() blocks via wait_window() and returns whatever _on_confirm set.
    """

    def __init__(self, parent, title: str,
                 width: int = 500, height: int = 400):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self._result = None

        # Center relative to parent
        self.update_idletasks()
        px = parent.winfo_rootx() + max(0, (parent.winfo_width()  - width)  // 2)
        py = parent.winfo_rooty() + max(0, (parent.winfo_height() - height) // 2)
        self.geometry(f"{width}x{height}+{px}+{py}")

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

        # CTkToplevel starts withdrawn and becomes visible via an internal after().
        # grab_set() requires the window to be viewable — defer it 200 ms.
        self.after(200, self._setup_modal)

    # ── Modal setup ───────────────────────────────────────────────────────────

    def _setup_modal(self) -> None:
        """Called 200 ms after init, once CTkToplevel is actually visible."""
        self.grab_set()
        self.focus_force()

    # ── Subclass interface ────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        """Override to populate the dialog with widgets."""
        raise NotImplementedError

    def _on_confirm(self) -> None:
        """Call super() after setting self._result."""
        self.grab_release()
        self.destroy()

    def _on_cancel(self) -> None:
        self._result = None
        self.grab_release()
        self.destroy()

    # ── Public API ────────────────────────────────────────────────────────────

    def get_result(self):
        """Block until the dialog is closed and return _result (or None)."""
        self.wait_window()
        return self._result
