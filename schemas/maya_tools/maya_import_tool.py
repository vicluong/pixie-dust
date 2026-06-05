from pathlib import Path
import sys


core_path = Path("/mnt/ala/mav/2026/sandbox/friday_short_film/pixie_dust/pixie-dust/core/")

if str(core_path) not in sys.path:
    sys.path.append(str(core_path))


from ui.import_ui import ImportDialog
from dcc_manager.dcc_manager import DCCManager


dcc_interface = DCCManager("maya").dcc_interface
ImportDialog.show_dialog(dcc_interface)
