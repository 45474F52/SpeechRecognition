from ConfigurationManager import ConfigurationManager as config
import json, pyaudio, win32api
from vosk import KaldiRecognizer
import CommandHandler as ch
import RecognitionHandler as rh
import AssistantManager as am


def execute_command(name: str, args: list[str]) -> None:
    """
    Выполнение команды с передачей аргументов по её имени
    :param name: имя команды
    :param args: аргументы, необходимые для выполнения команды
    """
    if ch.Command.named == True:
        for command in ch.commands:
            if name in command.aliasses:
                command.action(args)
                ch.Command.named = False
                return

    message = name + " " + " ".join(args)
    __assistant.print_and_play(message)


def format_text_to_parameters(text: str) -> tuple[str, list[str]]:
    """
    Форматирует строку в список параметров "название команды", "параметры для команды"
    :param text: строка с запросом для выполнения команды
    """
    params = text.split(" ")
    command_name = params[0]
    command_args = [input_part for input_part in params[1 : len(params)]]

    return [command_name, command_args]


def manual_testing() -> int:
    """Запускается для ручного тестирования программы"""
    text = ""
    while text != "exit":
        ch.Command.named = True
        text = input("Command >>> ")
        querry = format_text_to_parameters(text)
        execute_command(querry[0], querry[1])

    return int(0)


__recHandler = rh.RecognitionHandler
__assistant = am.Assistant


def main() -> int:
    """Точка старта программы"""
    global __recHandler
    global __assistant

    language = config.get_value_by_prop_name("assistant language")
    rate = int(config.get_value_by_prop_name("speech rate"))
    volume = float(config.get_value_by_prop_name("assistant volume"))

    __recHandler = rh.RecognitionHandler(language, rate, volume)
    __assistant = __recHandler.get_assistant
    
    ch.init_references(__recHandler)

    model = config.get_value_by_prop_name("model")
    if model == "big":
        __recHandler.set_model(rh.Models.big_model)
    else:
        __recHandler.set_model(rh.Models.small_model)

    magic_number_1 = int(16000)
    magic_number_2 = int(8000)
    magic_number_3 = int(4000)

    recognizer = KaldiRecognizer(rh.RecognitionHandler.current_model, magic_number_1)

    mode = config.get_value_by_prop_name("app mode")
    if mode == "manual":
        return manual_testing()
    elif mode != "voice":
        return int(1)

    audio = pyaudio.PyAudio()

    audio_stream = audio.open(
        rate=magic_number_1,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=magic_number_2,
    )
    audio_stream.start_stream()

    def listen_and_recognize() -> str:
        """
        Получает данные из аудио-потока и преобразует их в текст
        """
        while True:
            data = audio_stream.read(magic_number_3, exception_on_overflow=False)

            if recognizer.AcceptWaveform(data) and (len(data) > 0):
                recognized_data = json.loads(recognizer.Result())

                if recognized_data["text"]:
                    yield recognized_data["text"]

    for text in listen_and_recognize():
        if text == ch.Command.name:
            ch.Command.named = True
            win32api.Beep(500, 300)
            print(">")
        else:
            querry = format_text_to_parameters(text)
            execute_command(querry[0], querry[1])

    audio.close(audio_stream)
    return int(0)


if __name__ == "__main__":
    exit(main())