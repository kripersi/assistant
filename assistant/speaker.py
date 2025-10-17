import torch
import sounddevice as sd
import time
from config import SPEAKER, DEVICE_CPU


class TTS:
    def __init__(self, speaker=SPEAKER, device=DEVICE_CPU, samplerate=48000):
        self.model, _ = torch.hub.load(
            repo_or_dir="snakers4/silero-models",
            model="silero_tts",
            language="ru",
            speaker="ru_v3"
        )
        self.model.to(torch.device(device))
        self.speaker = speaker
        self.samplerate = samplerate

    def speak(self, text: str):
        audio = self.model.apply_tts(
            text=text,
            speaker=self.speaker,
            sample_rate=self.samplerate,
            put_accent=True,
            put_yo=True
        )

        sd.play(audio, samplerate=self.samplerate)
        time.sleep(len(audio) / self.samplerate)
        sd.stop()


# Инициализация TTS
tts = TTS(speaker=SPEAKER)


# Функция озвучки
def speak(text):
    tts.speak(text)



