from pathlib import Path

from dcc_manager.dcc_manager import DCCManager


def start_up(config_path: Path, dcc: str):
    dcc_manager = DCCManager(config_path, dcc)
    dcc_manager.create_ui()
