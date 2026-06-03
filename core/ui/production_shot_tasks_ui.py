from pathlib import Path
import json
import sys

try:
    from PySide6 import QtCore
    from PySide6 import QtWidgets
except:
    from PySide2 import QtCore
    from PySide2 import QtWidgets

import utils.file_folder_utils as ffu
from dcc_manager.dcc_interface import DCCInterface
from ui.shot_task_tree_ui import ShotTaskTreeWidget


class ProductionShotTasksTab(QtWidgets.QWidget):
    def __init__(self, dcc_interface: DCCInterface):
        super().__init__()

        self.dcc_interface = dcc_interface
        self.main_workspace_path = ffu.get_main_workspace_path()
        self.assignment_data = ffu.get_assignment_data()
        self.users = ffu.get_users()

        self.focused_version_item = None

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create all widgets for the UI"""
        self.current_user_dropdown = QtWidgets.QComboBox()
        self.current_user_dropdown.addItems([x for x in self.users])

        self.shot_tasks_tree = ShotTaskTreeWidget(extra_info=False)

        self.wip_label = QtWidgets.QLabel("WIP Versions")
        self.wip_label.setAlignment(QtCore.Qt.AlignCenter) 
        self.wip_list = QtWidgets.QTreeWidget()
        self.wip_list.setHeaderLabels(["Version"])
        # item = QtWidgets.QTreeWidgetItem(["v0001"])
        # self.wip_list.addTopLevelItem(item)

        self.publish_label = QtWidgets.QLabel("Published Versions")
        self.publish_label.setAlignment(QtCore.Qt.AlignCenter) 
        self.publish_list = QtWidgets.QTreeWidget()
        self.publish_list.setHeaderLabels(["Version"])
        # item = QtWidgets.QTreeWidgetItem(["v0001"])
        # self.publish_list.addTopLevelItem(item)

        self.new_file_btn = QtWidgets.QPushButton("New File")
        self.open_file_btn = QtWidgets.QPushButton("Open File")

    def create_layout(self):
        """Create all layouts and add widgets to them"""
        # Tab 3: Production
        shot_tasks_layout = QtWidgets.QVBoxLayout(self)
        shot_tasks_info_layout = QtWidgets.QHBoxLayout()
        shot_tasks_info_layout.addWidget(self.shot_tasks_tree)

        shot_tasks_wip_layout = QtWidgets.QVBoxLayout(self)
        shot_tasks_wip_layout.addWidget(self.wip_label)
        shot_tasks_wip_layout.addWidget(self.wip_list)
        shot_tasks_info_layout.addLayout(shot_tasks_wip_layout)

        shot_tasks_publish_layout = QtWidgets.QVBoxLayout(self)
        shot_tasks_publish_layout.addWidget(self.publish_label)
        shot_tasks_publish_layout.addWidget(self.publish_list)
        shot_tasks_info_layout.addLayout(shot_tasks_publish_layout)

        shot_tasks_layout.addLayout(shot_tasks_info_layout)

        file_creation_layout = QtWidgets.QHBoxLayout()
        file_creation_layout.addWidget(self.new_file_btn)
        file_creation_layout.addWidget(self.open_file_btn)
        shot_tasks_layout.addLayout(file_creation_layout)

    def create_connections(self):
        """Create all connections for the UI"""
        self.shot_tasks_tree.itemClicked.connect(self.show_shot_task_versions)
        self.wip_list.itemClicked.connect(self.focus_list)
        self.publish_list.itemClicked.connect(self.focus_list)
        self.new_file_btn.pressed.connect(self.create_new_file)
        self.open_file_btn.pressed.connect(self.open_file)

    def focus_list(self, list_item_widget):
        self.wip_list.clearSelection()
        self.publish_list.clearSelection()

        list_item_widget.treeWidget().setCurrentItem(list_item_widget)
        self.focused_version_item = list_item_widget

    def show_shot_task_versions(self):
        task_item = self.shot_tasks_tree.currentItem()
        task = task_item.text(0)

        parents = 0
        parent = task_item.parent()

        while parent:
            parents += 1
            parent = parent.parent()

        if parents == 3:
            department_item = task_item.parent()
            department = department_item.text(0)

            shot_item = department_item.parent()
            shot = shot_item.text(0)

            sequence_item = shot_item.parent()
            sequence = sequence_item.text(0)
            
            wip_asset_files = self.dcc_interface.get_shot_task_files(sequence, shot, department, task, "wip")
            self.wip_list.clear()
            for wip_asset_file in reversed(wip_asset_files):
                wip_asset_version = wip_asset_file.stem.rsplit("_", 1)[1]
                wip_asset_item = QtWidgets.QTreeWidgetItem([wip_asset_version])
                wip_asset_item.setData(0, QtCore.Qt.UserRole, wip_asset_file)
                self.wip_list.addTopLevelItem(wip_asset_item)
                
            published_asset_files = self.dcc_interface.get_shot_task_files(sequence, shot, department, task, "publishes")
            self.publish_list.clear()
            for published_asset_file in reversed(published_asset_files):
                published_asset_version = published_asset_file.stem.rsplit("_", 1)[1]
                published_asset_item = QtWidgets.QTreeWidgetItem([published_asset_version])
                published_asset_item.setData(0, QtCore.Qt.UserRole, published_asset_file)
                self.publish_list.addTopLevelItem(published_asset_item)

    def create_new_file(self):
        task_item = self.shot_tasks_tree.currentItem()
        task = task_item.text(0)

        parents = 0
        parent = task_item.parent()

        while parent:
            parents += 1
            parent = parent.parent()

        if parents == 3:
            department_item = task_item.parent()
            department = department_item.text(0)

            shot_item = department_item.parent()
            shot = shot_item.text(0)

            sequence_item = shot_item.parent()
            sequence = sequence_item.text(0)

            self.dcc_interface.create_new_shot_task_file(sequence, shot, department, task)
        else: 
            QtWidgets.QMessageBox.warning(
                self,
                "Wrong Selection",
                "Please select an asset part to create a new file for."
            )
            return

    def open_file(self):
        file_path = self.focused_version_item.data(0, QtCore.Qt.UserRole)
        self.dcc_interface.open_file(file_path)
