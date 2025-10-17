# github.com/kripersi , tg: @Marpexiz
import os
import winshell
import subprocess
import time
import pygetwindow as gw
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from config import *
import keyboard
import webbrowser
import urllib.parse
import datetime

from assistant.utils import get_keyboard_language
from assistant.speaker import speak


def open_app(app_name):
    apps = {
        "телеграм": TELEGRAM_PATH,
        "браузер": BROWSER_PATH,
        "блокнот": NOTEPAD_PATH,
        "проводник": EXPLORER_PATH,
        "диспетчер задач": TASKMGR_PATH,
        "youtube": "YOUTUBE"
    }
    path = apps.get(app_name)

    if path == "YOUTUBE":
        open_youtube()
    elif path:
        subprocess.Popen(path)
        speak(f"Открываю {app_name}")
    else:
        speak(f"Приложение {app_name} не найдено")


def close_active_window():
    try:
        win = gw.getActiveWindow()
        if win:
            win.close()
            speak(f"Закрываю окно: {win.title}")
        else:
            speak("Не удалось определить активное окно")
    except Exception:
        speak("Ошибка при закрытии активного окна")


def open_youtube():
    try:
        webbrowser.open("https://www.youtube.com")
        speak("Открываю YouTube")
    except Exception:
        speak("Не удалось открыть YouTube")


def clear_trash():
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
        speak("Корзина успешно очищена.")
    except Exception as e:
        speak(f"Ошибка при очистке корзины: {e}")


def focus_search_field():
    try:
        pyautogui.press('/')  # фокус на адресной строке
        time.sleep(0.2)
        speak("Поле поиска активировано")
    except Exception:
        speak("Не удалось переключиться на поле ввода")


def set_volume(command):
    try:
        # Получаем интерфейс управления громкостью
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        current = volume.GetMasterVolumeLevelScalar()

        # Выключение звука
        if any(phrase in command for phrase in ["выключи", "без звука", "отключи звук", "mute"]):
            volume.SetMasterVolumeLevelScalar(0.0, None)
            speak("Звук выключен")
            return

        # Уменьшение громкости
        elif any(phrase in command for phrase in ["потише", "уменьши", "сделай тише", "убавь", "уменьшить"]):
            new_level = max(0.0, current - 0.4)
            volume.SetMasterVolumeLevelScalar(new_level, None)
            speak(f"Громкость уменьшена")
            return

        # Увеличение громкости
        elif any(phrase in command for phrase in ["погромче", "увеличь", "сделай громче", "прибавь", "увеличить"]):
            new_level = min(1.0, current + 0.4)
            volume.SetMasterVolumeLevelScalar(new_level, None)
            speak(f"Громкость увеличена")
            return

        # Установка конкретного уровня
        numbers = [int(word) for word in command.split() if word.isdigit()]
        if numbers:
            level = max(0, min(numbers[0], 100))
            volume.SetMasterVolumeLevelScalar(level / 100.0, None)
            speak(f"Громкость установлена")
            return

        speak("Не удалось определить, что сделать с громкостью")

    except Exception:
        speak("Ошибка при изменении громкости")


def move_cursor(command):
    try:
        # Получаем текущие координаты
        current_x, current_y = pyautogui.position()

        # Пытаемся найти число
        numbers = [int(word) for word in command.split() if word.isdigit()]
        delta = numbers[0] if numbers else 100  # Если числа нет — используем это

        # Определяем направление
        if any(word in command for word in ["вправо", "правее"]):
            new_x, new_y = current_x + delta, current_y
            direction = "вправо"
        elif any(word in command for word in ["влево", "левее"]):
            new_x, new_y = current_x - delta, current_y
            direction = "влево"
        elif any(word in command for word in ["вверх", "выше"]):
            new_x, new_y = current_x, current_y - delta
            direction = "вверх"
        elif any(word in command for word in ["вниз", "ниже"]):
            new_x, new_y = current_x, current_y + delta
            direction = "вниз"
        else:
            speak("Не удалось определить направление")
            return

        # Перемещаем курсор
        pyautogui.moveTo(new_x, new_y, duration=0.5)
        speak(f"Курсор перемещён {direction} на {delta} пикселей")

    except Exception:
        speak("Ошибка при перемещении курсора")


def save_note(command, list_commands):
    try:
        # Извлекаем всё после ключевого слова
        for trigger in list_commands:
            if trigger in command:
                note_text = command.split(trigger, 1)[-1].strip()
                break
        else:
            speak("Не удалось распознать что написать в заметки")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"note_{timestamp}.txt"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(note_text)

        speak("Заметка сохранена.")
    except Exception as e:
        speak(f"Ошибка при сохранении заметки: {e}")


def click_at(command):
    try:
        # Пытаемся найти координаты в команде
        numbers = [int(word) for word in command.split() if word.isdigit()]

        if len(numbers) >= 2:
            x, y = numbers[0], numbers[1]
            pyautogui.click(x, y)
            speak(f"Щелчок в точке {x}, {y}")
        else:
            # Если координаты не указаны — кликаем по текущей позиции
            x, y = pyautogui.position()
            pyautogui.click()
            speak(f"Щелчок в текущей точке {x}, {y}")

    except Exception:
        speak("Не удалось выполнить щелчок")


