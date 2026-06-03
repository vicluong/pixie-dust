from pathlib import Path
import sys


core_path = Path("F:\\ALA Projects\\Pixie Dust\\sheeping_beauty\\pixie-dust\\core")

if str(core_path) not in sys.path:
    sys.path.append(str(core_path))

config_path = Path("F:\\ALA Projects\\Pixie Dust\\sheeping_beauty\\pixie-dust\\config.json")

import main
main.start_up("maya")
