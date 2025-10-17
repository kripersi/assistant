# github.com/kripersi , tg: @Marpexiz
from assistant.stt import listen
from assistant.speaker import speak
from assistant.dispatcher import execute


def run_assistant():
    speak("Привет. Готова начать работу!")
    while True:
        command = listen()

        if command:
            execute(command)


if __name__ == "__main__":
    run_assistant()

