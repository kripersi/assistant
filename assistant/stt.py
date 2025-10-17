# github.com/kripersi , tg: @Marpexiz
from .speaker import speak
from config import STT_PATH

from words2numsrus.extractor import NumberExtractor
import sounddevice as sd
import queue
import json
import vosk
import sys


class STT:
    def __init__(self, modelpath: str = "model", samplerate: int = 16000, device: int = None):
        print("Инициализация модели Vosk...")
        self.recognizer = vosk.KaldiRecognizer(vosk.Model(modelpath), samplerate)
        self.q = queue.Queue()
        self.samplerate = samplerate
        self.device = device

    def q_callback(self, indata, _, __, status):
        if status:
            print(f"[VOSK] Статус: {status}", file=sys.stderr)
        self.q.put(bytes(indata))

    def listen_once(self) -> str:
        with sd.RawInputStream(
            samplerate=self.samplerate,
            blocksize=8000,
            device=self.device,
            dtype='int16',
            channels=1,
            callback=self.q_callback
        ):

            while True:
                data = self.q.get()
                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())["text"]
                    return result.lower().replace("ё", "е")


stt = STT(
    modelpath=STT_PATH,
    samplerate=16000,
    device=5
)


def listen():
    try:
        command = stt.listen_once()

        # Преобразование текстовых чисел в цифровые
        extractor = NumberExtractor()
        command = extractor.replace_groups(command)

        if len(command) > 2:
            print(f"Распознано: {command}")

        return command
    except Exception as e:
        speak("Ошибка при распознавании речи.")
        print(f"[ERROR] {e}")
        return ""


