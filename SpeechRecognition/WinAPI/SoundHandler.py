import ctypes as c
from enum import Enum


class SoundHandler:
    """Инкапсулирует методы взаимодействия со звуком"""

    send_input = c.windll.user32.SendInput
    ptr = c.POINTER(c.c_ulong)

    @staticmethod
    def __key_down() -> c.c_ulong:
        """Запускает событие нажатия на клавишу"""
        inputs_count = c.c_ulong(1)
        extra = c.c_ulong(0)
        unit = INPUTUNIT()
        unit.ki = KEYBDINPUT(
            c.c_ushort(SoundVirtualKeys.MUTE.value),
            c.c_ushort(0x48),
            c.c_ulong(KeyEventFlags.KEY_DOWN.value),
            c.c_ulong(0),
            c.pointer(extra),
        )
        input_struct = INPUT(c.c_ulong(1), unit)
        SoundHandler.send_input(
            inputs_count, c.pointer(input_struct), c.sizeof(input_struct)
        )
        return extra

    @staticmethod
    def __key_up() -> c.c_ulong:
        """Запускает событие отпускание клавиши"""
        inputs_count = c.c_ulong(1)
        extra = c.c_ulong(0)
        unit = INPUTUNIT()
        unit.ki = KEYBDINPUT(
            c.c_ushort(SoundVirtualKeys.MUTE.value),
            c.c_ushort(0x48),
            c.c_ulong(KeyEventFlags.KEY_UP.value),
            c.c_ulong(0),
            c.pointer(extra),
        )
        input_struct = INPUT(c.c_ulong(1), unit)
        SoundHandler.send_input(
            inputs_count, c.pointer(input_struct), c.sizeof(input_struct)
        )
        return extra

    @staticmethod
    def __input_key() -> c.c_ulong:
        """Последовательно запускает события нажатия на клавишу и отпускания клавиши"""
        ex1 = SoundHandler.__key_down()
        ex2 = SoundHandler.__key_up()

        if ex1.value != int(0):
            return ex1
        elif ex2.value != int(0):
            return ex2
        else:
            return ex1

    @staticmethod
    def mute() -> bool:
        """Блокирует / возобновляет звук"""
        return SoundHandler.__input_key().value == int(0)

    @staticmethod
    def error() -> int:
        """Возвращает код последней ошибки в WinAPI"""
        import win32api

        return win32api.GetLastError()


class KEYBDINPUT(c.Structure):
    _fields_ = [
        ("wVk", c.c_ushort),
        ("wScan", c.c_ushort),
        ("dwFlags", c.c_ulong),
        ("time", c.c_ulong),
        ("dwExtraInfo", SoundHandler.ptr),
    ]


class HARDWAREINPUT(c.Structure):
    _fields_ = [("Msg", c.c_ulong), ("ParamL", c.c_ushort), ("ParamH", c.c_ushort)]


class MOUSEINPUT(c.Structure):
    _fields_ = [
        ("X", c.c_long),
        ("Y", c.c_long),
        ("MouseData", c.c_ulong),
        ("Flags", c.c_ulong),
        ("Time", c.c_ulong),
        ("ExtraInfo", SoundHandler.ptr),
    ]


class INPUTUNIT(c.Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT), ("hi", HARDWAREINPUT)]


class INPUT(c.Structure):
    _fields_ = [("type", c.c_ulong), ("unit", INPUTUNIT)]


class SoundVirtualKeys(Enum):
    MUTE = 0xAD
    DOWN = 0xAE
    UP = 0xAF


class KeyEventFlags(Enum):
    KEY_DOWN = 0x0000
    KEY_UP = 0x0002
