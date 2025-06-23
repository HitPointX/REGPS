
# BUILD.md - REGPS Build Instructions

## Overview
This document provides step-by-step instructions for building **REGPS** using **Nuitka** with Python 3.13 and the Microsoft Visual C++ (MSVC) toolchain.

REGPS is a GPS-style navigation overlay for **Resident Evil HD Remaster (PC - Steam version)** with step-by-step text and Text-to-Speech (TTS) guidance.

Currently, the project supports the **Jill Bad Ending Route**. Additional routes will be added in future updates.

---

## Requirements

### Python
- **Python 3.13.x**

> Nuitka does not currently support MinGW for Python 3.13 builds. You **must** use the MSVC toolchain with `--msvc=latest` for Python 3.13 compatibility.

### Required Software
- **Microsoft Visual Studio Build Tools** with the following components:
  - Desktop development with C++
  - Windows 10 SDK (or Windows 11 SDK)
  - MSVC v143 or later
  - C++ CMake tools for Windows (recommended)

- **Nuitka** (installed via pip)

### Required Python Packages
Install these packages in your Python environment:
```bash
pip install nuitka
pip install pyqt6
pip install pynput
pip install pygetwindow
pip install playsound
pip install pythonnet
pip install elevenlabs
pip install pydantic
```

---

## Build Commands

### Onefile Build Command (Recommended if Working)
```bash
nuitka --onefile ^
--windows-console-mode=disable ^
--enable-plugin=pyqt6 ^
--enable-plugin=pylint-warnings ^
--include-module=pydantic.functional_serializers ^
--include-data-files="ControllerStepTrigger.dll=ControllerStepTrigger.dll" ^
--follow-imports ^
--show-progress ^
--msvc=latest ^
--windows-icon-from-ico=icon.ico ^
--output-filename=REGPS.exe ^
step_tracker_with_dll_final.py
```

### Standalone (Onedir) Build Command (Fallback if Onefile Fails)
```bash
nuitka --standalone ^
--windows-console-mode=disable ^
--enable-plugin=pyqt6 ^
--enable-plugin=pylint-warnings ^
--include-module=pydantic.functional_serializers ^
--include-data-files="ControllerStepTrigger.dll=ControllerStepTrigger.dll" ^
--follow-imports ^
--show-progress ^
--msvc=latest ^
--windows-icon-from-ico=icon.ico ^
--output-filename=REGPS.exe ^
step_tracker_with_dll_final.py
```

---

## Build Flag Explanation

| Flag | Purpose |
|------|---------|
| `--onefile` | Produces a single executable file. |
| `--standalone` | Creates a folder-based build with all dependencies. |
| `--windows-console-mode=disable` | Hides the console window (for GUI apps). |
| `--enable-plugin=pyqt6` | Enables Nuitka support for PyQt6. |
| `--enable-plugin=pylint-warnings` | Optional: Improves import scanning reliability. |
| `--include-module=pydantic.functional_serializers` | Ensures ElevenLabs API dependency is included. |
| `--include-data-files="ControllerStepTrigger.dll=ControllerStepTrigger.dll"` | Adds the controller DLL to the final build directory. |
| `--follow-imports` | Ensures all imports are bundled. |
| `--show-progress` | Displays detailed build progress. |
| `--msvc=latest` | Forces use of MSVC (required for Python 3.13). |
| `--windows-icon-from-ico=icon.ico` | Applies a custom executable icon. |
| `--output-filename=REGPS.exe` | Names the final executable. |

---

## Build Process Notes
- The build process may take **several minutes** due to Nuitka's C++ compilation and optimization steps.
- False positives in VirusTotal are significantly reduced using Nuitka compared to PyInstaller.
- Python 3.13 **requires** the MSVC toolchain. MinGW is not supported for this version (as of writing).
- The onefile build is preferred if functional. Use the standalone fallback if the onefile build has issues.

---

## Distribution Guidelines

### Onefile Build
- Distribute the single `REGPS.exe` file.

### Standalone Build
- Distribute the **entire build folder**.
- The executable and DLL must remain in the same folder structure.

### Recommended Files for Distribution
- `REGPS.exe`
- `ControllerStepTrigger.dll`
- `README.md`
- `BUILD.md`

---

## Additional Notes
- The application is currently **only tested on the Steam release** of Resident Evil HD Remaster.
- Hotkeys:
  - `Z` or `L3+R3`: Advance to next step
  - `X`: Repeat current step
  - `Shift + Caps Lock + Q`: Toggle overlay visibility
  - Triple `Escape`: Exit program
- Additional route support will be added in future updates.

---

## Optional Files

### .gitignore
```text
# Byte-compiled files
__pycache__/
*.py[cod]

# Distribution folders
build/
dist/
*.spec

# Temporary files
*.tmp
*.log

# Python virtual environments
venv/
.env/

# Nuitka cache
.nuitka-cache/

# System files
Thumbs.db
.DS_Store

# Settings and personal files
settings.json
```

### LICENSE 
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
