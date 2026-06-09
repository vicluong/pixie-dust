from abc import ABC, abstractmethod
from pathlib import Path

try:
    from PySide6 import QtWidgets
except ImportError:
    from PySide2 import QtWidgets


class DCCInterface(ABC):
    # def __init__(self, config_path: str):
    #     self.config_path = config_path

    @abstractmethod
    def get_main_window(self) -> QtWidgets.QWidget:
        pass

    @abstractmethod
    def get_native_asset_files(self, asset_name: str, asset_type: str, asset_part: str, file_state_folder: str) -> list[Path]:
        pass

    @abstractmethod
    def get_native_shot_task_files(self, sequence: str, shot: str, department: str, task: str, file_state_folder: str) -> list[Path]:
        pass

    @abstractmethod
    def create_new_asset_file(self, asset_name: str, asset_type: str, asset_part: str) -> str:
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
    def get_parent_folder_from_scene(self) -> Path:
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
    def get_publish_file_extensions(self) -> dict[str, tuple[str, bool, bool]]:
        pass

    @abstractmethod
    def publish_file(self, publishes_folder: Path, extension: str) -> bool:
        pass

    @abstractmethod
    def get_latest_published_files(self, asset_name: str, asset_type: str, asset_part: str) -> list[tuple[Path, Path]]:
        pass

    @abstractmethod
    def import_file(self, file: Path) -> None:
        pass

    @abstractmethod
    def reference_file(self, file: Path) -> None:
        pass
