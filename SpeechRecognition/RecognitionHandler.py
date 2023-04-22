from vosk import Model
from enum import Enum
import AssistantManager as am


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


class RecognitionHandler:
    current_model = None
    current_model_name = ""

    def __init__(self, language: str, rate: int, volume: float) -> None:
        """Инициализирует голосового ассистента"""
        self.__assistant = am.Assistant(language, rate, volume)

    def set_model(self, model: Models) -> None:
        """
        Изменяет используемую речевую модель
        :param model: речевая модель, которую нужно использовать
        """
        RecognitionHandler.current_model_name = model.name
        print("Смена модели на %s ..." % RecognitionHandler.current_model_name)
        self.__assistant.play_voice_speech("Ожидайте установку речевой модели")
        RecognitionHandler.current_model = Model(model.value)
        self.__assistant.play_voice_speech("Установка речевой модели завершена")
        print("READY")

    @property
    def get_assistant(self) -> am.Assistant:
        return self.__assistant