from pathlib import Path
import json
import sys

try:
    from PySide6 import QtWidgets, QtCore
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtWidgets, QtCore
    from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

from dcc_manager.dcc_interface import DCCInterface


class SaveDialog(QtWidgets.QDialog):
    dlg_instance = None

    @classmethod
    def show_dialog(cls, dcc_interface: DCCInterface):
        if not cls.dlg_instance:
            cls.dlg_instance = SaveDialog(dcc_interface)

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self, dcc_interface: DCCInterface):
        super(SaveDialog, self).__init__()

        self.setWindowTitle("File Save")

        self.dcc_interface = dcc_interface
        self.main_window = self.dcc_interface.get_main_window()

        size = self.main_window.screen().size()
        screen_w, screen_h = size.width(), size.height()
        self.resize(int(screen_w * 0.3), int(screen_h * 0.18))

        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.Tool, True)

        self.scene_folder = self.dcc_interface.get_scene_folder()
        self.file_extensions = self.dcc_interface.get_file_extensions()

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.update_filename_preview()

    def create_widgets(self):
        self.title_label = QtWidgets.QLabel("File Save")

        self.name_label = QtWidgets.QLabel("Name")
        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.setReadOnly(True)

        self.version_label = QtWidgets.QLabel("Version")
        self.version_spin = QtWidgets.QSpinBox()
        self.version_spin.setMinimum(1)
        self.next_version = self.dcc_interface.get_next_available_version()
        self.version_spin.setValue(self.next_version)
        self.version_spin.setMaximum(9999)
        self.version_spin.setEnabled(False)
        self.next_version_check = QtWidgets.QCheckBox(
            "Use Next Available Version"
        )
        self.next_version_check.setChecked(True)

        # self.file_type_label = QtWidgets.QLabel("File Type")
        # self.file_type_combo = QtWidgets.QComboBox()
        # self.file_type_combo.addItems(self.file_extensions)

        self.preview_label = QtWidgets.QLabel("File Preview")
        self.preview_edit = QtWidgets.QLineEdit()
        self.preview_edit.setReadOnly(True)

        self.workarea_label = QtWidgets.QLabel("Work Area")
        self.workarea_edit = QtWidgets.QLineEdit()
        self.workarea_edit.setReadOnly(True)
        self.workarea_edit.setText(str(self.scene_folder))

        self.save_btn = QtWidgets.QPushButton("Save")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        main_layout.addWidget(self.title_label)

        form_layout = QtWidgets.QFormLayout()

        form_layout.addRow(self.name_label, self.name_edit)

        version_row = QtWidgets.QHBoxLayout()
        version_row.addWidget(self.version_spin)
        version_row.addWidget(self.next_version_check)

        form_layout.addRow(self.version_label, version_row)

        # form_layout.addRow(self.file_type_label, self.file_type_combo)
        form_layout.addRow(self.preview_label, self.preview_edit)
        form_layout.addRow(self.workarea_label, self.workarea_edit)

        main_layout.addLayout(form_layout)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)

        main_layout.addLayout(btn_layout)
        main_layout.addStretch()

    def create_connections(self):
        self.name_edit.textChanged.connect(self.update_filename_preview)
        self.version_spin.valueChanged.connect(self.update_filename_preview)
        # self.file_type_combo.currentIndexChanged.connect(self.update_filename_preview)

        self.next_version_check.toggled.connect(self.toggle_next_version_spin)

        self.cancel_btn.clicked.connect(self.close)
        self.save_btn.clicked.connect(self.save_file)

    def toggle_next_version_spin(self):
        self.version_spin.setEnabled(
            not self.next_version_check.isChecked()
        )

        if self.next_version_check.isChecked():
            self.next_version = self.dcc_interface.get_next_available_version()
            self.version_spin.setValue(self.next_version)

    def update_filename_preview(self):
        scene_name = self.dcc_interface.get_scene_name().rsplit("_", 1)[0]
        version = self.version_spin.value()

        extension = self.file_extensions[0]

        file_name = f"{scene_name}_v{version:04}{extension}"

        self.name_edit.setText(scene_name)
        self.preview_edit.setText(file_name)

    def save_file(self):
        path = self.scene_folder / self.preview_edit.text()

        if self.dcc_interface.verify_file("wip"):
            self.dcc_interface.save_file(path)

            cmds.confirmDialog(
                title="Saved",
                message=f"Saved:\n{path}",
                button=["OK"]
            )

            self.close()
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Save Error",
                "Current file failed verification."
            )
            return


if __name__ == "__main__":
    SaveDialog.show_dialog()
