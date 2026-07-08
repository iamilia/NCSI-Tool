import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import winreg
import sys
import ctypes

def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Relaunch the script with administrator privileges"""
    try:
        # Get the current script path
        script_path = sys.argv[0]
        
        # If running as .py file, run with python
        if script_path.endswith('.py'):
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script_path}"', None, 1
            )
        # If running as .exe file, run directly
        else:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", script_path, "", None, 1
            )
        sys.exit()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run as administrator: {str(e)}")
        sys.exit(1)

class NCSITool:
    def __init__(self, root):
        self.root = root
        self.root.title("NCSI Network Connectivity Tool")
        self.root.geometry("420x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")
        
        # Registry path
        self.reg_path = r"SYSTEM\CurrentControlSet\Services\NlaSvc\Parameters\Internet"
        
        # Check if registry path exists
        try:
            winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.reg_path)
        except FileNotFoundError:
            messagebox.showerror("Error", "Registry path not found!")
            sys.exit(1)
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(main_frame, text="NCSI Network Connectivity Tool", 
                        font=("Segoe UI", 20), fg="white", bg="#1e1e1e")
        title.pack(pady=(0, 20))
        
        
        # Style for buttons
        button_style = {
            "height": 2,
            "font": ("Segoe UI", 12),
            "relief": tk.FLAT,
            "borderwidth": 0,
            "cursor": "hand2"
        }
        
        # Status Button
        self.status_btn = tk.Button(main_frame, text="View Current Status", 
                                   bg="#ff9500", fg="white",
                                   command=self.view_status, **button_style)
        self.status_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Disable Button
        self.disable_btn = tk.Button(main_frame, text="Disable NCSI", 
                                    bg="#ff3b30", fg="white",
                                    command=self.disable_ncsi, **button_style)
        self.disable_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Custom Button
        self.custom_btn = tk.Button(main_frame, text="Set Custom Probe", 
                                   bg="#34c759", fg="black",
                                   command=self.set_custom_probe, **button_style)
        self.custom_btn.pack(fill=tk.X, pady=(0, 10))
        
        # Undo Button
        self.undo_btn = tk.Button(main_frame, text="Restore Windows Default", 
                                 bg="#0a84ff", fg="white",
                                 command=self.restore_default, **button_style)
        self.undo_btn.pack(fill=tk.X)
        
    def read_registry(self, key_name):
        """Read a registry value"""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.reg_path)
            value, _ = winreg.QueryValueEx(key, key_name)
            winreg.CloseKey(key)
            return value
        except FileNotFoundError:
            return None
    
    def write_registry(self, key_name, value, value_type=winreg.REG_DWORD):
        """Write a registry value"""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, self.reg_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, key_name, 0, value_type, value)
            winreg.CloseKey(key)
            return True
        except PermissionError:
            messagebox.showerror("Permission Error", 
                               "Access denied! Please run as Administrator.")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to write registry: {str(e)}")
            return False
    
    def view_status(self):
        """View current NCSI status"""
        try:
            values = {}
            keys = ["EnableActiveProbing", "PassivePollPeriod", "ActiveWebProbeHost", "ActiveWebProbePath"]
            
            for key in keys:
                val = self.read_registry(key)
                if val is not None:
                    values[key] = val
                else:
                    values[key] = "Not Set"
            
            msg = "Current NCSI Settings:\n\n"
            msg += f"EnableActiveProbing: {values.get('EnableActiveProbing', 'N/A')}\n"
            msg += f"PassivePollPeriod: {values.get('PassivePollPeriod', 'N/A')}\n"
            msg += f"ActiveWebProbeHost: {values.get('ActiveWebProbeHost', 'N/A')}\n"
            msg += f"ActiveWebProbePath: {values.get('ActiveWebProbePath', 'N/A')}"
            
            messagebox.showinfo("Current Status", msg)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read status: {str(e)}")
    
    def disable_ncsi(self):
        """Disable NCSI"""
        if not is_admin():
            messagebox.showerror("Access Denied", 
                               "Please run as Administrator to modify settings.")
            return
            
        try:
            if self.write_registry("EnableActiveProbing", 0) and \
               self.write_registry("PassivePollPeriod", 0):
                messagebox.showinfo("Done", "NCSI Disabled!\nRestart required.")
            else:
                messagebox.showerror("Failed", "Failed to disable NCSI.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def set_custom_probe(self):
        """Set custom probe domain"""
        if not is_admin():
            messagebox.showerror("Access Denied", 
                               "Please run as Administrator to modify settings.")
            return
            
        domain = simpledialog.askstring("Custom Probe", 
                                       "Enter your domain (e.g., www.google.com):",
                                       parent=self.root)
        
        if domain and domain.strip():
            domain = domain.strip()
            try:
                if self.write_registry("EnableActiveProbing", 1) and \
                   self.write_registry("ActiveWebProbeHost", domain, winreg.REG_SZ) and \
                   self.write_registry("ActiveWebProbePath", "/ncsi.txt", winreg.REG_SZ) and \
                   self.write_registry("ActiveWebProbeContent", "Microsoft Connect Test", winreg.REG_SZ):
                    messagebox.showinfo("Success", f"Probe changed to: {domain}\nRestart required.")
                else:
                    messagebox.showerror("Failed", "Failed to set custom probe.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def restore_default(self):
        """Restore Windows default settings"""
        if not is_admin():
            messagebox.showerror("Access Denied", 
                               "Please run as Administrator to modify settings.")
            return
            
        try:
            if self.write_registry("EnableActiveProbing", 1) and \
               self.write_registry("PassivePollPeriod", 120) and \
               self.write_registry("ActiveWebProbeHost", "http://www.msftconnecttest.com/redirect", winreg.REG_SZ) and \
               self.write_registry("ActiveWebProbePath", "/ncsi.txt", winreg.REG_SZ) and \
               self.write_registry("ActiveWebProbeContent", "Microsoft Connect Test", winreg.REG_SZ):
                messagebox.showinfo("Done", "Restored to default.\nRestart required.")
            else:
                messagebox.showerror("Failed", "Failed to restore defaults.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    # Check for admin rights
    if not is_admin():
        # Ask user if they want to run as administrator
        response = messagebox.askyesno(
            "Administrator Required",
            "This tool requires administrator privileges to modify system settings.\n\n"
            "Do you want to run as administrator?",
            icon='warning'
        )
        if response:
            run_as_admin()
        else:
            # Run without admin (but show limited functionality)
            root = tk.Tk()
            app = NCSITool(root)
            # Show warning in the interface
            root.mainloop()
    else:
        # Run normally with admin rights
        root = tk.Tk()
        app = NCSITool(root)
        root.mainloop()

if __name__ == "__main__":
    main()