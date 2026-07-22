import sys
import winreg
import ctypes
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, 
    QPushButton, QMessageBox, QInputDialog, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import os

def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
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
        QMessageBox.critical(None, "Error", f"Failed to run as administrator: {str(e)}")
        sys.exit(1)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class NCSITool(QWidget):
    def __init__(self):
        super().__init__()
        self.reg_path = r"SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet"
        
        # Check if registry path exists
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.reg_path)
            winreg.CloseKey(key)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Registry path not found!")
            sys.exit(1)

        self.init_ui()

    def init_ui(self):
        # Window setup
        self.setWindowTitle("NCSI Network Connectivity Tool")
        self.setFixedSize(450, 460)
        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel#TitleLabel {
                font-size: 20px;
                font-weight: bold;
                color: #FFFFFF;
                margin-bottom: 10px;
            }
            QPushButton {
                font-size: 14px;
                font-weight: 600;
                border-radius: 8px;
                padding: 12px;
                color: #FFFFFF;
                border: none;
            }
            QPushButton:hover {
                background-color: opacity(0.8);
            }
            QPushButton#StatusBtn {
                background-color: #FF9500;
            }
            QPushButton#StatusBtn:hover {
                background-color: #E08200;
            }
            QPushButton#DisableBtn {
                background-color: #FF3B30;
            }
            QPushButton#DisableBtn:hover {
                background-color: #D73229;
            }
            QPushButton#CustomBtn {
                background-color: #34C759;
                color: #000000;
            }
            QPushButton#CustomBtn:hover {
                background-color: #2DB04F;
            }
            QPushButton#UndoBtn {
                background-color: #0A84FF;
            }
            QPushButton#UndoBtn:hover {
                background-color: #006ADB;
            }
        """)

        # Main Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Title
        title = QLabel("NCSI Network Connectivity Tool")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Status Button
        self.status_btn = QPushButton("View Current Status")
        self.status_btn.setObjectName("StatusBtn")
        self.status_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.status_btn.clicked.connect(self.view_status)
        layout.addWidget(self.status_btn)

        # Disable Button
        self.disable_btn = QPushButton("Disable NCSI")
        self.disable_btn.setObjectName("DisableBtn")
        self.disable_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.disable_btn.clicked.connect(self.disable_ncsi)
        layout.addWidget(self.disable_btn)

        # Custom Probe Button
        self.custom_btn = QPushButton("Set Custom Probe")
        self.custom_btn.setObjectName("CustomBtn")
        self.custom_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.custom_btn.clicked.connect(self.set_custom_probe)
        layout.addWidget(self.custom_btn)

        # Undo Button
        self.undo_btn = QPushButton("Restore Windows Default")
        self.undo_btn.setObjectName("UndoBtn")
        self.undo_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.undo_btn.clicked.connect(self.restore_default)
        layout.addWidget(self.undo_btn)

        self.setLayout(layout)

    # --- Registry Helper Methods ---
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
            QMessageBox.critical(self, "Permission Error", "Access denied! Please run as Administrator.")
            return False
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to write registry: {str(e)}")
            return False

    # --- Button Logic Methods ---
    def view_status(self):
        try:
            keys = ["EnableActiveProbing", "PassivePollPeriod", "ActiveWebProbeHost", "ActiveWebProbePath"]
            values = {key: self.read_registry(key) or "Not Set" for key in keys}

            msg = (
                f"<b>EnableActiveProbing:</b> {values['EnableActiveProbing']}<br>"
                f"<b>PassivePollPeriod:</b> {values['PassivePollPeriod']}<br>"
                f"<b>ActiveWebProbeHost:</b> {values['ActiveWebProbeHost']}<br>"
                f"<b>ActiveWebProbePath:</b> {values['ActiveWebProbePath']}"
            )
            
            box = QMessageBox(self)
            box.setWindowTitle("Current Status")
            box.setTextFormat(Qt.TextFormat.RichText)
            box.setText(msg)
            box.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read status: {str(e)}")

    def disable_ncsi(self):
        if not is_admin():
            QMessageBox.warning(self, "Access Denied", "Please run as Administrator to modify settings.")
            return

        if self.write_registry("EnableActiveProbing", 0) and self.write_registry("PassivePollPeriod", 0):
            QMessageBox.information(self, "Done", "NCSI Disabled!\nRestart required.")
        else:
            QMessageBox.critical(self, "Failed", "Failed to disable NCSI.")

    def set_custom_probe(self):
        if not is_admin():
            QMessageBox.warning(self, "Access Denied", "Please run as Administrator to modify settings.")
            return

        domain, ok = QInputDialog.getText(self, "Custom Probe", "Enter your domain (e.g., www.google.com):")
        
        if ok and domain.strip():
            domain = domain.strip()
            if (self.write_registry("EnableActiveProbing", 1) and
                self.write_registry("ActiveWebProbeHost", domain, winreg.REG_SZ) and
                self.write_registry("ActiveWebProbePath", "/ncsi.txt", winreg.REG_SZ) and
                self.write_registry("ActiveWebProbeContent", "Microsoft Connect Test", winreg.REG_SZ)):
                QMessageBox.information(self, "Success", f"Probe changed to: {domain}\nRestart required.")
            else:
                QMessageBox.critical(self, "Failed", "Failed to set custom probe.")

    def restore_default(self):
        if not is_admin():
            QMessageBox.warning(self, "Access Denied", "Please run as Administrator to modify settings.")
            return

        if (self.write_registry("EnableActiveProbing", 1) and
            self.write_registry("PassivePollPeriod", 120) and
            self.write_registry("ActiveWebProbeHost", "http://www.msftconnecttest.com/redirect", winreg.REG_SZ) and
            self.write_registry("ActiveWebProbePath", "/ncsi.txt", winreg.REG_SZ) and
            self.write_registry("ActiveWebProbeContent", "Microsoft Connect Test", winreg.REG_SZ)):
            QMessageBox.information(self, "Done", "Restored to default.\nRestart required.")
        else:
            QMessageBox.critical(self, "Failed", "Failed to restore defaults.")

def main():
    try:
        myappid = 'mycompany.myproduct.ncsitool.1.0' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

    app = QApplication(sys.argv)

    # Check for admin rights
    if not is_admin():
        reply = QMessageBox.warning(
            None,
            "Administrator Required",
            "This tool requires administrator privileges to modify system settings.\n\n"
            "Do you want to run as administrator?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )

        if reply == QMessageBox.StandardButton.Yes:
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