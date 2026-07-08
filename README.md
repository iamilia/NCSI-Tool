# 🔧 NCSI Network Connectivity Tool

<div align="center">

![NCSI Tool Banner](https://img.shields.io/badge/Windows-NCSI%20Tool-blue?style=for-the-badge&logo=windows)
![Python](https://img.shields.io/badge/Python-3.6+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge)

**A beautiful, modern GUI tool to manage Windows NCSI settings**

[![Download](https://img.shields.io/badge/Download-EXE-blue?style=for-the-badge&logo=github)](https://github.com/iamilia/NCSI-Tool/releases)
[![Report Issue](https://img.shields.io/badge/Report%20Issue-GitHub-red?style=for-the-badge)](https://github.com/iamilia/NCSI-Tool/issues)

</div>

---

## 📖 Overview

**NCSI (Network Connectivity Status Indicator)** is a Windows service that checks internet connectivity by probing a Microsoft server. Sometimes, this causes issues in corporate networks, VPNs, or restricted environments. This tool allows you to:

- ✅ **View** current NCSI settings
- ❌ **Disable** NCSI (stops connectivity checks)
- ✏️ **Set a custom probe** (use your own domain for connectivity tests)
- ↩️ **Restore** Windows default settings

---

## ✨ Features

| Feature                    | Description                                             |
| -------------------------- | ------------------------------------------------------- |
| 🔧 **Registry Management** | Safely read/write NCSI registry keys                    |
| 🛡️ **Admin Check**         | Automatically prompts for administrator privileges      |
| 📊 **Status Viewer**       | View all current NCSI settings in one dialog            |
| ⚡ **Fast & Lightweight**  | No external dependencies (only Python standard library) |
| 🖱️ **CLI Support**         | Use command-line arguments for automation               |

## 🚀 Installation

### Option 1: Download EXE (Recommended)

1. Go to [Releases](https://github.com/yourusername/NCSI-Tool/releases)
2. Download `NCSI-Tool.exe`
3. Run it (no installation required)

### Option 2: Run from Source

```bash
git clone https://github.com/iamilia/NCSI-Tool.git
cd NCSI-Tool
python ncsi_tool.py
```