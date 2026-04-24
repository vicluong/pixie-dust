from pathlib import Path
import json
import sys

try:
    from PySide6 import QtCore
    from PySide6 import QtWidgets
except:
    from PySide2 import QtCore
    from PySide2 import QtWidgets

import helper_functions as hf


class ProductionTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        config_path = hf.get_code_dir() / "config.json"

        with open(str(config_path), 'r') as file:
            config_data = json.load(file)
            self.main_folder_path = Path(config_data["main_folder_path"])
            self.assignment_data_path = Path(config_data["assignment_data_path"])

        self.assignment_data = hf.get_assignment_data()

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create all widgets for the UI"""
        # Tab 3: Assignment
        self.assets_tree = QtWidgets.QTreeWidget()
        self.assets_tree.setHeaderLabels(["Assets", "Latest WIP Version", "Latest Publish Version", "Assignees"])
        main_type_tree_item = QtWidgets.QTreeWidgetItem()
        main_type_tree_item.setText(0, "Asset")
        main_type_tree_item2 = QtWidgets.QTreeWidgetItem()
        main_type_tree_item2.setText(0, "Asset2")
        main_type_tree_item.addChild(main_type_tree_item2)
        self.assets_tree.addTopLevelItems([main_type_tree_item])
        self.assets_tree.expandAll()
        self.assets_tree.setItemsExpandable(False)

        self.assignee_tasks_le = QtWidgets.QLineEdit()

    def create_layout(self):
        """Create all layouts and add widgets to them"""
        # Tab 3: Production
        production_layout = QtWidgets.QVBoxLayout(self)

        production_layout.addWidget(self.assignee_tasks_le)

        production_main_tab = QtWidgets.QTabWidget()
        production_tasks_tab = QtWidgets.QWidget()
        production_assets_tab = QtWidgets.QWidget()
        production_shots_tab = QtWidgets.QWidget()
        production_main_tab.addTab(production_tasks_tab, "My Tasks")
        production_main_tab.addTab(production_assets_tab, "Assets")
        production_main_tab.addTab(production_shots_tab, "Shots / Sequences")
        production_layout.addWidget(production_main_tab)

    def create_connections(self):
        """Create all connections for the UI"""
        self.get_tasks_btn.pressed.connect(self.show_tasks_table)
