import os
import RecognitionHandler as rh
import AssistantManager as am


class Command:
    """
    Объект команды, к которому можно обратиться по псевдониму из списка, чтобы выполнить указанную функцию. Имеет описание.
    """

    named = False
    """Показывает идёт ли в данный момент обращение к ассистенту по его имени"""
    name = ""
    """Имя ассистента"""

    @staticmethod
    def __init_name() -> None:
        """Получает имя ассистента, по которому идёт обращение к нему"""
        from ConfigurationManager import ConfigurationManager as config

        Command.name = config.get_value_by_prop_name("assistant name")

    def __init__(
        self, aliasses: list[str], action, description: str = "—", visible: bool = True
    ) -> None:
        """
        Инициализирует команду списком псевдонимов, функцией и описанием
        :param aliasses: список псевдонимов, по которым можно идентифицировать команду
        :param action: функция, которую выполняет команда. Функция обязательно принимает список аргументов
        :param description: описание того, что делает эта команда
        :param visible: определяет будет ли отображаться справка по этой команде
        """
        if Command.name == "":
            Command.__init_name()

        self.__aliasses = aliasses
        self.__action = action
        self.__description = description
        self.__visible = visible

    @property
    def aliasses(self) -> list[str]:
        """Список псевдонимов (идентификаторов) команды"""
        return self.__aliasses

    @property
    def action(self):
        """Функция, которую выполняет команда"""
        return self.__action

    @property
    def description(self) -> str:
        """Описание того, что делает эта команда"""
        return self.__description

    @property
    def visible(self) -> bool:
        """Определяет будет ли эта команда отображаться в справке по командам"""
        return self.__visible

    def info(self) -> str:
        """Возвращает текст с полным описанием команды"""
        return "\n" + " или ".join(self.__aliasses) + ": " + "\n" + self.__description


__recHandler = rh.RecognitionHandler
__assistant = am.Assistant
__console_visible_flag = False


def init_references(recHandler: rh.RecognitionHandler):
    """Обязательная инициализация голосового ассистента"""
    global __recHandler
    global __assistant
    __recHandler = recHandler
    __assistant = __recHandler.get_assistant

    # FUNCTIONS


def show_commands_func(args: list[str]) -> None:
    """
    Отображает информацию для ознакомления с командами
    """
    __assistant.print_and_play("Справка")
    for command in commands:
        if command.visible == True:
            __assistant.play_voice_speech("Команды")
            __assistant.print_and_play(command.info())


def exit_func(args: list[str]):
    """
    Останавливает выполнение программы с кодом 0
    """
    __assistant.print_and_play("Пока :(")
    exit(0)


def close_func(args: list[str]) -> None:
    """
    Закрывает активное окно
    """
    from WinAPI import WindowsHandler as wh

    engine = wh.Engine()
    if engine.close_active_window() == False:
        __assistant.print_and_play("ОШИБКА WinAPI")


def cls_func(args: list[str]):
    """
    Очищает командную строку текущего процесса
    """
    os.system("cls")


def mute_func(args: list[str]) -> None:
    """
    Блокирует звук. При повторном использовании возобновляет его
    """
    from WinAPI import SoundHandler as sh

    if sh.SoundHandler.mute() == False:
        __assistant.print_and_play("ОШИБКА WinAPI")


def console_window_func(args: list[str]) -> None:
    """
    Скрывает окно консоли. При повторном использовании возобновляет его
    """
    from WinAPI import WindowsHandler as wh

    global __console_visible_flag
    engine = wh.Engine()
    if __console_visible_flag == False:
        __console_visible_flag = True
        engine.hide_console()
    else:
        __console_visible_flag = False
        engine.show_console()


def change_func(args: list[str]):
    """
    Меняет модель на новую, если она еще не используется
    :param args: параметры для полного сопоставления с командой
    """
    if len(args) == 3:
        if args[0] == "модель" and args[1] == "на":
            model_type = args[2]

            if model_type == "простую":
                model_name = rh.Models.small_model.name
            elif model_type == "улучшенную":
                model_name = rh.Models.big_model.name
            else:
                model_name = ""

            if model_name != "":
                if __recHandler.current_model_name != model_name:
                    __recHandler.current_model_name = model_name
                    __recHandler.set_model(
                        rh.Models.big_model
                        if __recHandler.current_model_name == rh.Models.big_model.name
                        else rh.Models.small_model
                    )
                else:
                    __assistant.print_and_play("Эта модель уже используется")

                return

    for arg in args:
        print(arg, end=" ")

    print()


def open_in_browser_func(args: list[str]):
    """
    Запускает браузер с переданным запросом
    :param args: запрос в браузере
    """
    querry = "+".join(args)
    cmdCommand = "start microsoftedge https://www.bing.com/search?q=" + querry
    os.system(cmdCommand)


def start_process_func(args: list[str]):
    """
    Запускает процесс по его имени
    :param args: имя процесса
    """
    if len(args) > 0:
        process = ""
        process_name = args[0]
        if process_name == "браузер":
            process = "microsoftedge"
        elif process_name == "блокнот":
            process = "notepad"
        else:
            message = "Процесс " + process_name + " не найден"
            __assistant.print_and_play(message)
            return

        os.system(process)


def incr_decr_prop_func(args: list[str]) -> None:
    """
    Увеличивает или уменьшает: скорость проигрывания слов / громкость голосового ассистента
    :param args: параметры для полного сопоставления с командой
    """
    if 3 <= len(args) <= 6:
        prop = args[0]
        if prop == "скорость" or "громкость" and args[1] == "на":
            from NumbersHelper import NumbersHelper as nh
            from ConfigurationManager import ConfigurationManager as config
            nums = [n for n in args[2 : len(args)]]

            if prop == "скорость":
                value = nh.int_parse(" ".join(nums))
                __assistant.set_rate(value)
                config.set_value_by_prop_name("speech rate", str(value))
            else:
                if nums[0] == "один" or (nums[1] == "целых" and (nums[3] == "десятых" or nums[3] == "десятую")):
                    value = nh.float_parse(" ".join(nums))
                    __assistant.set_volume(value)
                    config.set_value_by_prop_name("assistant volume", str(value))
                else:
                    return

            __assistant.print_and_play(f"Параметр \"{prop}\" изменён")


commands = [
    Command(
        ["команды", "помощь", "справка"], show_commands_func, "Справка по командам", False),
    Command(
        ["завершить", "закройся"], exit_func, "Остановить выполнение программы"),
    Command(
        ["закрыть", "закрой"], close_func, "Закрыть активное окно"),
    Command(
        ["очистить", "сотри"], cls_func, "Очистить командную строку текущего процесса"),
    Command(
        ["звук"], mute_func, "Блокировать звук. При повторном использовании звук возвращается"),
    Command(
        ["консоль", "терминал"], console_window_func, "Скрыть окно консоли. При повторном использовании окно возвращается"),
    Command(
        ["смени", "измени"], change_func, "Изменить речевую модель"),
    Command(
        ["найди", "покажи"], open_in_browser_func, "Запустить браузер с запросом"),
    Command(
        ["открой", "запусти"], start_process_func, "Запустить процесс по его имени"),
    Command(
        ["увеличь", "прибавь", "уменьши", "убавь"], incr_decr_prop_func, "Изменить: скорость / громкость ассистента", False),
]
