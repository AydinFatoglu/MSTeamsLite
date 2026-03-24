# MSTeamsLite

A lightweight Microsoft Teams launcher built for corporate VDI (Virtual Desktop Infrastructure) environments. Opens Teams directly inside a native window using the WebView2 (Edge/Chromium) engine — no separate Teams installation required.

---

## Features

- Embedded Microsoft Teams via WebView2 engine
- Automatic microphone, camera, and speaker permission handling
- System tray support — minimizes to tray instead of closing
- Persistent user session across launches
- Graceful fallback with error message if WebView2 Runtime is not found

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.8+ |
| wxPython | 4.2.2+ |
| WebView2 Runtime | Any |
| OS | Windows 10 / 11 |

> WebView2 Runtime comes pre-installed on Windows 11 and recent Windows 10 builds. No extra installation needed in most corporate environments.

---

## Installation

```bash
pip install wxPython
```

---

## Usage

```bash
python vdi_teams.py
```

### System Tray

| Action | Result |
|--------|--------|
| Click X button | Minimizes to tray |
| Double-click tray icon | Restores window |
| Right-click tray → Show | Restores window |
| Right-click tray → Close | Exits application |

---

## Building EXE

### 1. Find WebView2Loader.dll

```bash
python find_webview2loader.py
```

### 2. Build with PyInstaller

```bash
pyinstaller --noconfirm --onefile --windowed \
  --icon "your_icon.ico" \
  --add-data "path\to\WebView2Loader.dll;." \
  vdi_teams.py
```

> Use `--onefile` for a single executable. The resulting binary is approximately 12MB.

---

## How Permissions Work

On first launch, WebView2 displays a native browser permission popup for microphone and camera access. Once the user grants permission, the app writes the allow entries directly into the WebView2 `Preferences` file:

```
%LOCALAPPDATA%\vdi_teams\EBWebView\Default\Preferences
```

Permissions are written at three points:
- On application startup
- After the page finishes loading
- On application close

From the second launch onwards, no permission popup appears.

---

## Project Structure

```
vdi_teams/
├── vdi_teams.py            # Main application
├── find_webview2loader.py  # Utility to locate WebView2Loader.dll
└── README.md
```

---

## Technical Details

| Component | Detail |
|-----------|--------|
| GUI Framework | wxPython |
| Browser Engine | WebView2 (Edge/Chromium) |
| Session Storage | Isolated WebView2 profile under `%LOCALAPPDATA%\vdi_teams` |
| Permission Storage | JSON-based Preferences file |
| Tray Support | wx.adv.TaskBarIcon |

---

## License

Built for internal corporate use.
