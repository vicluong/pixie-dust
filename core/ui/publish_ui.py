from pathlib import Path
import sys

try:
    from PySide6 import QtWidgets, QtCore
except:
    from PySide2 import QtWidgets, QtCore

import maya.cmds as cmds

from dcc_manager.dcc_interface import DCCInterface


class PublishDialog(QtWidgets.QDialog):
    dlg_instance = None

    @classmethod
    def show_dialog(cls, dcc_interface: DCCInterface):
        if not cls.dlg_instance:
            cls.dlg_instance = PublishDialog(dcc_interface)

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self, dcc_interface: DCCInterface):
        super(PublishDialog, self).__init__()

        self.setWindowTitle("Publish Files")

        self.dcc_interface = dcc_interface
        self.main_window = self.dcc_interface.get_main_window()

        size = self.main_window.screen().size()
        screen_w, screen_h = size.width(), size.height()

        self.resize(int(screen_w * 0.3), int(screen_h * 0.25))

        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.Tool, True)

        self.scene_folder = self.dcc_interface.get_scene_folder()

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.title_label = QtWidgets.QLabel("Publish Export Files")

        # Preview path
        self.preview_label = QtWidgets.QLabel("Publish Path")
        self.preview_edit = QtWidgets.QLineEdit()
        self.preview_edit.setReadOnly(True)
        self.preview_edit.setText(str(self.scene_folder))

        # Export section
        self.export_label = QtWidgets.QLabel("Export Types")

        self.export_widget = QtWidgets.QWidget()
        self.export_layout = QtWidgets.QVBoxLayout(self.export_widget)

        self.export_layout.setContentsMargins(4, 4, 4, 4)
        self.export_layout.setSpacing(8)

        self.export_checkboxes = {}

        self.file_types = {
            ".ma": "Maya ASCII Scene",
            ".mb": "Maya Binary Scene",
            ".fbx": "FBX Exchange Format",
            ".abc": "Alembic Cache",
            ".obj": "Wavefront OBJ Geometry",
            ".usd": "Universal Scene Description",
        }

        for ext, description in self.file_types.items():
            checkbox = QtWidgets.QCheckBox(f"{ext} — {description}")

            checkbox.setMinimumHeight(24)

            self.export_layout.addWidget(checkbox)
            self.export_checkboxes[ext] = checkbox

        self.export_layout.addStretch()

        # Scroll area
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.export_widget)

        # Buttons
        self.publish_btn = QtWidgets.QPushButton("Publish")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        main_layout.addWidget(self.title_label)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.preview_label, self.preview_edit)
        form_layout.addRow(self.export_label, self.scroll_area)
        main_layout.addLayout(form_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.publish_btn)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.cancel_btn.clicked.connect(self.close)
        self.publish_btn.clicked.connect(self.publish_file)

    def get_selected_file_types(self):
        selected = []

        for ext, checkbox in self.export_checkboxes.items():
            if checkbox.isChecked():
                selected.append(ext)

        return selected

    def publish_file(self):
        selected_types = self.get_selected_file_types()

        if not selected_types:
            QtWidgets.QMessageBox.warning(
                self,
                "No Export Type",
                "Please select at least one export type."
            )

            return

        if self.dcc_interface.verify_file():
            failed_exports = []

            for ext in selected_types:
                try:
                    print(f"Publishing file extension: {ext}")
                    success = self.dcc_interface.publish_file(ext)

                    if not success:
                        failed_exports.append(ext)

                except Exception as error:
                    print(error)
                    failed_exports.append(ext)

            if failed_exports:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Publish Complete",
                    "Some exports failed:\n\n"
                    + "\n".join(failed_exports)
                )
            else:
                cmds.confirmDialog(
                    title="Publish Complete",
                    message="All exports completed successfully.",
                    button=["OK"]
                )
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Save Error",
                "Current file failed verification."
            )

        self.close()
