def int_parse(text: str) -> int:
    """
    Преобразует текст в число (до тысячи)
    """
    number = None
    units = text.split(" ")
    length = len(units)
    if length == 1:
        numh = switch_hundreds(units[0])
        numt = switch_tens(units[0])
        numu = switch_units(units[0])
        number = numh + numt + numu
    elif length == 2:
        numh = switch_hundreds(units[0])
        numt1 = switch_tens(units[0])
        numt2 = switch_tens(units[1])
        numu1 = switch_units(units[1])
        number = numh + numt1 + numt2 + numu1
    elif length == 3:
        numh = switch_hundreds(units[0])
        numt1 = switch_tens(units[1])
        numu1 = switch_units(units[2])
        number = numh + numt1 + numu1

    return number if number <= 1000 else 1000


def float_parse(text: str) -> float:
    pass


def switch_hundreds(text: str) -> int:
    if text.startswith("тыс"):
        return 1000
    elif text == "девятьсот":
        return 900
    elif text == "восемьсот":
        return 800
    elif text == "семьсот":
        return 700
    elif text == "шестьсот":
        return 600
    elif text == "пятьсот":
        return 500
    elif text == "четыреста":
        return 400
    elif text == "триста":
        return 300
    elif text == "двести":
        return 200
    elif text == "сто":
        return 100
    else:
        return 0


def switch_tens(text: str) -> int:
    if text == "девяносто":
        return 90
    elif text == "восемьдесят":
        return 80
    elif text == "семьдесят":
        return 70
    elif text == "шестьдесят":
        return 60
    elif text == "пятьдесят":
        return 50
    elif text == "сорок":
        return 40
    elif text == "тридцать":
        return 30
    elif text == "двадцать":
        return 20
    elif text == "девятнадцать":
        return 19
    elif text == "восемнадцать":
        return 18
    elif text == "семнадцать":
        return 17
    elif text == "шестнадцать":
        return 16
    elif text == "пятнацдать":
        return 15
    elif text == "четырнадцать":
        return 14
    elif text == "тринадцать":
        return 13
    elif text == "двенадцать":
        return 12
    elif text == "одиннадцать" or text == "одинадцать":
        return 11
    elif text == "десять":
        return 10
    else:
        return 0


def switch_units(text: str) -> int:
    if text == "девять":
        return 9
    elif text == "восемь":
        return 8
    elif text == "семь":
        return 7
    elif text == "шесть":
        return 6
    elif text == "пять":
        return 5
    elif text == "четыре":
        return 4
    elif text == "три":
        return 3
    elif text == "два":
        return 2
    elif text == "один":
        return 1
    else:
        return 0