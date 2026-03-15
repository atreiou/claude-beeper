# Claude Beeper

**Never miss a Claude Code response again.**

A tiny Windows system tray app that beeps when Claude Code's desktop app flashes in the taskbar — so you can afk without constantly checking if Claude is done.

## The Problem

Claude Code (desktop app) flashes its taskbar icon when it has a response ready, but there's no sound. If you're afk, you have to keep glancing over at the computer's taskbar to see if Claude is done. This is annoying.

## The Solution

Claude Beeper sits in your system tray and watches for Claude Code's taskbar flash. When it detects one, it plays a short beep (1000Hz, 400ms). That's it. Simple.

## Installation

### From Source

**Requirements:** Python 3.8+, Windows 10/11

```bash
pip install pystray pillow pywin32
python claude_beeper.py
```

### Build Executable

```bash
pip install pyinstaller
python create_icon.py
build.bat
```

The executable will be in `dist/ClaudeBeeper.exe`.

### Auto-Start with Windows

Run `install.bat` as Administrator — it copies the executable to Program Files and adds it to Windows startup.

## Usage

- **Launch:** Double-click `ClaudeBeeper.exe` or run `python claude_beeper.py`
- **Pause/Resume:** Right-click tray icon → Pause/Resume
- **Quit:** Right-click tray icon → Quit

The tray icon is a blue circle with a bell when active, grey with pause bars when paused.

## How It Works

1. Registers a Windows Shell Hook to receive `HSHELL_FLASH` messages
2. Finds the Claude Code window by searching for windows with "claude" in the title
3. When the flashing window matches Claude's handle, plays a beep via `winsound.Beep()`
4. Caches the window handle for performance — re-discovers if the window closes and reopens

## Dependencies

- `pystray` — system tray icon
- `Pillow` — icon image generation
- `pywin32` — Windows API access (shell hooks, window enumeration)

## License

MIT
