import json
from fuzzywuzzy import fuzz
import ctypes
import locale


def equ(text, needed, threshold=65):
    return fuzz.ratio(text, needed) >= threshold


# Загрузка ответов из JSON
def read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Не удалось загрузить responses.json: {e}")
        return {}


def get_keyboard_language():
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    hwnd = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(hwnd, 0)
    layout_id = user32.GetKeyboardLayout(thread_id)
    language_id = layout_id & (2**16 - 1)  # младшие 16 бит

    lang = locale.windows_locale.get(language_id, "unknown")
    return lang


