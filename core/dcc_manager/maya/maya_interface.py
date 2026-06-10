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
    # def __init__(self, config_path: str):
    #     super().__init__(config_path)

    def get_main_window(self) -> QtWidgets.QWidget:
        main_window_ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

    def get_native_asset_files(self, asset_type: str, asset_name: str, asset_step: str, file_state_folder: str) -> list[Path]:
        main_workspace_path = ffu.get_main_workspace_path()

        if file_state_folder == "publishes":
            folder = main_workspace_path / "assets" / asset_type / asset_name / asset_step / file_state_folder / "mb"
        elif file_state_folder == "wip":
            folder = main_workspace_path / "assets" / asset_type / asset_name / asset_step / file_state_folder
        else:
            QtWidgets.QMessageBox.warning(
                None, 
                "Asset Retrieval Error", 
                f"Invalid file state given."
            )
            return

        if folder.exists():
            pattern = re.compile(r"_v(\d{4})\.mb$")

            versions = []

            for file in folder.iterdir():
                match = pattern.search(file.name)
                if match:
                    versions.append((int(match.group(1)), file))

            versions.sort(key=lambda x: x[0])
            sorted_files = [f for _, f in versions]

            return sorted_files

    def get_native_shot_task_files(self, sequence: str, shot: str, step: str, task: str, file_state_folder: str) -> list[Path]:
        main_workspace_path = ffu.get_main_workspace_path()
        
        if file_state_folder == "publishes":
            folder = main_workspace_path / "sequences" / sequence / shot / step / task / file_state_folder / "mb"
        elif file_state_folder == "wip":
            folder = main_workspace_path / "sequences" / sequence / shot / step / task / file_state_folder
        else:
            QtWidgets.QMessageBox.warning(
                None, 
                "Asset Retrieval Error", 
                f"Invalid file state given."
            )
            return
        
        if folder.exists():
            pattern = re.compile(r"_v(\d{4})\.mb$")

            versions = []

            for file in folder.iterdir():
                match = pattern.search(file.name)
                if match:
                    versions.append((int(match.group(1)), file))

            versions.sort(key=lambda x: x[0])
            sorted_files = [f for _, f in versions]

            return sorted_files

    def create_new_asset_file(self, asset_type: str, asset_name: str, asset_step: str) -> str:
        if cmds.file(q=True, modified=True):
            result = cmds.confirmDialog(
                title="Save Changes",
                message="Save changes to the current scene before creating a new scene?",
                button=["Save", "Don't Save", "Cancel"],
                defaultButton="Save",
                cancelButton="Cancel",
            )
            if result == "Save":
                cmds.file(save=True)
                cmds.file(new=True, force=True)
            elif result == "Don't Save":
                cmds.file(new=True, force=True)
            else:
                return
        else:
            cmds.file(new=True, force=True)

        main_workspace_path = ffu.get_main_workspace_path()
        file_path = str(main_workspace_path / "assets" / asset_type / asset_name / asset_step 
                        / "wip" / f"{asset_type}_{asset_name}_{asset_step}_v0000.mb")

        cmds.file(rename=f"{str(file_path)}")

        return str(file_path)
    
    def create_new_shot_task_file(self, sequence: str, shot: str, step: str, task: str) -> str:
        if cmds.file(q=True, modified=True):
            result = cmds.confirmDialog(
                title="Save Changes",
                message="Save changes to the current scene before creating a new scene?",
                button=["Save", "Don't Save", "Cancel"],
                defaultButton="Save",
                cancelButton="Cancel",
            )
            if result == "Save":
                cmds.file(save=True)
                cmds.file(new=True, force=True)
            elif result == "Don't Save":
                cmds.file(new=True, force=True)
            else:
                return
        else:
            cmds.file(new=True, force=True)
        
        main_workspace_path = ffu.get_main_workspace_path()
        file_path = str(main_workspace_path / "sequences" / sequence / shot / step / task
                        / "wip" / f"{sequence}_{shot}_{step}_{task}_v0000.mb")

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

    def verify_file(self) -> bool:
        if not (cmds.file(q=True, sceneName=True)):
            QtWidgets.QMessageBox.warning(
                None,
                "Verification Error",
                "Ensure you are saving a non-empty scene."
            )
            return False

        scene_path = Path(cmds.file(q=True, sceneName=True))

        main_workspace_path = ffu.get_main_workspace_path()
        relative_path = scene_path.relative_to(main_workspace_path)
        relative_parts = relative_path.parts

        file_name = relative_path.name
        file_parts = file_name.split("_")

        file_ext = scene_path.suffix
        file_stem = scene_path.stem.split("_")[-1]

        if relative_parts[0] == "assets":
            # Check relative folders match with the file name
            if file_parts[0] == relative_parts[1] and file_parts[1] == relative_parts[2] and file_parts[2] == relative_parts[3] and "wip" == relative_parts[4]:
                # Check if the version and file type are correct
                if file_stem[0] == "v" and len(file_stem[1:]) == 4 and file_stem[1:].isdigit() and file_ext in self.get_file_extensions():
                    return True
        elif relative_parts[0] == "sequences":
            # Check relative folders match with the file name
            if file_parts[0] == relative_parts[1] and file_parts[1] == relative_parts[2] and file_parts[2] == relative_parts[3] and  file_parts[3] == relative_parts[4] and "wip" == relative_parts[5]:
                # Check if the version and file type are correct
                if file_stem[0] == "v" and len(file_stem[1:]) == 4 and file_stem[1:].isdigit() and file_ext in self.get_file_extensions():
                    return True
        else:
            QtWidgets.QMessageBox.warning(
                None,
                "File Verification Error",
                "Ensure your file is within either the main assets or sequences folders and is a WIP file."
            )
            return False
        return False

    def get_parent_folder_from_scene(self) -> Path:
        scene_path = Path(cmds.file(q=True, sceneName=True))
        task_wip_folder_path = scene_path.parent

        return task_wip_folder_path

    # Usually performed after verify_file or before save_file
    def get_next_available_version(self, folder_path) -> int:
        pattern = re.compile(r"_v(\d{4})$")

        latest_version = -1

        for file in folder_path.iterdir():
            version_match = pattern.search(file.stem)

            if version_match and file.suffix in self.get_file_extensions():
                version = int(version_match.group(1))

                if version > latest_version:
                    latest_version = version

        return latest_version + 1

    def open_file(self, file_path: Path) -> None:
        if not file_path:
            QtWidgets.QMessageBox.warning(
                None, 
                "Open Error", 
                f"Ensure there is a valid file path to open."
            )
            return
        if cmds.file(q=True, modified=True):
            result = cmds.confirmDialog(
                title="Save Changes",
                message="Save changes to the current scene?",
                button=["Save", "Don't Save", "Cancel"],
                defaultButton="Save",
                cancelButton="Cancel",
            )
            if result == "Save":
                cmds.file(save=True)
                cmds.file(str(file_path), open=True, force=True)
            elif result == "Don't Save":
                cmds.file(str(file_path), open=True, force=True)
        else:
            cmds.file(str(file_path), open=True)

    def save_file(self, file_path: Path) -> bool:
        print(file_path)
        if not file_path:
            QtWidgets.QMessageBox.warning(
                None, 
                "Open Error", 
                f"Ensure there is a valid file path to open."
            )
            return
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

    def get_publish_file_extensions(self) -> dict[str, tuple[str, bool, bool]]:
        """Get the publish file extensions and additional info for the UI

        Returns:
            dict[str, tuple[str, bool, bool]]: Key is file extension while value is a tuple containing
                what the file extension is then if is_locked then is_checked
        """
        file_types = {
            ".mb": ("Maya Binary Scene", True, True),
            ".usd": ("Universal Scene Description", False, True),
            ".fbx": ("FBX Exchange Format", False, False),
            # ".abc": "Alembic Cache",
            ".obj": ("OBJ Geometry", False, False),
        }

        return file_types

    def publish_file(self, publishes_folder: Path, extension: str) -> bool:
        if cmds.file(q=True, modified=True):
            QtWidgets.QMessageBox.warning(
                None, 
                "Publish Error", 
                f"Ensure that you have saved the scene and that there are no modifications that need to be saved."
            )
            return
        if extension == ".mb":
            folder_ext_path = publishes_folder / "mb"
            if not folder_ext_path.exists():
                folder_ext_path.mkdir()

            file_path = folder_ext_path / (self.get_scene_name().split(".")[0] + ".mb")
            cmds.file(str(file_path), exportAll=True, force=True, type="mayaBinary")

            latest_file_path = folder_ext_path / (self.get_scene_name().rsplit("_", 1)[0] + "_latest.mb")
            cmds.file(str(latest_file_path), exportAll=True, force=True, type="mayaBinary")

        elif extension == ".usd":
            cmds.loadPlugin("mayaUsdPlugin", quiet=True)
            folder_ext_path = publishes_folder / "usd"
            if not folder_ext_path.exists():
                folder_ext_path.mkdir()
            file_path = folder_ext_path / (self.get_scene_name().split(".")[0])
            cmds.mayaUSDExport(
                file=file_path,
            )

            latest_file_path = folder_ext_path / (self.get_scene_name().rsplit("_", 1)[0] + "_latest")
            cmds.mayaUSDExport(
                file=latest_file_path,
            )

        elif extension == ".fbx":
            folder_ext_path = publishes_folder / "fbx"
            if not folder_ext_path.exists():
                folder_ext_path.mkdir()
            file_path = folder_ext_path / (self.get_scene_name().split(".")[0] + ".fbx")
            cmds.file(str(file_path), exportAll=True, force=True, type="FBX export")

            latest_file_path = folder_ext_path / (self.get_scene_name().rsplit("_", 1)[0] + "_latest.fbx")
            cmds.file(str(latest_file_path), exportAll=True, force=True, type="FBX export")

        elif extension == ".obj":
            folder_ext_path = publishes_folder / "obj"
            if not folder_ext_path.exists():
                folder_ext_path.mkdir()
            file_path = folder_ext_path / (self.get_scene_name().split(".")[0] + ".obj")
            cmds.file(str(file_path), exportAll=True, force=True, type="OBJexport")

            latest_file_path = folder_ext_path / (self.get_scene_name().rsplit("_", 1)[0] + "_latest.obj")
            cmds.file(str(latest_file_path), exportAll=True, force=True, type="OBJexport")

        else:
            return False
        return True
    
    def get_latest_published_files(self, asset_name: str, asset_type: str, asset_step: str) -> list[tuple[Path, Path]]:
        main_workspace_path = ffu.get_main_workspace_path()
        publishes_path = main_workspace_path / "assets" / asset_type / asset_name / asset_step / "publishes"

        latest_files = []

        for exts_folder in publishes_path.iterdir():
            if exts_folder.is_dir():
                latest_file = next(
                    (p for p in exts_folder.glob("*_latest.*") if p.suffix != ".mtl"),
                    None,
                )
                latest_ver = max(
                    (p for p in exts_folder.glob("*_v*") if p.suffix != ".mtl"),
                    key=lambda p: int(p.stem.rpartition("_v")[2]),
                    default=None,
                )
                if latest_file and latest_ver:
                    latest_files.append((latest_file, latest_ver))

        return latest_files

    def import_file(self, file: Path) -> None:
        if file.exists():
            if file.suffix == "usd":
                if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
                    cmds.loadPlugin("mayaUsdPlugin")
                cmds.mayaUSDImport(file=file, primPath="/")
            else:
                cmds.file(str(file), i=True)
        else:
            QtWidgets.QMessageBox.warning(
                None, 
                "Import Error", 
                f"Invalid file given for importing."
            )
            return

    def reference_file(self, file: Path) -> None:
        if file.exists():
            if file.suffix == ".usd":
                if not cmds.pluginInfo("mayaUsdPlugin", query=True, loaded=True):
                    cmds.loadPlugin("mayaUsdPlugin")

                usd_shapes = cmds.ls(type="mayaUsdProxyShape") or []
                ref_paths = [Path(cmds.getAttr(f"{shape}.filePath")) for shape in usd_shapes]
                if file in ref_paths:
                    QtWidgets.QMessageBox.warning(
                        None, 
                        "Reference Error", 
                        f"USD Stage already loaded: {file.name}"
                    )
                    return

                task = file.stem.split("_")[1]
                proxy_shape = cmds.createNode("mayaUsdProxyShape", name=f"{task}StageShape")
                cmds.setAttr(f"{proxy_shape}.filePath", file, type="string")
                parent_transform = cmds.listRelatives(proxy_shape, parent=True)[0]
                cmds.rename(parent_transform, f"{task}Stage")
            elif file.suffix == ".mb":
                existing_refs = cmds.file(query=True, reference=True) or []
                ref_paths = [Path(ref) for ref in existing_refs]

                if file in ref_paths:
                    QtWidgets.QMessageBox.warning(
                        None, 
                        "Reference Error", 
                        f"Maya file is already referenced: {file.name}"
                    )
                    return
                else:
                    cmds.file(file, reference=True)
            else:
                QtWidgets.QMessageBox.warning(
                None, 
                "Reference Error", 
                f"Unable to reference file of this type. Choose either .mb or .usd"
            )
            return
        else:
            QtWidgets.QMessageBox.warning(
                None, 
                "Reference Error", 
                f"Invalid file given for referencing."
            )
            return
