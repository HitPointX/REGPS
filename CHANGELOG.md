# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

### 0.0.1 (2025-06-23)

## [0.0.1] - Initial Pre-Release
### Added
- Implemented a GPS-style step tracker for Resident Evil HD Remaster (PC, Steam release).
- Overlay displays real-time step instructions with a typing effect.
- Text-to-Speech (TTS) reads each step aloud using the ElevenLabs API.
- Hotkey bindings:
  - `Z` or `L3+R3`: Advance to the next step.
  - `X`: Repeat the current step.
  - `Shift + Caps Lock + Q`: Toggle overlay visibility.
- Exit functionality by pressing the Escape key three times rapidly.
- Saves progress to `settings.json` for step resumption.
- Initial route included: Jill Valentine (Bad Ending).
- Game window tracking to dynamically position the overlay.

### Changed
- Updated from `ffplay` audio playback to `playsound` to eliminate console popups and simplify audio dependency.
- Switched from DLL extraction/cleanup model to a direct DLL load with a standalone directory for simplification and better antivirus compatibility.

### Fixed
- Corrected DLL loading issues to avoid Python runtime path errors.
- Resolved system errors when packaging with PyInstaller.
- Addressed antivirus false positives by transitioning the build process to Nuitka with MSVC.

### Build Process Improvements
- Migrated build process from PyInstaller to Nuitka for significantly fewer antivirus false positives.
- Updated to MSVC compilation with `--standalone` build structure.
- Migrated from PyQt5 to PyQt6 for better long-term support and Nuitka plugin compatibility.
- Added missing `pydantic.functional_serializers` dependency to ensure ElevenLabs API compatibility.
- Successfully tested onefile builds but reverted to standalone build for more reliable runtime behavior.

### Known Limitations
- Currently supports only the Steam release.
- Only one route (Jill Bad Ending) is implemented; additional routes to be added in future updates.
- Supports only Windows builds as of now.

---

Development will continue with additional routes and usability improvements in future updates.
