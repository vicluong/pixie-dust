from pathlib import Path
import json
import sys

def get_code_dir():
    code_dir = Path("F:\\ALA Projects\\Pixie Dust\\sheeping_beauty\\pixie-dust")
    return code_dir

def path_append_code_dir():
    sys.path.append(str(get_code_dir()))

def get_main_folder_path():
    config_path = get_code_dir() / "config.json"

    with open(str(config_path), 'r') as file:
        config_data = json.load(file)
        main_folder_path = Path(config_data["main_folder_path"])

    return main_folder_path

def get_assignment_data():
    config_path = get_code_dir() / "config.json"

    with open(str(config_path), 'r') as file:
        config_data = json.load(file)
        assignment_data_path = Path(config_data["assignment_data_path"])

    with open(str(assignment_data_path), 'r') as file:
        assignment_data = json.load(file)

    return assignment_data

def get_users_data():
    config_path = get_code_dir() / "config.json"

    with open(str(config_path), 'r') as file:
        config_data = json.load(file)
        users_data_path = Path(config_data["users_data_path"])

    with open(str(users_data_path), 'r') as file:
        users_data = json.load(file)

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

def create_asset_folders(main_folder_path: Path, asset_type: str, asset_name: str):
    asset_path = main_folder_path / "assets" / asset_type / asset_name
    asset_path.mkdir()

    asset_parts = []

    if asset_type == "camera":
        asset_parts = ["layout", "rig"]
    elif asset_type == "character":
        asset_parts = ["animation", "art", "charfx", "model", "rig", "surfacing"]
    elif asset_type == "charfx":
        asset_parts = ["charfx"]
    elif asset_type == "fx":
        asset_parts = ["art", "fx", "model", "rig", "surfacing"]
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

    shot_assets_path = shot_path / "assets"
    shot_assets_path.mkdir()

    asset_types = ["audio", "camera", "character", "charfx", "fx", "lighting", "mattePainting", "production", "prop", "set", "setPiece", "vehicle"]
    for asset_type in asset_types:
        shot_asset_path = shot_assets_path / asset_type
        shot_asset_path.mkdir()

    shot_departments_path = shot_path / "departments"
    shot_departments_path.mkdir()

    departments = ["animation", "charfx", "comp", "editorial", "fx", "layout", "light"]
    for department in departments:
        shot_department_path = shot_departments_path / department
        shot_department_path.mkdir()

def create_shot_task_folders(shot_task_path: Path):
    shot_task_path.mkdir()

    publishes_path = shot_task_path / "publishes"
    publishes_path.mkdir()
    
    wip_path = shot_task_path / "wip"
    wip_path.mkdir()
