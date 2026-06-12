from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
# Allow overriding the config path with an environment variable for different mounts/hosts
env_config = os.environ.get("PIXIE_CONFIG_PATH")
if env_config:
	CONFIG_PATH = Path(env_config)
else:
	CONFIG_PATH = Path(r"F:\ALA Projects\Pixie Dust\sheeping_beauty\pixie-dust\config_venom\config.json")
