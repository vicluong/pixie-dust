from pathlib import Path
import sys


core_path = Path("F:\\ALA Projects\\Pixie Dust\\sheeping_beauty\\pixie-dust\\core")

if str(core_path) not in sys.path:
    sys.path.append(str(core_path))


from ui.save_ui import SaveDialog
from dcc_manager.dcc_manager import DCCManager


config_path = Path("F:\\ALA Projects\\Pixie Dust\\sheeping_beauty\\pixie-dust\\config.json")

dcc_interface = DCCManager(config_path, "maya").dcc_interface
SaveDialog.show_dialog(dcc_interface)
