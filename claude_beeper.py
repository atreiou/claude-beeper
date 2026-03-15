# ============================================================
# 1. SECTION: Imports and Constants
# ============================================================

# 1.1 Standard library imports
import sys
import ctypes
import winsound
import threading

# 1.2 pywin32 imports
import win32gui
import win32con
import win32api

# 1.3 Tray icon imports
import pystray
from PIL import Image, ImageDraw

# 1.4 Shell hook constant
HSHELL_FLASH = 0x8006

# 1.5 Register the SHELLHOOK window message
WM_SHELLHOOK = win32gui.RegisterWindowMessage("SHELLHOOK")

# 1.6 User32 reference
user32 = ctypes.windll.user32

# 1.7 Global state flags
_paused = False
_cached_claude_hwnd = None

# end of 1. SECTION: Imports and Constants


# ============================================================
# 2. SECTION: Tray Icon Image Generation
# ============================================================

# 2.1 Generate the active (unpaused) tray icon
def make_icon_active():

    # 2.1.1 Create base image
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 2.1.2 Draw filled circle background
    draw.ellipse([2, 2, 62, 62], fill=(80, 140, 255, 255))

    # 2.1.3 Draw bell body (rounded rectangle)
    draw.rounded_rectangle([18, 20, 46, 44], radius=6, fill=(255, 255, 255, 255))

    # 2.1.4 Draw bell top arc
    draw.ellipse([20, 14, 44, 30], fill=(255, 255, 255, 255))

    # 2.1.5 Draw bell clapper
    draw.ellipse([27, 42, 37, 52], fill=(255, 255, 255, 255))

    # 2.1.6 Return finished image
    return img

# end of 2.1

# 2.2 Generate the paused tray icon (greyed out)
def make_icon_paused():

    # 2.2.1 Create base image
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 2.2.2 Draw filled circle background (grey)
    draw.ellipse([2, 2, 62, 62], fill=(120, 120, 120, 255))

    # 2.2.3 Draw two pause bars
    draw.rectangle([18, 18, 28, 46], fill=(255, 255, 255, 255))
    draw.rectangle([36, 18, 46, 46], fill=(255, 255, 255, 255))

    # 2.2.4 Return finished image
    return img

# end of 2.2
# end of 2. SECTION: Tray Icon Image Generation


# ============================================================
# 3. SECTION: Window Discovery
# ============================================================

# 3.1 Find Claude app window handle
def find_claude_hwnd():

    # 3.1.1 Declare global cache reference
    global _cached_claude_hwnd

    # 3.1.2 Return cached handle if still valid
    if _cached_claude_hwnd and win32gui.IsWindow(_cached_claude_hwnd):
        return _cached_claude_hwnd

    # 3.1.3 Collect matching windows via enumeration
    matches = []

    # 3.1.4 Define enum callback
    def callback(hwnd, _):

        # 3.1.4.1 Skip invisible windows
        if not win32gui.IsWindowVisible(hwnd):
            return

        # 3.1.4.2 Match on window title containing 'claude'
        title = win32gui.GetWindowText(hwnd)
        if 'claude' in title.lower():
            matches.append(hwnd)

    # end of 3.1.4

    # 3.1.5 Run enumeration
    win32gui.EnumWindows(callback, None)

    # 3.1.6 Cache and return first match, or None
    _cached_claude_hwnd = matches[0] if matches else None
    return _cached_claude_hwnd

# end of 3.1
# end of 3. SECTION: Window Discovery


# ============================================================
# 4. SECTION: Shell Hook Message Handler
# ============================================================

# 4.1 Window procedure for the hidden message window
def wnd_proc(hwnd, msg, wParam, lParam):

    # 4.1.1 Handle shell hook messages only
    if msg == WM_SHELLHOOK:

        # 4.1.1.1 Check for taskbar flash event
        if wParam == HSHELL_FLASH:

            # 4.1.1.1.1 Skip if paused
            if not _paused:

                # 4.1.1.1.1.1 Look up Claude's window handle
                claude_hwnd = find_claude_hwnd()

                # 4.1.1.1.1.2 Beep if the flashing window is Claude
                if claude_hwnd and lParam == claude_hwnd:
                    winsound.Beep(1000, 400)

                # end of 4.1.1.1.1.2

            # end of 4.1.1.1.1

        # end of 4.1.1.1

    # end of 4.1.1

    # 4.1.2 Pass all other messages to default handler
    return win32gui.DefWindowProc(hwnd, msg, wParam, lParam)

