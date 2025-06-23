# REGPS - Resident Evil GPS (Speedrun Step Tracker)

![REGPS Logo](icon.png)

## Project Overview
**REGPS (Resident Evil GPS)** is a real-time, GPS-style speedrun step tracker designed specifically for **Resident Evil HD Remaster (PC version).**

The program displays **text overlays** and provides **text-to-speech (TTS) step-by-step navigation** to guide players through speedrun routes, similar to how a GPS guides drivers.

**Note:** This has currently only been tested with the **Steam release** of Resident Evil HD Remaster. Compatibility with other versions is untested.

Currently, the program fully supports the **Jill Valentine - Bad Ending Route.** Additional routes and characters will be added in future updates.

---

## Features
- Real-Time Overlay: Displays the current step with a smooth typing effect.
- Text-to-Speech Guidance: Reads each step aloud for hands-free navigation.
- Controller & Keyboard Support: Advance steps using keyboard or controller inputs.
- Overlay Toggle: Hide or show the overlay with a keybind.
- Auto-Save Progress: Saves your current step and resumes it on restart.
- GPS-style Navigation: Move sequentially through steps or repeat the last one.

---

## How to Use

### 1. Run the Program
Extract the provided ZIP and run `REGPS.exe` from the extracted folder.  
Important: Do not move the `REGPS.exe` outside of its folder. It relies on the included files and DLLs to function properly.

---

### 2. Keybinds

| Action | Keybind |
|--------|---------|
| Advance to Next Step | `Z` (keyboard) or `L3 + R3` (controller) |
| Repeat Current Step | `X` |
| Toggle Overlay Visibility | `Shift + Caps Lock + Q` |
| Exit Program | Press `Escape` 3 times quickly |

---

### 3. Requirements
- Resident Evil HD Remaster (PC)  
  **Tested only on the Steam release.**
- Audio device for TTS playback
- Windows OS

---

### 4. Supported Routes
- Jill Valentine - Bad Ending

More routes (Chris, Jill Good Ending, etc.) coming soon.

---

## File Structure

REGPS/
├── REGPS.exe
├── ControllerStepTrigger.dll
├── icon.ico
├── settings.json (auto-generated)
├── [PyQt6 and dependency DLLs]


---

## Building Instructions

See [BUILD.md](BUILD.md) for the exact Nuitka build command and dependency setup.

---

## Future Plans
- Add support for Chris Redfield routes.
- Implement Jill Good Ending route.
- Add optional step sound effects and TTS voice selection.
- Build a step editor for custom route creation.

---

## Credits
- Developed by HitPoint
- Powered by ElevenLabs for TTS
- Built with Python, PyQt6, Nuitka

---

## Feedback & Contributions
If you'd like to contribute, suggest features, or report bugs, feel free to open an issue or submit a pull request.

---

This project is designed to assist speedrunners and players in navigating Resident Evil HD Remaster efficiently. It is not affiliated with or endorsed by Capcom.
