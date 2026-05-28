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

import utils.file_folder_utils as ffu

def get_main_window() -> QtWidgets.QWidget:
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class SaveDialog(QtWidgets.QDialog):
    dlg_instance = None

    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = SaveDialog()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self):
        super(SaveDialog, self).__init__(get_main_window())

        self.setWindowTitle("File Save")

        size = get_main_window().screen().size()
        screen_w, screen_h = size.width(), size.height()
        self.resize(int(screen_w * 0.22), int(screen_h * 0.18))

        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.Tool, True)

        self.create_widgets()
        self.create_layout()
        self.create_connections()
        self.update_filename_preview()

    def create_widgets(self):
        self.title_label = QtWidgets.QLabel("File Save")

        self.name_label = QtWidgets.QLabel("Name")
        self.name_edit = QtWidgets.QLineEdit("scene")

        self.version_label = QtWidgets.QLabel("Version")
        self.version_spin = QtWidgets.QSpinBox()
        self.version_spin.setMinimum(1)
        self.version_spin.setValue(1)
        self.version_spin.setMaximum(9999)
        self.version_spin.setEnabled(False)
        self.next_version_check = QtWidgets.QCheckBox(
            "Use Next Available Version"
        )
        self.next_version_check.setChecked(True)

        self.filetype_label = QtWidgets.QLabel("File Type")
        self.filetype_combo = QtWidgets.QComboBox()
        self.filetype_combo.addItems([
            "Maya Binary (.mb)",
            "Maya ASCII (.ma)"
        ])

        self.preview_label = QtWidgets.QLabel("Preview")
        self.preview_edit = QtWidgets.QLineEdit()
        self.preview_edit.setReadOnly(True)

        self.workarea_label = QtWidgets.QLabel("Work Area")
        self.workarea_edit = QtWidgets.QLineEdit()
        self.workarea_edit.setReadOnly(True)
        self.workarea_edit.setText("C:/template/test/wip")

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

        form_layout.addRow(self.filetype_label, self.filetype_combo)
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
        self.filetype_combo.currentIndexChanged.connect(self.update_filename_preview)

        self.next_version_check.toggled.connect(self.toggle_version_spin)

        self.cancel_btn.clicked.connect(self.close)
        self.save_btn.clicked.connect(self.save_file)

    def toggle_version_spin(self):
        self.version_spin.setEnabled(
            not self.next_version_check.isChecked()
        )

    def update_filename_preview(self):
        name = self.name_edit.text() or "scene"
        version = self.version_spin.value()

        extension = ".mb"
        if "ASCII" in self.filetype_combo.currentText():
            extension = ".ma"

        filename = f"{name}_v{version:04}{extension}"

        self.preview_edit.setText(filename)

    def save_file(self):
        path = self.preview_edit.text()

        ffu.verify_file(Path(cmds.file(q=True, sceneName=True)), "wip", ".mb")
        # Make this non-reliant on maya

        cmds.confirmDialog(
            title="Saved",
            message=f"Saved:\n{path}",
            button=["OK"]
        )

        self.close()


if __name__ == "__main__":
    SaveDialog.show_dialog()
