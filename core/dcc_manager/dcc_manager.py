from pathlib import Path

from ui.pixie_dust_ui import PixieDustDialog


class DCCManager:
    """Interface for DCC operations."""
    def __init__(self, dcc: str):
        # self.config_path = config_path
        dcc_key = dcc.lower()
        self.dcc_interface = self._get_dcc_interface(dcc_key)

        if not self.dcc_interface:
            raise ModuleNotFoundError("The specificed DCC could not be imported properly.")

    def create_ui(self):
        PixieDustDialog.show_dialog(self.dcc_interface)

    def _get_dcc_interface(self, dcc: str):
        if dcc == "maya":
            from dcc_manager.maya.maya_interface import MayaInterface
            return MayaInterface()
        elif dcc == "houdini":
            from dcc_manager.houdini.houdini_interface import HoudiniInterface
            return HoudiniInterface()
        # elif dcc == "nuke":
        #     from nuke_pipeline.netcopy_nuke import NukeNetCopy
        #     return NukeInterface()
        else:
            raise ValueError(f"DCC '{dcc}' is not supported by DCCManager.")
