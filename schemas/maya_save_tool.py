from pathlib import Path
import sys

code_dir = Path("F:\\ALA Projects\\Pixie Dust\\sheeping_beauty\\pixie-dust\\core")

if str(code_dir) not in sys.path:
    sys.path.append(str(code_dir))

from ui.save_ui import SaveDialog
from dcc_manager.dcc_manager import DCCManager

dcc_manager = DCCManager("maya").dcc_interface
SaveDialog.show_dialog(dcc_manager)
