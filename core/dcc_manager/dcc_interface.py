from abc import ABC, abstractmethod

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets


class DCCInterface(ABC):
    @abstractmethod
    def get_main_window(self) -> QtWidgets.QWidget:
        pass
