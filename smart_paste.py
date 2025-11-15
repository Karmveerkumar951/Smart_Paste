import time
import threading
from math import hypot
from pynput import mouse, keyboard
import pyperclip

# Config
DOUBLE_CLICK_MAX_INTERVAL = 0.35   # seconds
DOUBLE_CLICK_MAX_DISTANCE = 6      # pixels
SHORT_SLEEP_AFTER_COPY = 0.06      # seconds to let clipboard update

kb = keyboard.Controller()

# State
_last_click_time = 0.0
_last_click_pos = (0, 0)
_last_click_button = None
_state_lock = threading.Lock()
shutdown_event = threading.Event()

def send_ctrl_c():
    kb.press(keyboard.Key.ctrl)
    kb.press('c')
    kb.release('c')
    kb.release(keyboard.Key.ctrl)

def send_ctrl_v():
    kb.press(keyboard.Key.ctrl)
    kb.press('v')
    kb.release('v')
    kb.release(keyboard.Key.ctrl)

def try_auto_copy():
    """Attempt to copy selection by sending Ctrl+C, but only update if clipboard changes."""
    try:
        before = pyperclip.paste()
    except Exception:
        before = None

    send_ctrl_c()
    time.sleep(SHORT_SLEEP_AFTER_COPY)

    try:
        after = pyperclip.paste()
    except Exception:
        after = None

    if after != before:
        # clipboard updated; consider it a successful auto-copy
        print(f"[AUTO-COPY] clipboard updated ({len(str(after or ''))} chars).")
    else:
        # nothing changed; likely no selection
        # print("[AUTO-COPY] nothing copied.")
        pass

def on_click(x, y, button, pressed):
    """Mouse click callback."""
    global _last_click_time, _last_click_pos, _last_click_button

    # only care about left button release
    if button != mouse.Button.left or pressed:
        return

    now = time.time()
    with _state_lock:
        dx = x - _last_click_pos[0]
        dy = y - _last_click_pos[1]
        dist = hypot(dx, dy)
        interval = now - _last_click_time

        is_double = (
            _last_click_button == button and
            interval <= DOUBLE_CLICK_MAX_INTERVAL and
            dist <= DOUBLE_CLICK_MAX_DISTANCE
        )

        # update last-click info
        _last_click_time = now
        _last_click_pos = (x, y)
        _last_click_button = button

    if is_double:
        print(f"[DOUBLE-CLICK] at ({x},{y}) — performing paste.")
        # small delay to ensure caret/selection is in place
        time.sleep(0.02)
        send_ctrl_v()
    else:
        # Run auto-copy in a short background thread so listener isn't blocked
        t = threading.Thread(target=try_auto_copy, daemon=True)
        t.start()

def on_activate_stop():
    """Hotkey handler to request shutdown."""
    print("\n[HOTKEY] Ctrl+Shift+S pressed — stopping...")
    shutdown_event.set()

def main():
    print("Auto Copy/Paste running.")
    print(" - Selecting text then releasing left button will auto-copy it.")
    print(" - Double-clicking left button will auto-paste.")
    print("Stop: press Ctrl+C in this terminal, or press Ctrl+Shift+S.\n")

    # Create listeners
    mouse_listener = mouse.Listener(on_click=on_click)
    hotkey = keyboard.GlobalHotKeys({
        '<ctrl>+<shift>+s': on_activate_stop
    })

    # Start listeners
    mouse_listener.start()
    hotkey.start()

    try:
        # Main loop: wait for shutdown_event (set by Ctrl+C or hotkey)
        while not shutdown_event.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n[KeyboardInterrupt] Stopping...")
        shutdown_event.set()
    finally:
        # stop listeners and wait for them to finish
        if mouse_listener.running:
            mouse_listener.stop()
        try:
            hotkey.stop()
        except Exception:
            # some versions might already be stopped
            pass

        mouse_listener.join()
        # GlobalHotKeys has no join method, but stop() should end it.
        print("Stopped cleanly.")

if __name__ == "__main__":
    main()
