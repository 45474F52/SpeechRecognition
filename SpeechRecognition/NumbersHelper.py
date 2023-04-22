class NumbersHelper:
    """Инкапсулирует методы преобразования чисел из строкового представления в эквивалентное им числовое значение"""

    @staticmethod
    def int_parse(text: str) -> int:
        """
        Преобразует текст в число (до тысячи)
        """
        number = int(0)
        units = text.split(" ")
        length = len(units)
        if length == 1:
            numth = NumbersHelper.__switch_thousands(units[0])
            numh = NumbersHelper.__switch_hundreds(units[0])
            numt = NumbersHelper.__switch_tens(units[0])
            numu = NumbersHelper.__switch_units(units[0])
            number = numth + numh + numt + numu
        elif length == 2:
            numth = NumbersHelper.__switch_thousands(units[0])
            numh = NumbersHelper.__switch_hundreds(units[0])
            numt1 = NumbersHelper.__switch_tens(units[0])
            numt2 = NumbersHelper.__switch_tens(units[1])
            numu1 = NumbersHelper.__switch_units(units[1])
            number = numth + numh + numt1 + numt2 + numu1
        elif length == 3:
            numth = NumbersHelper.__switch_thousands(units[0])
            numh = NumbersHelper.__switch_hundreds(units[0])
            numt1 = NumbersHelper.__switch_tens(units[1])
            numu1 = NumbersHelper.__switch_units(units[2])
            number = numth + numh + numt1 + numu1

        return number if number <= int(1000) else int(1000)

    @staticmethod
    def float_parse(text: str) -> float:
        """Преобразует текст в число с плавающей точкой (в диапазоне от 0.0 до 1.0)"""
        number = float(0.0)

        units = text.split(" ")
        length = len(units)
        if length == 1:
            number = float(1.0) if units[0] == "один" else float(0.0)
        else:
            half1 = NumbersHelper.__switch_units(units[0])
            half2 = NumbersHelper.__switch_units(units[2])
            num = str(half1) + "." + str(half2)
            number = float(num)

        return number if number <= float(1.0) else float(1.0)

    @staticmethod
    def __switch_thousands(text: str) -> int:
        """Парсинг тысяч"""
        if text.startswith("тыс"):
            return int(1000)
        else:
            return int(0)

    @staticmethod
    def __switch_hundreds(text: str) -> int:
        """Парсинг сотен"""
        if text == "девятьсот":
            return int(900)
        elif text == "восемьсот":
            return int(800)
        elif text == "семьсот":
            return int(700)
        elif text == "шестьсот":
            return int(600)
        elif text == "пятьсот":
            return int(500)
        elif text == "четыреста":
            return int(400)
        elif text == "триста":
            return int(300)
        elif text == "двести":
            return int(200)
        elif text == "сто":
            return int(100)
        else:
            return int(0)

    @staticmethod
    def __switch_tens(text: str) -> int:
        """Парсинг десятков"""
        if text == "девяносто":
            return int(90)
        elif text == "восемьдесят":
            return int(80)
        elif text == "семьдесят":
            return int(70)
        elif text == "шестьдесят":
            return int(60)
        elif text == "пятьдесят":
            return int(50)
        elif text == "сорок":
            return int(40)
        elif text == "тридцать":
            return int(30)
        elif text == "двадцать":
            return int(20)
        elif text == "девятнадцать":
            return int(19)
        elif text == "восемнадцать":
            return int(18)
        elif text == "семнадцать":
            return int(17)
        elif text == "шестнадцать":
            return int(16)
        elif text == "пятнацдать":
            return int(15)
        elif text == "четырнадцать":
            return int(14)
        elif text == "тринадцать":
            return int(13)
        elif text == "двенадцать":
            return int(12)
        elif text == "одиннадцать" or text == "одинадцать":
            return int(11)
        elif text == "десять":
            return int(10)
        else:
            return int(0)

    @staticmethod
    def __switch_units(text: str) -> int:
        """Парсинг единиц"""
        if text == "девять":
            return int(9)
        elif text == "восемь":
            return int(8)
        elif text == "семь":
            return int(7)
        elif text == "шесть":
            return int(6)
        elif text == "пять":
            return int(5)
        elif text == "четыре":
            return int(4)
        elif text == "три":
            return int(3)
        elif text == "два":
            return int(2)
        elif text == "один" or text == "одну":
            return int(1)
        else:
            return int(0)
