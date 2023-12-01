import pyttsx3


class Assistant:
    """Инкапсулирует свойств и методов голосового ассистента"""

    tts = None
    """Синтезатор речи"""

    def __init__(self, language: str, rate: int, volume: float) -> None:
        """
        Инициализирует свойства голосового ассистента
        Инициализирует синтезатор речи, если этого еще не произошло
        """
        if Assistant.tts == None:
            Assistant.tts = pyttsx3.init()

        self.set_language(language)
        self.set_rate(rate)
        self.set_volume(volume)

    def set_rate(self, rate: int = 200) -> None:
        """
        Устанавливает скорость воспроизведения слов в минуту
        :param rate: скорость воспроизведения слов в минуту
        """
        if rate < 1:
            rate = 1
        elif rate > 1000:
            rate = 1000

        Assistant.tts.setProperty("rate", rate)

    def set_volume(self, volume: float = 1.0) -> None:
        """
        Устанавливает громкость голоса ассистента
        :param volume: громкость голоса ассистента. Принимает значения от 0.0 до 1.0
        """
        if volume < 0.0:
            volume = 0.0
        elif volume > 1.0:
            volume = 1.0

        Assistant.tts.setProperty("volume", volume)

    def set_language(self, language: str) -> None:
        """
        Устанавливает языковые параметры для ассистента
        :param language: разговорный язык голосового ассистента
        """
        language = language.lower()
        Assistant.tts.setProperty("voice", language)
        assistant_id = (
            "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_RU-RU_IRINA_11.0"
            if language == "ru"
            else "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"
        )
        Assistant.tts.setProperty("voice", assistant_id)

    def play_voice_speech(self, text: str) -> None:
        """
        Проигрывание речи голосового ассистента
        :param text: текст, который преобразуется в речь
        """
        Assistant.tts.say(text)
        Assistant.tts.runAndWait()

    def print_and_play(self, message: str) -> None:
        """
        Записывает сообщение в консоль и проигрывает его как речь
        :param text: текст, который выведется в консоль и преобразуется в речь
        """
        print(message)
        self.play_voice_speech(message)
