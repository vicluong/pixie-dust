from pathlib import Path
import sys


core_path = Path("/mnt/ala/mav/2026/sandbox/friday_short_film/pixie_dust/pixie-dust/core/")

if str(core_path) not in sys.path:
    sys.path.append(str(core_path))

import main
main.start_up("maya")
