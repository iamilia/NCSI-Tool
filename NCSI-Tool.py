import sys
import winreg
import ctypes
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QDialog, QLineEdit, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def run_as_admin():
    """Relaunch the script with administrator privileges"""
    try:
        script_path = sys.argv[0]
        if script_path.endswith('.py'):
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script_path}"', None, 1
            )
        else:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", script_path, "", None, 1
            )
        sys.exit()
    except Exception as e:
        MacMessageBox.show(None, THEMES[detect_system_theme()], "critical",
                            "Error", f"Failed to run as administrator: {str(e)}")
        sys.exit(1)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def detect_system_theme():
    """Read Windows' current app theme (light/dark) from the registry."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return "light" if value == 1 else "dark"
    except Exception:
        return "light"


# ---------------------------------------------------------------------------
# Theme palettes
#   Light  -> White + Rose/Pink
#   Dark   -> Petrol / Navy Blue + Teal & Amber accents
# ---------------------------------------------------------------------------

THEMES = {
    "light": {
        "window_bg":      "#FFF6F8",
        "card_bg":        "#FFFFFF",
        "card_border":    "#F3D9E0",
        "row_alt":        "#FDF0F3",
        "text_primary":   "#3A2A30",
        "text_secondary": "#9A7684",
        "accent":         "#E8879A",
        "accent_hover":   "#D96E85",
        "accent_soft":    "#FCE4EA",
        "danger":         "#E5677B",
        "danger_hover":   "#D14F65",
        "success":        "#5FBF9F",
        "success_hover":  "#4CA989",
        "info":           "#7FA6D9",
        "info_hover":     "#6690C7",
        "warn":           "#E7A854",
        "warn_hover":     "#D9963E",
        "divider":        "#F0DDE3",
        "custom_text":    "#FFFFFF",
    },
    "dark": {
        "window_bg":      "#0D1B2A",
        "card_bg":        "#16283E",
        "card_border":    "#20344C",
        "row_alt":        "#132435",
        "text_primary":   "#EAF2FA",
        "text_secondary": "#8FA6BE",
        "accent":         "#2EC4B6",
        "accent_hover":   "#26AA9E",
        "accent_soft":    "#16333A",
        "danger":         "#EF6461",
        "danger_hover":   "#D9534F",
        "success":        "#E9C46A",
        "success_hover":  "#D9AF52",
        "info":           "#4C8FD1",
        "info_hover":     "#3B77B5",
        "warn":           "#E3B341",
        "warn_hover":     "#D1A430",
        "divider":        "#1F3349",
        "custom_text":    "#0D1B2A",
    },
}


def build_stylesheet(t):
    return f"""
    QWidget {{
        background-color: {t['window_bg']};
        color: {t['text_primary']};
        font-family: 'Segoe UI', 'SF Pro Display', sans-serif;
    }}
    QLabel {{
        background: transparent;
    }}
    QLabel#TitleLabel {{
        font-size: 19px;
        font-weight: 700;
        color: {t['text_primary']};
    }}
    QLabel#SubtitleLabel {{
        font-size: 12px;
        color: {t['text_secondary']};
    }}
    QFrame#Card {{
        background-color: {t['card_bg']};
        border: 1px solid {t['card_border']};
        border-radius: 14px;
    }}
    QFrame#StatusRow {{
        background: transparent;
        border: none;
        border-bottom: 1px solid {t['divider']};
    }}
    QFrame#StatusRowLast {{
        background: transparent;
        border: none;
    }}
    QLabel#StatusKey {{
        font-size: 12px;
        color: {t['text_secondary']};
        font-weight: 600;
        background: transparent;
    }}
    QLabel#StatusVal {{
        font-size: 13px;
        color: {t['text_primary']};
        font-weight: 600;
        background: transparent;
    }}
    QFrame#Divider {{
        background-color: {t['divider']};
        max-height: 1px;
        min-height: 1px;
        border: none;
    }}
    QPushButton {{
        font-size: 13px;
        font-weight: 600;
        border-radius: 10px;
        padding: 12px;
        color: #FFFFFF;
        border: none;
    }}
    QPushButton#ThemeBtn {{
        background-color: {t['accent_soft']};
        color: {t['text_primary']};
        border-radius: 16px;
        padding: 6px 14px;
        font-size: 12px;
        font-weight: 600;
    }}
    QPushButton#ThemeBtn:hover {{
        background-color: {t['card_border']};
    }}
    QPushButton#RefreshBtn {{
        background-color: transparent;
        color: {t['accent']};
        font-size: 12px;
        font-weight: 700;
        padding: 4px 8px;
        border-radius: 6px;
    }}
    QPushButton#RefreshBtn:hover {{
        background-color: {t['accent_soft']};
    }}
    QPushButton#StatusBtn {{
        background-color: {t['info']};
    }}
    QPushButton#StatusBtn:hover {{
        background-color: {t['info_hover']};
    }}
    QPushButton#DisableBtn {{
        background-color: {t['danger']};
    }}
    QPushButton#DisableBtn:hover {{
        background-color: {t['danger_hover']};
    }}
    QPushButton#CustomBtn {{
        background-color: {t['success']};
        color: {t['custom_text']};
    }}
    QPushButton#CustomBtn:hover {{
        background-color: {t['success_hover']};
    }}
    QPushButton#UndoBtn {{
        background-color: {t['accent']};
    }}
    QPushButton#UndoBtn:hover {{
        background-color: {t['accent_hover']};
    }}
    QLabel#FooterLabel {{
        font-size: 11px;
        color: {t['text_secondary']};
    }}
    QLineEdit {{
        background-color: {t['window_bg']};
        border: 1px solid {t['card_border']};
        border-radius: 8px;
        padding: 8px 10px;
        color: {t['text_primary']};
        font-size: 13px;
    }}
    QLineEdit:focus {{
        border: 1px solid {t['accent']};
    }}

    /* --- Mac-style alert dialog --- */
    QDialog#MacAlert {{
        background-color: {t['card_bg']};
        border: 1px solid {t['card_border']};
        border-radius: 14px;
    }}
    QLabel#AlertIcon {{
        font-size: 28px;
        background: transparent;
    }}
    QLabel#AlertTitle {{
        font-size: 15px;
        font-weight: 700;
        color: {t['text_primary']};
        background: transparent;
    }}
    QLabel#AlertMessage {{
        font-size: 13px;
        color: {t['text_secondary']};
        background: transparent;
    }}
    QPushButton#AlertSecondary {{
        background-color: {t['accent_soft']};
        color: {t['text_primary']};
        border-radius: 9px;
        padding: 9px 16px;
        font-size: 13px;
        font-weight: 600;
    }}
    QPushButton#AlertSecondary:hover {{
        background-color: {t['card_border']};
    }}

    /* --- Custom probe dialog --- */
    QDialog#ProbeDialog {{
        background-color: {t['card_bg']};
        border: 1px solid {t['card_border']};
        border-radius: 14px;
    }}
    """


PRIMARY_COLORS = {
    "info":     ("accent", "accent_hover"),
    "warning":  ("warn", "warn_hover"),
    "critical": ("danger", "danger_hover"),
    "question": ("accent", "accent_hover"),
}
ICONS = {
    "info": "\u2139",       # info circle
    "warning": "\u26A0",    # warning triangle
    "critical": "\u26D4",   # no entry
    "question": "\u2753",   # question mark
}


# ---------------------------------------------------------------------------
# Mac-style themed alert dialog (replacement for QMessageBox)
# ---------------------------------------------------------------------------

class MacMessageBox(QDialog):
    def __init__(self, parent, theme, kind, title, message, buttons):
        super().__init__(parent)
        self.result_text = buttons[-1] if buttons else "OK"

        self.setObjectName("MacAlert")
        self.setWindowTitle(title)
        self.setFixedWidth(360)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setAutoFillBackground(True)
        self.setStyleSheet(build_stylesheet(theme))

        primary_key, primary_hover_key = PRIMARY_COLORS.get(kind, ("accent", "accent_hover"))
        primary_color = theme[primary_key]
        primary_hover = theme[primary_hover_key]

        root = QVBoxLayout()
        root.setContentsMargins(24, 22, 24, 20)
        root.setSpacing(10)

        top = QHBoxLayout()
        top.setSpacing(12)
        icon_lbl = QLabel(ICONS.get(kind, "\u2139"))
        icon_lbl.setObjectName("AlertIcon")
        icon_lbl.setStyleSheet(f"color: {primary_color};")
        top.addWidget(icon_lbl, alignment=Qt.AlignmentFlag.AlignTop)

        text_box = QVBoxLayout()
        text_box.setSpacing(4)
        title_lbl = QLabel(title)
        title_lbl.setObjectName("AlertTitle")
        title_lbl.setWordWrap(True)
        msg_lbl = QLabel(message)
        msg_lbl.setObjectName("AlertMessage")
        msg_lbl.setWordWrap(True)
        text_box.addWidget(title_lbl)
        text_box.addWidget(msg_lbl)
        top.addLayout(text_box)
        root.addLayout(top)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        primary_label = buttons[-1] if buttons else "OK"
        primary_btn = QPushButton(primary_label)
        primary_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        primary_btn.setDefault(True)
        primary_btn.setMinimumHeight(38)
        primary_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: {theme['custom_text'] if kind == 'critical' else '#FFFFFF'};
                border-radius: 9px;
                padding: 9px 18px;
                font-size: 13px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background-color: {primary_hover};
            }}
        """)
        primary_btn.clicked.connect(lambda: self._finish(primary_label))

        if len(buttons) > 1:
            # Two (or more) buttons: secondary on the left, primary on the right —
            # both sized to share the row evenly, mac-alert style.
            secondary_btn = QPushButton(buttons[0])
            secondary_btn.setObjectName("AlertSecondary")
            secondary_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            secondary_btn.setMinimumHeight(38)
            secondary_btn.clicked.connect(lambda: self._finish(buttons[0]))
            btn_row.addWidget(secondary_btn, 1)
            btn_row.addWidget(primary_btn, 1)
        else:
            # Single button: full width, matching macOS's single-action alert style.
            btn_row.addWidget(primary_btn, 1)

        root.addLayout(btn_row)
        self.setLayout(root)

    def _finish(self, text):
        self.result_text = text
        self.accept()

    @staticmethod
    def show(parent, theme, kind, title, message, buttons=("OK",)):
        dlg = MacMessageBox(parent, theme, kind, title, message, buttons)
        dlg.exec()
        return dlg.result_text


