from pathlib import Path
import json
import sys

# def get_core_dir():
#     code_dir = Path("/mnt/ala/mav/2026/sandbox/friday_short_film/pixie_dust/pixie-dust")
#     return code_dir

# def get_config_path(core_dir):
#     config_path = core_dir / "config.json"

#     return config_path

from env_vars import CONFIG_PATH

def _load_config():
    try:
        with open(str(CONFIG_PATH), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")
    except Exception as e:
        raise RuntimeError(f"Failed to read config file {CONFIG_PATH}: {e}")

def get_main_workspace_path():
    config_data = _load_config()
    try:
        main_workspace_path = Path(config_data["main_workspace_path"])
    except KeyError:
        raise KeyError(f"Missing key 'main_workspace_path' in config {CONFIG_PATH}. Available keys: {list(config_data.keys())}")

    return main_workspace_path

def get_assignment_data_path():
    config_data = _load_config()
    try:
        assignment_data_path = Path(config_data["assignment_data_path"])
    except KeyError:
        raise KeyError(f"Missing key 'assignment_data_path' in config {CONFIG_PATH}. Available keys: {list(config_data.keys())}")

    return assignment_data_path

def get_assignment_data():
    assignment_data_path = get_assignment_data_path()

    try:
        with open(str(assignment_data_path), 'r') as file:
            assignment_data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Assignment data file not found at {assignment_data_path}")

    return assignment_data

def get_users_data():
    config_data = _load_config()
    try:
        users_data_path = Path(config_data["users_data_path"])
    except KeyError:
        raise KeyError(f"Missing key 'users_data_path' in config {CONFIG_PATH}. Available keys: {list(config_data.keys())}")

    try:
        with open(str(users_data_path), 'r') as file:
            users_data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Users data file not found at {users_data_path}")

    return users_data

def get_users():
    users_data = get_users_data()

    users = []

    for uid_info in users_data.values():
        users.append(uid_info["name"])

    return users

def get_user_name(uid: str):
    users_data = get_users_data()

    user_name = users_data[uid]["name"]

    return user_name

def get_uid(name: str):
    users_data = get_users_data()

    for uid, data in users_data.items():
        if data["name"] == name:
            return uid
    
    raise ValueError("Wrong UID provided")

# ---------------------------FOLDER CREATION ----------------------------

def create_asset_folders(main_workspace_path: Path, asset_type: str, asset_name: str):
    asset_path = main_workspace_path / "assets" / asset_type / asset_name
    asset_path.mkdir()

    asset_parts = []

    if asset_type == "audio":
        asset_parts = ["audio"]
    elif asset_type == "camera":
        asset_parts = ["layout", "rig"]
    elif asset_type == "character":
        asset_parts = ["animation", "art", "charfx", "model", "rig", "surfacing"]
    elif asset_type == "charfx":
        asset_parts = ["charfx"]
    elif asset_type == "fx":
        asset_parts = ["art", "fx", "model", "rig", "surfacing"]
    elif asset_type == "lighting":
        asset_parts = ["lighting"]
    elif asset_type == "mattePainting":
        asset_parts = ["mattePainting"]
    elif asset_type == "prop":
        asset_parts = ["art", "model", "rig", "surfacing"]
    elif asset_type == "set":
        asset_parts = ["art", "model", "surfacing"]
    elif asset_type == "setPiece":
        asset_parts = ["art", "fx", "model", "surfacing"]

    for asset_part in asset_parts:
        asset_part_path = asset_path / asset_part
        asset_part_path.mkdir()
        publishes_path = asset_part_path / "publishes"
        publishes_path.mkdir()
        wip_path = asset_part_path / "wip"
        wip_path.mkdir()

def create_shot_folders(shot_path: Path):
    shot_path.mkdir()

    departments = ["animation", "charfx", "comp", "editorial", "fx", "layout", "light"]
    for department in departments:
        shot_department_path = shot_path / department
        shot_department_path.mkdir()

def create_shot_task_folders(shot_task_path: Path):
    shot_task_path.mkdir()

    publishes_path = shot_task_path / "publishes"
    publishes_path.mkdir()
    
    wip_path = shot_task_path / "wip"
    wip_path.mkdir()
