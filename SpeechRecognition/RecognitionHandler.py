from vosk import Model
from enum import Enum
import pyttsx3


class Models(Enum):
    """
    Содержит пути до папок речевых моделей
    """

    small_model = "C:\\Users\\egori\\Desktop\\model"
    """
    Небольшая модель. Загружается ~ 5 секунд. Плохое качество распознавания речи
    """
    big_model = "C:\\Users\\egori\\Desktop\\big_model"
    """
    Большая модель. Загружается ~ 1.5 минуты. Хорошее качество распознавания речи
    """


tts = None
"""
Синтезатор речи
"""

current_model = None
current_model_name = ""

def set_speech_rate(rate: int = 200) -> None:
    """
    Устанавливает скорость воспроизведения слов в минуту
    :param rate: скорость воспроизведения слов в минуту
    """
    if rate < 1:
        rate = 1
    elif rate > 1000:
        rate = 1000

    tts.setProperty("voice", rate)


def set_speech_volume(volume: float = 1.0) -> None:
    """
    Устанавливает громкость голоса ассистента
    :param volume: громкость голоса ассистента. Принимает значения от 0.0 до 1.0
    """
    if volume < 0.0:
        volume = 0.0
    elif volume > 1.0:
        volume = 1.0

    tts.setProperty("voice", volume)


def assistant_init(language: str = "ru", rate: int = 200, volume: float = 1.0) -> None:
    """
    Инициализирует голосового ассистента
    :param language: разговорный язык голосового ассистента. Доступные значения: "ru", "en"
    :param rate: скорость воспроизведения слов в минуту
    :param volume: громкость голоса ассистента. Принимает значения от 0.0 до 1.0
    """
    language = language.lower()
    tts.setProperty("voice", language)
    assistant_id = (
        "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_RU-RU_IRINA_11.0"
        if language == "ru"
        else "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
    )
    tts.setProperty("voice", assistant_id)
    set_speech_rate(rate)
    set_speech_volume(volume)


def init(language: str = "ru", rate: int = 200, volume: float = 1.0) -> None:
    """
    Инициализирует синтезатор речи и голосового ассистента
    :param language: разговорный язык голосового ассистента
    :param rate: скорость воспроизведения слов в минуту
    :param volume: громкость голоса ассистента
    """
    global tts
    tts = pyttsx3.init()
    assistant_init(language, rate, volume)


def play_voice_speech(text: str) -> None:
    """
    Проигрывание речи голосового ассистента
    :param text: текст, который преобразуется в речь
    """
    tts.say(text)
    tts.runAndWait()


def set_model(model: Models) -> None:
    """
    Изменяет используемую речевую модель
    :param model: речевая модель, которую нужно использовать
    """
    global current_model_name
    current_model_name = model.name

    print("Смена модели на %s ..." % current_model_name)
    play_voice_speech("Ожидайте установку речевой модели")

    global current_model
    current_model = Model(model.value)

    play_voice_speech("Установка речевой модели завершена")
    print("READY")