# ---------------------------------------------------------------------------
# Custom themed dialog for entering a custom probe domain
# ---------------------------------------------------------------------------

class ProbeDialog(QDialog):
    def __init__(self, parent, theme):
        super().__init__(parent)
        self.setObjectName("ProbeDialog")
        self.setWindowTitle("Set Custom Probe")
        self.setFixedSize(360, 180)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setAutoFillBackground(True)
        self.setStyleSheet(build_stylesheet(theme))

        layout = QVBoxLayout()
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(12)

        label = QLabel("Enter your probe domain")
        label.setObjectName("AlertTitle")
        layout.addWidget(label)

        hint = QLabel("Example: www.example.com")
        hint.setObjectName("SubtitleLabel")
        layout.addWidget(hint)

        self.input = QLineEdit()
        self.input.setPlaceholderText("www.example.com")
        layout.addWidget(self.input)

        layout.addStretch()

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("AlertSecondary")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setMinimumHeight(38)
        cancel_btn.clicked.connect(self.reject)

        ok_btn = QPushButton("Apply")
        ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ok_btn.setDefault(True)
        ok_btn.setMinimumHeight(38)
        ok_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme['success']};
                color: {theme['custom_text']};
                border-radius: 9px;
                padding: 9px 18px;
                font-size: 13px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background-color: {theme['success_hover']};
            }}
        """)
        ok_btn.clicked.connect(self.accept)

        btn_row.addWidget(cancel_btn, 1)
        btn_row.addWidget(ok_btn, 1)
        layout.addLayout(btn_row)

        self.setLayout(layout)

    def value(self):
        return self.input.text().strip()


# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------

class NCSITool(QWidget):
    def __init__(self):
        super().__init__()
        self.reg_path = r"SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet"
        self.current_theme_name = detect_system_theme()

        # Check if registry path exists
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.reg_path)
            winreg.CloseKey(key)
        except FileNotFoundError:
            MacMessageBox.show(self, THEMES[self.current_theme_name], "critical",
                                "Error", "Registry path not found!")
            sys.exit(1)

        self.init_ui()
        self.apply_theme(self.current_theme_name)
        self.refresh_status()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def init_ui(self):
        self.setWindowTitle("NCSI Network Connectivity Tool")
        self.setFixedSize(460, 560)

        icon_path = resource_path("icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        root = QVBoxLayout()
        root.setContentsMargins(24, 22, 24, 22)
        root.setSpacing(16)

        # ---- Header row: title + theme toggle ----
        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        title = QLabel("NCSI Connectivity Tool")
        title.setObjectName("TitleLabel")
        subtitle = QLabel("Manage Windows network connectivity probing")
        subtitle.setObjectName("SubtitleLabel")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        self.theme_btn = QPushButton("\U0001F319  Dark")
        self.theme_btn.setObjectName("ThemeBtn")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self.toggle_theme)

        header.addLayout(title_box)
        header.addStretch()
        header.addWidget(self.theme_btn, alignment=Qt.AlignmentFlag.AlignTop)
        root.addLayout(header)

        # ---- Status card ----
        self.status_card = QFrame()
        self.status_card.setObjectName("Card")

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(18, 16, 18, 8)
        card_layout.setSpacing(4)

        card_header = QHBoxLayout()
        card_title = QLabel("Current Status")
        card_title.setStyleSheet("font-size: 14px; font-weight: 700; background: transparent;")
        refresh_btn = QPushButton("\u27F3 Refresh")
        refresh_btn.setObjectName("RefreshBtn")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.clicked.connect(self.refresh_status)
        card_header.addWidget(card_title)
        card_header.addStretch()
        card_header.addWidget(refresh_btn)
        card_layout.addLayout(card_header)
        card_layout.addSpacing(6)

        self.status_labels = {}
        rows = [
            ("Active Probing", "EnableActiveProbing"),
            ("Poll Period", "PassivePollPeriod"),
            ("Probe Host", "ActiveWebProbeHost"),
            ("Probe Path", "ActiveWebProbePath"),
        ]
        for i, (display, key) in enumerate(rows):
            row_frame = QFrame()
            row_frame.setObjectName("StatusRowLast" if i == len(rows) - 1 else "StatusRow")
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(2, 10, 2, 10)
            row_layout.setSpacing(10)

            key_lbl = QLabel(display)
            key_lbl.setObjectName("StatusKey")

            val_lbl = QLabel("\u2014")
            val_lbl.setObjectName("StatusVal")
            val_lbl.setWordWrap(True)
            val_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            row_layout.addWidget(key_lbl, 1)
            row_layout.addWidget(val_lbl, 2)
            row_frame.setLayout(row_layout)

            card_layout.addWidget(row_frame)
            self.status_labels[key] = val_lbl

        self.status_card.setLayout(card_layout)
        root.addWidget(self.status_card)

        # ---- Action buttons ----
        actions_label = QLabel("Actions")
        actions_label.setStyleSheet("font-size: 13px; font-weight: 700;")
        root.addWidget(actions_label)

        self.disable_btn = QPushButton("\U0001F6AB  Disable NCSI")
        self.disable_btn.setObjectName("DisableBtn")
        self.disable_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.disable_btn.clicked.connect(self.disable_ncsi)
        root.addWidget(self.disable_btn)

        self.custom_btn = QPushButton("\U0001F310  Set Custom Probe")
        self.custom_btn.setObjectName("CustomBtn")
        self.custom_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.custom_btn.clicked.connect(self.set_custom_probe)
        root.addWidget(self.custom_btn)

        self.undo_btn = QPushButton("\u21BA  Restore Windows Default")
        self.undo_btn.setObjectName("UndoBtn")
        self.undo_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.undo_btn.clicked.connect(self.restore_default)
        root.addWidget(self.undo_btn)

        root.addStretch()

        # ---- Footer ----
        admin_state = "Running as Administrator" if is_admin() else "Limited mode — restart as Administrator to apply changes"
        footer = QLabel(admin_state)
        footer.setObjectName("FooterLabel")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(footer)

        self.setLayout(root)

    # ------------------------------------------------------------------
    # Theme handling
    # ------------------------------------------------------------------
    def apply_theme(self, name):
        self.current_theme_name = name
        t = THEMES[name]
        self.setStyleSheet(build_stylesheet(t))
        self.theme_btn.setText("\u2600  Light" if name == "dark" else "\U0001F319  Dark")

    def toggle_theme(self):
        new_theme = "dark" if self.current_theme_name == "light" else "light"
        self.apply_theme(new_theme)

    # ------------------------------------------------------------------
    # Registry helpers
    # ------------------------------------------------------------------
    def read_registry(self, key_name):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.reg_path)
            value, _ = winreg.QueryValueEx(key, key_name)
            winreg.CloseKey(key)
            return value
        except FileNotFoundError:
            return None

    def write_registry(self, key_name, value, value_type=winreg.REG_DWORD):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.reg_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, key_name, 0, value_type, value)
            winreg.CloseKey(key)
            return True
        except PermissionError:
            self.alert("critical", "Permission Error", "Access denied! Please run as Administrator.")
            return False
        except Exception as e:
            self.alert("critical", "Error", f"Failed to write registry: {str(e)}")
            return False

    def alert(self, kind, title, message, buttons=("OK",)):
        return MacMessageBox.show(self, THEMES[self.current_theme_name], kind, title, message, buttons)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def refresh_status(self):
        keys = ["EnableActiveProbing", "PassivePollPeriod", "ActiveWebProbeHost", "ActiveWebProbePath"]
        for key in keys:
            value = self.read_registry(key)
            display = "Not Set" if value is None else str(value)
            if key in self.status_labels:
                self.status_labels[key].setText(display)

    def disable_ncsi(self):
        if not is_admin():
            self.alert("warning", "Access Denied", "Please run as Administrator to modify settings.")
            return

        if self.write_registry("EnableActiveProbing", 0) and self.write_registry("PassivePollPeriod", 0):
            self.alert("info", "Done", "NCSI Disabled! Restart required.")
            self.refresh_status()
        else:
            self.alert("critical", "Failed", "Failed to disable NCSI.")

    def set_custom_probe(self):
        if not is_admin():
            self.alert("warning", "Access Denied", "Please run as Administrator to modify settings.")
            return

        dialog = ProbeDialog(self, THEMES[self.current_theme_name])
        if dialog.exec() == QDialog.DialogCode.Accepted:
            domain = dialog.value()
            if not domain:
                return
            if (self.write_registry("EnableActiveProbing", 1) and
                self.write_registry("ActiveWebProbeHost", domain, winreg.REG_SZ) and
                self.write_registry("ActiveWebProbePath", "/ncsi.txt", winreg.REG_SZ) and
                self.write_registry("ActiveWebProbeContent", "Microsoft Connect Test", winreg.REG_SZ)):
                self.alert("info", "Success", f"Probe changed to: {domain}. Restart required.")
                self.refresh_status()
            else:
                self.alert("critical", "Failed", "Failed to set custom probe.")

    def restore_default(self):
        if not is_admin():
            self.alert("warning", "Access Denied", "Please run as Administrator to modify settings.")
            return

        if (self.write_registry("EnableActiveProbing", 1) and
            self.write_registry("PassivePollPeriod", 120) and
            self.write_registry("ActiveWebProbeHost", "http://www.msftconnecttest.com/redirect", winreg.REG_SZ) and
            self.write_registry("ActiveWebProbePath", "/ncsi.txt", winreg.REG_SZ) and
            self.write_registry("ActiveWebProbeContent", "Microsoft Connect Test", winreg.REG_SZ)):
            self.alert("info", "Done", "Restored to default. Restart required.")
            self.refresh_status()
        else:
            self.alert("critical", "Failed", "Failed to restore defaults.")


def main():
    try:
        myappid = 'mycompany.myproduct.ncsitool.1.0'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))

    theme = THEMES[detect_system_theme()]

    if not is_admin():
        choice = MacMessageBox.show(
            None, theme, "question",
            "Administrator Required",
            "This tool requires administrator privileges to modify system settings. "
            "Do you want to run as administrator?",
            buttons=("Not now", "Run as Administrator")
        )

        if choice == "Run as Administrator":
            run_as_admin()
        else:
            window = NCSITool()
            window.show()
            sys.exit(app.exec())
    else:
        window = NCSITool()
        window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()