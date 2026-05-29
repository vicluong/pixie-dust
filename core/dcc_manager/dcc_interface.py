from abc import ABC, abstractmethod
from pathlib import Path

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets


class DCCInterface(ABC):
    @abstractmethod
    def get_main_window(self) -> QtWidgets.QWidget:
        pass

    @abstractmethod
    def get_asset_files(self, asset_name: str, asset_type: str, asset_part: str, parent_folder: str) -> list[Path]:
        pass

    @abstractmethod
    def get_shot_task_files(self, sequence: str, shot: str, department: str, task: str, parent_folder: str) -> list[Path]:
        pass

    @abstractmethod
    def create_new_asset_file(self, asset_name: str, asset_type: str, asset_part: str) -> str:
        pass

    @abstractmethod
    def get_file_extensions(self) -> list[str]:
        pass

    @abstractmethod
    def get_scene_name(self) -> str:
        pass

    @abstractmethod
    def get_scene_folder(self) -> Path:
        pass

    @abstractmethod
    def verify_file(self) -> bool:
        pass

    @abstractmethod
    def get_next_available_version(self) -> int:
        pass

    @abstractmethod
    def open_file(self, file_path: Path) -> None:
        pass

    @abstractmethod
    def save_file(self, file_path: Path) -> bool:
        pass

    @abstractmethod
    def publish_file(self, file_path: Path) -> bool:
        pass
