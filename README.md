# 🔧 NCSI Network Connectivity Tool v2.0.0

<div align="center">

![NCSI Tool Banner](https://img.shields.io/badge/Windows-NCSI%20Tool-blue?style=for-the-badge&logo=windows)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?style=for-the-badge&logo=qt)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)

**A modern, powerful PyQt6-based GUI tool to manage Windows NCSI settings**

[![Download](https://img.shields.io/badge/Download-v2.0.0-blue?style=for-the-badge&logo=github)](https://github.com/iamilia/NCSI-Tool/releases)
[![Report Issue](https://img.shields.io/badge/Report%20Issue-GitHub-red?style=for-the-badge)](https://github.com/iamilia/NCSI-Tool/issues)

</div>

---

## 📖 Overview

**NCSI (Network Connectivity Status Indicator)** is a Windows service that checks internet connectivity by probing Microsoft servers. In corporate networks, VPNs, or restricted environments, NCSI can often incorrectly flag networks as "No Internet Connection". 

**NCSI Tool v2.0** provides a sleek, modern interface to view, customize, or disable Windows network connectivity probing seamlessly.

---

## ✨ Features in v2.0

| Feature | Description |
| :--- | :--- |
| 🎨 **Modern PyQt6 UI** | Completely rewritten UI using PyQt6, replacing the legacy Tkinter engine. |
| 🌓 **Adaptive Themes** | Built-in Light and Dark themes with automatic Windows theme detection & toggle button. |
| 📊 **Live Status Dashboard** | Embedded live registry status card with instant refresh capability. |
| 🍎 **Mac-style Dialogs** | Replaced default system alerts with custom, beautifully designed modal dialogs. |
| 🔧 **Registry Management** | Safely read and update NCSI registry entries (`EnableActiveProbing`, `ProbeHost`, etc.). |
| 🛡️ **Admin Privilege Helper** | Auto-detects administrator rights and prompts for elevated privilege execution. |

---

## 🚀 Quick Start

### Option 1: Executable File (Recommended)
1. Head over to the [Releases](https://github.com/iamilia/NCSI-Tool/releases) page.
2. Download `NCSI-Tool.exe`.
3. Launch the application (Runs directly, no setup required).

### Option 2: Run from Source

**Prerequisites:**
- Python 3.8+
- PyQt6

```bash
# Clone repository
git clone https://github.com/iamilia/NCSI-Tool.git
cd NCSI-Tool

# Install dependencies
pip install PyQt6

# Run application
python NCSI-Tool.py
```
