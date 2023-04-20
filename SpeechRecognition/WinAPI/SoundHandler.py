import ctypes as c
from enum import Enum


send_input = c.windll.user32.SendInput
ptr = c.POINTER(c.c_ulong)


class KEYBDINPUT(c.Structure):
    _fields_ = [
        ("wVk", c.c_ushort),
        ("wScan", c.c_ushort),
        ("dwFlags", c.c_ulong),
        ("time", c.c_ulong),
        ("dwExtraInfo", ptr),
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
        ("ExtraInfo", ptr),
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


def key_down() -> c.c_ulong:
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
    send_input(inputs_count, c.pointer(input_struct), c.sizeof(input_struct))
    return extra


def key_up() -> c.c_ulong:
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
    send_input(inputs_count, c.pointer(input_struct), c.sizeof(input_struct))
    return extra


def input_key() -> c.c_ulong:
    ex1 = key_down()
    ex2 = key_up()

    if ex1.value != c.c_ulong(0).value:
        return ex1
    elif ex2.value != c.c_ulong(0).value:
        return ex2
    else:
        return ex1


def mute() -> bool:
    """
    Блокирует / возобновляет звук
    """
    return input_key().value == c.c_ulong(0).value


def error() -> int:
    """
    Возвращает код последней ошибки в WinAPI
    """
    import win32api

    return win32api.GetLastError()