# end of 4.1
# end of 4. SECTION: Shell Hook Message Handler


# ============================================================
# 5. SECTION: Hidden Window and Message Loop
# ============================================================

# 5.1 Global handle for the message window
_msg_hwnd = None

# 5.2 Create and run the hidden message window on its own thread
def run_message_loop():

    # 5.2.1 Declare global handle reference
    global _msg_hwnd

    # 5.2.2 Define the window class
    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc   = wnd_proc
    wc.lpszClassName = "ClaudeBeeper"
    wc.hInstance     = win32api.GetModuleHandle(None)

    # 5.2.3 Register the window class
    win32gui.RegisterClass(wc)

    # 5.2.4 Create a message-only window (no taskbar presence)
    _msg_hwnd = win32gui.CreateWindow(
        wc.lpszClassName,
        "Claude Beeper",
        0, 0, 0, 0, 0,
        win32con.HWND_MESSAGE,
        0,
        wc.hInstance,
        None
    )

    # 5.2.5 Register as a shell hook window
    user32.RegisterShellHookWindow(_msg_hwnd)

    # 5.2.6 Run the Windows message loop until quit
    win32gui.PumpMessages()

    # 5.2.7 Clean up on exit
    user32.DeregisterShellHookWindow(_msg_hwnd)
    win32gui.DestroyWindow(_msg_hwnd)

# end of 5.2
# end of 5. SECTION: Hidden Window and Message Loop


# ============================================================
# 6. SECTION: Tray Icon and Menu
# ============================================================

# 6.1 Toggle paused state
def on_pause(icon, item):

    # 6.1.1 Declare global paused reference
    global _paused

    # 6.1.2 Flip the paused flag
    _paused = not _paused

    # 6.1.3 Swap the icon image to reflect state
    icon.icon = make_icon_paused() if _paused else make_icon_active()

    # 6.1.4 Update the icon tooltip
    icon.title = "Claude Beeper (Paused)" if _paused else "Claude Beeper"

# end of 6.1

# 6.2 Quit the application
def on_quit(icon, item):

    # 6.2.1 Stop the tray icon loop
    icon.stop()

    # 6.2.2 Post quit message to the hidden window's message loop
    if _msg_hwnd:
        win32gui.PostMessage(_msg_hwnd, win32con.WM_QUIT, 0, 0)

# end of 6.2

# 6.3 Return the dynamic pause menu label
def pause_label(item):

    # 6.3.1 Return label based on current paused state
    return "Resume" if _paused else "Pause"

# end of 6.3

# 6.4 Build and run the system tray icon
def run_tray():

    # 6.4.1 Build the context menu
    menu = pystray.Menu(
        pystray.MenuItem(pause_label, on_pause),
        pystray.MenuItem("Quit", on_quit)
    )

    # 6.4.2 Create the tray icon
    icon = pystray.Icon(
        "ClaudeBeeper",
        make_icon_active(),
        "Claude Beeper",
        menu
    )

    # 6.4.3 Run the tray icon (blocks until stop() is called)
    icon.run()

# end of 6.4
# end of 6. SECTION: Tray Icon and Menu


# ============================================================
# 7. SECTION: Main Entry Point
# ============================================================

# 7.1 Start message loop thread and tray icon
def main():

    # 7.1.1 Start the shell hook listener on a background thread
    msg_thread = threading.Thread(target=run_message_loop, daemon=True)
    msg_thread.start()

    # 7.1.2 Run the tray icon on the main thread (required by pystray)
    run_tray()

# end of 7.1

# 7.2 Script entry guard
if __name__ == "__main__":
    main()

# end of 7.2
# end of 7. SECTION: Main Entry Point