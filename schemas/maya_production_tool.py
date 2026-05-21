from pathlib import Path
import sys

code_dir = Path("F:\\ALA Projects\\Pixie Dust\\sheeping_beauty\\pixie-dust\\core")

if str(code_dir) not in sys.path:
    sys.path.append(str(code_dir))

import main
main.start_up("maya")
