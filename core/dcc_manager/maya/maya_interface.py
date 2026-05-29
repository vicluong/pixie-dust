from pathlib import Path
import re

try:
    from PySide6 import QtWidgets
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

from dcc_manager.dcc_interface import DCCInterface
import utils.file_folder_utils as ffu

class MayaInterface(DCCInterface):
    def get_main_window(self) -> QtWidgets.QWidget:
        main_window_ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

    def get_asset_files(self, asset_name: str, asset_type: str, asset_part: str, parent_folder: str) -> list[str]:
        main_folder_path = ffu.get_main_folder_path()
        folder = Path(main_folder_path) / "assets" / asset_type / asset_name / asset_part / parent_folder

        pattern = re.compile(r"_v(\d{4})\.mb$")

        versions = []

        for file in folder.iterdir():
            match = pattern.search(file.name)
            if match:
                versions.append((int(match.group(1)), file))

        versions.sort(key=lambda x: x[0])
        sorted_files = [f for _, f in versions]

        return sorted_files

    def create_new_asset_file(self, asset_name: str, asset_type: str, asset_part: str) -> str:
        cmds.file(new=True)
        main_folder_path = ffu.get_main_folder_path()
        file_path = str(main_folder_path / "assets" / asset_type / asset_name / asset_part 
                        / "wip" / f"{asset_name}_{asset_type}_{asset_part}_v0000.mb")

        cmds.file(rename=f"{str(file_path)}")

        return str(file_path)
    
    def get_file_extensions(self) -> list[str]:
        extensions = [".mb", ".ma"]

        return extensions

    def get_scene_name(self) -> str:
        return cmds.file(q=True, sn=True, shn=True)

    def get_scene_folder(self) -> Path:
        scene_folder = Path(cmds.file(q=True, sceneName=True)).parent

        return scene_folder

    def verify_file(self, file_state_folder: str) -> bool:
        scene_path = Path(cmds.file(q=True, sceneName=True))

        main_folder_path = ffu.get_main_folder_path()
        relative_path = scene_path.relative_to(main_folder_path)
        relative_parts = relative_path.parts

        file_name = relative_path.name
        file_parts = file_name.split("_")

        file_ext = scene_path.suffix
        file_stem = scene_path.stem.split("_")[-1]

        if relative_parts[0] == "assets":
            # Check relative folders match with the file name
            if file_parts[0] == relative_parts[2] and file_parts[1] == relative_parts[1] and  file_parts[2] == relative_parts[3] and relative_parts[4] == file_state_folder:
                # Check if the version and file type are correct
                if file_stem[0] == "v" and len(file_stem[1:]) == 4 and file_stem[1:].isdigit() and file_ext in self.get_file_extensions():
                    return True
        elif relative_parts[0] == "sequences":
            return
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "File Verification Error",
                "Are you sure your file is within either the main assets or sequences folders?"
            )
            return False

    # Usually performed after verify_file or before save_file
    def get_next_available_version(self) -> int:
        scene_path = Path(cmds.file(q=True, sceneName=True))
        task_folder = scene_path.parent

        pattern = re.compile(r"_v(\d{4})$")

        latest_version = -1

        for file in task_folder.iterdir():
            version_match = pattern.search(file.stem)

            if version_match and file.suffix in self.get_file_extensions():
                version = int(version_match.group(1))

                if version > latest_version:
                    latest_version = version

        return latest_version + 1

    def save_file(self, file_path: Path) -> str:
        if cmds.file(q=True, modified=True):
            cmds.file(rename=file_path)
            cmds.file(save=True)
            return file_path
        else:
            QtWidgets.QMessageBox.warning(
                None, 
                "Save Error", 
                f"Changes need to be made first before saving."
            )
            return

    def publish_file(self) -> str:
        pass

    def publish_file(self) -> str:
        pass
