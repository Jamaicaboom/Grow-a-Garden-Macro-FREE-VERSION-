import time
import pyautogui
import keyboard

MACRO_SPEED = 0.1  # Default speed for reliable operation
macro_running = False

UI_NAV_KEY = '\\'  # UI Navigation toggle key


def set_macro_speed(new_speed):
    global MACRO_SPEED
    MACRO_SPEED = new_speed


def stop_macro():
    global macro_running
    macro_running = False


def fast_press(key, times=1):
    for _ in range(times):
        if not macro_running:
            return
        keyboard.press_and_release(key)
        time.sleep(MACRO_SPEED)


def scroll_mouse_up(amount=20):
    for _ in range(amount):
        if not macro_running:
            return
        pyautogui.scroll(200)
        time.sleep(min(MACRO_SPEED, 0.05))


def scroll_mouse_down(amount=8):
    for _ in range(amount):
        if not macro_running:
            return
        pyautogui.scroll(-200)
        time.sleep(min(MACRO_SPEED, 0.05))


def toggle_ui_navigation():
    if not macro_running:
        return
    keyboard.press_and_release(UI_NAV_KEY)
    time.sleep(0.15)


def setup_once_after_start():
    print("🔄 Starting macro setup...")

    scroll_mouse_up(20)      # Zoom in slowly
    scroll_mouse_down(8)     # Scroll down a bit
    toggle_ui_navigation()   # Toggle UI Nav on
    toggle_ui_navigation()   # Toggle UI Nav off

    # Recall Wrench equip steps removed — assume it's in slot 2 already

    print("🔧 Initial setup completed.")


def run_macro():
    global macro_running
    macro_running = True

    setup_once_after_start()
    print("✅ Macro is now running.")

    while macro_running:
        time.sleep(0.1)

    print("⏹ Macro stopped.")
