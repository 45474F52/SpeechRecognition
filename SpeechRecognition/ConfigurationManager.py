import os
from enum import Enum


class AppModes(Enum):
    """Режимы работы приложения"""

    Manual = "manual"
    """Ручной режим работы"""
    Voice = "voice"
    """Голосовой режим работы"""


class ConfigurationManager:
    """Инкапсулирует методы взаимодействия с файлом конфигурации приложения"""

    __file = "appConfig.txt"
    """Путь до файла конфигурации приложения"""

    @staticmethod
    def set_path(path: str):
        """
        Устанавливает новый путь до файла конфигурации
        :remarks: Вызывает исключение FileNotFoundError, если файла по указанному пути не существует
        :param path: путь до файла конфигурации
        """
        if os.path.exists(path):
            ConfigurationManager.__file = path
        else:
            raise FileNotFoundError(path)

    @staticmethod
    def get_all_lines() -> list[str]:
        """Возвращает все строки из файла конфигурации"""
        with open(ConfigurationManager.__file, "r") as config:
            lines = config.readlines()
        return lines

    @staticmethod
    def get_line_by_prop_name(name: str) -> str:
        """
        Возвращает строку из файла конфигурации с определённым свойством или пустую строку, если искомое свойство не найдено
        :param name: имя свойства
        """
        lines = ConfigurationManager.get_all_lines()
        i = 0
        name = name.lower()
        while i < len(lines):
            if lines[i].startswith("property: " + name.lower()):
                return lines[i]
            else:
                i = i + 1

        return ""

    @staticmethod
    def get_prop_value_pair(name: str) -> list[str]:
        """
        Возвращает пару "свойство - значение" по имени свойства или пустой список, если искомое свойство не найдено
        :param name: имя свойства
        """
        return ConfigurationManager.parse_pair_from_line(
            ConfigurationManager.get_line_by_prop_name(name)
        )

    @staticmethod
    def parse_pair_from_line(line: str) -> list[str]:
        """
        Возвращает пару "свойство - значение" из строки со свойством или пустой список, если искомое свойство не найдено
        :param line: строка со свойством из файла конфигурации
        """
        pair = list[str]()
        if line != "":
            pair = line.split(" #")[0].split(";")
        return pair

    @staticmethod
    def parse_value_from_pair(value: str) -> str:
        """
        Возвращает значение, хранимое в паре "свойство - значение" или пустую строку, если значение было пустым
        :param value: "значение" из пары "свойство - значение"
        """
        return (
            ""
            if value.isspace() == True or value == ""
            else value.replace("value: ", "")
        )

    @staticmethod
    def get_value_by_prop_name(name: str) -> str:
        """
        Возвращает значение свойства по его имени из файла конфигурации приложения или пустую строку, если искомое свойство не найдено
        :param name: имя свойства
        """
        pair = ConfigurationManager.get_prop_value_pair(name)
        return (
            "" if len(pair) < 2 else ConfigurationManager.parse_value_from_pair(pair[1])
        )

    @staticmethod
    def set_value_by_prop_name(name: str, value: str) -> None:
        """
        Ищет свойство по имени и, если оно найдено, устанавливает для него значение
        :remarks: Новое значение не должно содержать следующие спецсимволы ':', ',', ';', '#', '|'
        :param: name: имя свойства
        :param: value: новое значение свойства
        """
        line = ConfigurationManager.get_line_by_prop_name(name)
        if line != "":
            prop_value_pair = ConfigurationManager.parse_pair_from_line(line)
            if len(prop_value_pair) >= 2:
                new_pair = prop_value_pair.copy()
                new_pair[1] = "value: " + value
                newLine = line.replace(";".join(prop_value_pair), ";".join(new_pair))

                with open(ConfigurationManager.__file, "r") as config:
                    text = config.read()

                text = text.replace(line, newLine)

                with open(ConfigurationManager.__file, "w") as config:
                    config.write(text)
