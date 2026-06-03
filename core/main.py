from pathlib import Path

from dcc_manager.dcc_manager import DCCManager


def start_up(dcc: str):
    dcc_manager = DCCManager(dcc)
    dcc_manager.create_ui()
