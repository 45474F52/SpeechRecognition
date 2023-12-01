from enum import Enum
import win32gui


class CloseWindowMessages(Enum):
    """
    Предоставляет и описывает сообщения для закрытия окна и освобождения ресурсов
    """

    WM_DESTROY = 0x0002
    """
    Отправляется при уничтожении окна ему и его дочерним окнам.

    Используется для освобождения выделенного объекта памяти, связанного с окном.
    """
    WM_NCDESTROY = 0x0082
    """
    Уведомляет окно о том, что его неклиентская область уничтожается.
    Отправляется после сообщения WM_DESTROY (после уничтожения дочерних окон).

    Ипользуется для освобождения всех ресурсов памяти, выделенных для окна
    """


class WindowStates(Enum):
    """
    Флаги состояний окон
    """

    HIDE = 0
    """Скрывает окно и активирует другое"""
    NORMAL = 1
    """
    Активирует и отображает окно
    Если окно в состоянии MINIMIZED или MAXIMIZED система сбросит состояние и позицию окна до исходного
    Указывается при отображении окна в первый раз
    """
    SHOWNORMAL = 1
    """Эквиваленто значению NORMAL"""
    SHOWMINIMIZED = 2
    """Активирует окно и отображает его в состоянии MINIMIZED"""
    MAXIMIZED = 3
    """Активирует окно и разворачивает его на весь экран"""
    SHOWMAXIMIZED = 3
    """Эквивалентно значению MAXIMIZED"""
    SHOWNOACTIVE = 4
    """
    Отображает окно с его последними значениями размера и положения
    Эквивалентно значению NORMAL, но окно не активируется
    """
    SHOW = 5
    """Активирует окно и отображает его с его текущими значениями размера и положения"""
    MINIMIZE = 6
    """Сворачивает окно и активирует следующее окно по Z-индексу"""
    SHOWMINNOACTIVE = 7
    """
    Отображает окно в состоянии MINIMIZED
    Эквивалентно значению SHOWMINIMIZED, но окно не активируется
    """
    SHOWNA = 8
    """
    Отображает окно с его текущими значениями размера и положения
    Эквивалентно значению SHOW, но окно не активируется
    """
    RESTORE = 9
    """
    Активирует и отображает окно
    Если окно в состоянии MINIMIZED или MAXIMIZED система сбросит состояние и позицию окна до исходного
    Указывается при восстановлении свёрнутого окна
    """
    FORCEMINIMIZE = 11
    """
    Сворачивает окно, даже если поток, которому оно пренадлежит, не отвечает
    Используется только при сворачивании окон из другого потока
    """


class WindowsHandler:
    """
    Определяет команды управления окнами с использованием библиотек WinAPI
    """

    __console_hwnd = 0
    """Дескриптор окна консоли"""

    @staticmethod
    def __init_hwnd() -> None:
        """Получает дескриптор окна консоли приложения"""
        if WindowsHandler.__console_hwnd == 0:
            WindowsHandler.__console_hwnd = win32gui.GetForegroundWindow()

    def __init__(self) -> None:
        WindowsHandler.__init_hwnd()

    def close_active_window(self) -> bool:
        """
        Получает дескриптор активного окна и освобождает его ресурсы
        """
        return self.__close_window(win32gui.GetForegroundWindow())

    def __close_window(self, hwnd: int) -> bool:
        """
        Закрывает окно по переданному дескриптору и освобождает ресурсы
        """
        result1 = win32gui.SendMessage(
            hwnd, CloseWindowMessages.WM_DESTROY.value, None, None
        )
        # Открытые ранее окна перестанут быть доступны, даже если отображаются на панели задач
        # result2 = win32gui.SendMessage(hwnd, CloseWindowMessages.WM_NCDESTROY.value, None, None)

        if result1 == 0:
            return True
        else:
            return False

    def hide_console(self) -> None:
        """Скрывает консоль приложения"""
        self.__set_window_state(WindowsHandler.__console_hwnd, WindowStates.HIDE)

    def show_console(self) -> None:
        """Заново отображает консоль приложения после скрытия"""
        self.__set_window_state(WindowsHandler.__console_hwnd, WindowStates.SHOW)

    def __set_window_state(self, hwnd: int, state: WindowStates) -> bool:
        """
        Устанавливает флаг состояния окна
        :param hwnd: дескриптор окна
        :param state: флаг состояния окна
        :return: Возвращает False, если окно скрыто, иначе True
        """
        result = win32gui.ShowWindow(hwnd, state.value)
        return result == 0
