try:
    from PySide6 import QtWidgets
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtWidgets
    from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

from ..dcc_interface import DCCInterface


class MayaInterface(DCCInterface):
    def get_main_window(self) -> QtWidgets.QWidget:
        main_window_ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
