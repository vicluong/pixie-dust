from abc import ABC, abstractmethod

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets


class DCCInterface(ABC):
    @abstractmethod
    def get_main_window(self) -> QtWidgets.QWidget:
        pass

    @abstractmethod
    def create_new_file(self) -> str:
        pass

    @abstractmethod
    def save_file(self) -> str:
        pass

    @abstractmethod
    def publish_file(self) -> str:
        pass
