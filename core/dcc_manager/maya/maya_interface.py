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
    
    def verify_file(self) -> str:
        pass

    def create_new_asset_file(self, asset_name: str, asset_type: str, asset_part: str) -> str:
        cmds.file(new=True)
        main_folder_path = ffu.get_main_folder_path()
        file_path = str(main_folder_path / "assets" / asset_type / asset_name / asset_part 
                        / "wip" / f"{asset_name}_{asset_type}_{asset_part}_v000.mb")

        cmds.file(rename=f"{str(file_path)}")

        return str(file_path)

    def save_file(self) -> str:
        pass

    def publish_file(self) -> str:
        pass