def handle_print_command(command, list_commands):
    try:
        # Извлекаем всё после ключевого слова
        for trigger in list_commands:
            if trigger in command:
                text = command.split(trigger, 1)[-1].strip()
                break
        else:
            speak("Не удалось распознать что написать")
            return

        if text:
            keyboard.write(text, delay=0.05)  # Ввод текста
            speak(f"Написала: {text}")
        else:
            speak("Что именно написать?")

    except Exception:
        speak("Ошибка при выполнении команды печати")


def search_google(command):
    try:
        # Извлекаем текст после ключевого слова
        query = " ".join(command.split()[1:]).strip()

        if not query:
            speak("Что искать в Google?")
            return

        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(url)
        speak(f"Ищу в Google: {query}")

    except Exception:
        speak("Не удалось выполнить поиск в Google")


def scroll_page(command):
    try:
        cmd = command.lower()
        amount = 200  # значение по умолчанию

        if "вниз" in cmd:
            direction = -1
        elif "вверх" in cmd:
            direction = 1
        else:
            speak("Не поняла направление прокрутки")
            return

        # Ищем число в команде
        numbers = [int(word) for word in cmd.split() if word.isdigit()]
        if numbers:
            amount = numbers[0]

        pyautogui.scroll(direction * amount)
        speak(f"Прокрутил {'вниз' if direction == -1 else 'вверх'} на {amount} единиц")

    except Exception:
        speak("Ошибка при прокрутке страницы")


def minimize_windows():
    if get_keyboard_language().startswith('ru'):
        # переключаем язык на англ, так как при русской расскладке не работает комбинация клавиш
        pyautogui.hotkey('alt', 'shift')

    pyautogui.hotkey('win', 'd')
    speak("Все окна свернуты")


def switch_language():
    try:
        time.sleep(0.2)
        pyautogui.hotkey('alt', 'shift')
        speak("Язык переключён")
    except Exception:
        speak("Не удалось переключить язык")


def take_screenshot():
    try:
        folder = "screenshots"
        os.makedirs(folder, exist_ok=True)
        filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        path = os.path.join(folder, filename)

        screenshot = pyautogui.screenshot()
        screenshot.save(path)

        speak(f"Скриншот сохранён: {filename}")
    except Exception:
        speak("Не удалось сделать скриншот.")


def click_enter():
    try:
        time.sleep(0.2)
        pyautogui.press('enter')
        speak("Нажала enter")
    except Exception:
        speak("Не удалось нажать enter")


def click_space():
    try:
        time.sleep(0.2)
        pyautogui.press('space')
        speak("Нажала space")
    except Exception:
        speak("Не удалось нажать space")


def paste_text():
    if get_keyboard_language().startswith('ru'):
        # переключаем язык на англ, так как при русской расскладке не работает комбинация клавиш
        pyautogui.hotkey('alt', 'shift')

    try:
        time.sleep(0.2)
        keyboard.press_and_release('ctrl+v')
        speak("Вставила текст из буфера")
    except Exception:
        speak("Не удалось вставить текст")


def copy_text():
    if get_keyboard_language().startswith('ru'):
        # переключаем язык на англ, так как при русской расскладке не работает комбинация клавиш
        pyautogui.hotkey('alt', 'shift')

    try:
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'c')
        speak("Скопировала выделенный текст")
    except Exception:
        speak("Не удалось скопировать текст")


def delete_text(command):
    try:
        if any(kw in command for kw in ["удали все", "удали весь текст", "очисти поле", "удалить все"]):
            if get_keyboard_language().startswith('ru'):
                # переключаем язык на англ, так как при русской расскладке не работает комбинация клавиш
                pyautogui.hotkey('alt', 'shift')

            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('backspace')
            speak("Удалила весь текст")
            return

        elif any(kw in command for kw in ["удали выделенное", "удали выделенный текст", "удали то что выделил",
                                          "удали последний символ", "удали последнее", "удали символ"]):
            pyautogui.press('backspace')
            speak("Удалила")
            return

        # Удалить последние X символов
        numbers = [int(word) for word in command.split() if word.isdigit()]
        if numbers:
            count = numbers[0]
            for _ in range(count):
                pyautogui.press('backspace')
            speak(f"Удалила последние {count} символов")
            return

        speak("Не удалось определить, что удалить")

    except Exception:
        speak("Ошибка при удалении текста")


def handle_hotkey_command(main_command, list_commands):
    try:
        # Извлекаем всё после ключевого слова
        for trigger in list_commands:
            if trigger in main_command:
                hotkey_part = main_command.split(trigger, 1)[-1].strip()
                break
        else:
            speak("Не удалось распознать комбинацию")
            return

        # Удаляем лишние слова и пробелы
        hotkey_clean = hotkey_part.replace(" и ", "+").replace(" плюс ", "+").replace(" plus ", "+").replace(" ", "")

        if hotkey_clean:
            keyboard.send(hotkey_clean)
            speak(f"Нажала комбинацию {hotkey_clean}")
        else:
            speak("Не удалось распознать комбинацию")

    except Exception:
        speak("Ошибка при выполнении команды клавиш")
