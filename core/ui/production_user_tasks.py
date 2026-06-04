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
from ui.asset_tree_ui import AssetTreeWidget
from ui.shot_task_tree_ui import ShotTaskTreeWidget


class ProductionUserTasksTab(QtWidgets.QWidget):
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

        self.wip_label = QtWidgets.QLabel("WIP Versions")
        self.wip_label.setAlignment(QtCore.Qt.AlignCenter) 
        self.wip_list = QtWidgets.QTreeWidget()
        self.wip_list.setHeaderLabels(["Version"])

        self.open_file_btn = QtWidgets.QPushButton("Open File")

        current_assignee_uid = ffu.get_uid(self.current_user_dropdown.currentText())
        self.asset_task_trees = AssetTreeWidget(extra_info=False, uid=current_assignee_uid)
        self.shot_task_trees = ShotTaskTreeWidget(extra_info=False, uid=current_assignee_uid)

    def create_layout(self):
        """Create all layouts and add widgets to them"""
        production_tasks_layout = QtWidgets.QVBoxLayout(self)

        current_user_layout = QtWidgets.QFormLayout()
        current_user_layout.addRow("Current User:", self.current_user_dropdown)
        production_tasks_layout.addLayout(current_user_layout)

        production_tasks_trees_layout = QtWidgets.QHBoxLayout()
        production_tasks_trees_layout.addWidget(self.asset_task_trees)
        production_tasks_trees_layout.addWidget(self.shot_task_trees)

        wip_layout = QtWidgets.QVBoxLayout()
        wip_layout.addWidget(self.wip_label)
        wip_layout.addWidget(self.wip_list)
        production_tasks_trees_layout.addLayout(wip_layout)

        production_tasks_layout.addLayout(production_tasks_trees_layout)

        open_file_layout = QtWidgets.QHBoxLayout()
        open_file_layout.addWidget(self.open_file_btn)
        production_tasks_layout.addLayout(open_file_layout)

    def create_connections(self):
        """Create all connections for the UI"""
        self.asset_task_trees.itemClicked.connect(self.focus_list)
        self.shot_task_trees.itemClicked.connect(self.focus_list)

        self.current_user_dropdown.currentTextChanged.connect(self.show_tasks_trees)
        self.current_user_dropdown.currentTextChanged.connect(self.focus_list)
        self.open_file_btn.pressed.connect(self.open_file)

    def show_tasks_trees(self):
        current_assignee_uid = ffu.get_uid(self.current_user_dropdown.currentText())

        self.asset_task_trees.generate_specific_user_tree(current_assignee_uid)
        self.shot_task_trees.generate_specific_user_tree(current_assignee_uid)

    def focus_list(self, list_item_widget):
        self.asset_task_trees.clearSelection()
        self.shot_task_trees.clearSelection()

        if isinstance(list_item_widget, QtWidgets.QTreeWidgetItem):
            list_item_widget.treeWidget().setCurrentItem(list_item_widget)
            self.selected_item = list_item_widget

            self.show_versions()

    def show_versions(self):
        self.wip_list.clear()

        count = 0
        parent = self.selected_item.parent()

        while parent:
            count += 1
            parent = parent.parent()

        if self.selected_item.treeWidget() == self.asset_task_trees and count == 2:
            asset_part_item = self.selected_item
            asset_part = asset_part_item.text(0)
            asset_name_item = asset_part_item.parent()
            asset_name = asset_name_item.text(0)
            asset_type_item = asset_name_item.parent()
            asset_type = asset_type_item.text(0)
            
            wip_files = self.dcc_interface.get_asset_files(asset_name, asset_type, asset_part, "wip")
            
            for wip_file in reversed(wip_files):
                wip_version = wip_file.stem.rsplit("_", 1)[1]
                wip_item = QtWidgets.QTreeWidgetItem([wip_version])
                wip_item.setData(0, QtCore.Qt.UserRole, wip_file)
                self.wip_list.addTopLevelItem(wip_item)
        elif self.selected_item.treeWidget() == self.shot_task_trees and count == 3:
            task_item = self.selected_item
            task = task_item.text(0)
            department_item = task_item.parent()
            department = department_item.text(0)
            shot_item = department_item.parent()
            shot = shot_item.text(0)
            sequence_item = shot_item.parent()
            sequence = sequence_item.text(0)
            
            wip_files = self.dcc_interface.get_shot_task_files(sequence, shot, department, task, "wip")

            for wip_file in reversed(wip_files):
                wip_version = wip_file.stem.rsplit("_", 1)[1]
                wip_item = QtWidgets.QTreeWidgetItem([wip_version])
                wip_item.setData(0, QtCore.Qt.UserRole, wip_file)
                self.wip_list.addTopLevelItem(wip_item)

    def open_file(self):
        file_path = self.wip_list.currentItem().data(0, QtCore.Qt.UserRole)
        self.dcc_interface.open_file(file_path)

        self.window().close()
