# github.com/kripersi , tg: @Marpexiz
from assistant.actions import *
from assistant.preprocess_command import match_command
from assistant.utils import equ


def execute(command):
    action, target, list_variants = match_command(command)

    if equ(action, "открой"):
        open_app(target)

    elif equ(action, "текст"):
        if "встав" in command:
            paste_text()
        elif "копир" in command:
            copy_text()
        elif "удал" in command:
            delete_text(command)

    elif equ(action, "поиск"):
        focus_search_field()

    elif equ(action, "скриншот"):
        take_screenshot()

    elif equ(action, "очистка корзины"):
        clear_trash()

    elif equ(action, "пробел"):
        click_space()

    elif equ(action, "закрыть активное окно"):
        close_active_window()

    elif equ(action, "enter"):
        click_enter()

    elif equ(action, "прокрутка"):
        scroll_page(command)

    elif equ(action, "сверни"):
        minimize_windows()

    elif equ(action, "громкость"):
        set_volume(command)

    elif equ(action, "курсор"):
        move_cursor(command)

    elif equ(action, "поиск в гугле"):
        search_google(command)

    elif equ(action, "язык"):
        switch_language()

    elif equ(action, "клик"):
        click_at(command)

    elif equ(action, "комбинация"):
        handle_hotkey_command(command, list_variants)

    elif equ(action, "печать"):
        handle_print_command(command, list_variants)

    elif equ(action, "выход"):
        speak("До встречи.")
        raise SystemExit




