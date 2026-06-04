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
from ui.production_user_tasks import ProductionUserTasksTab
from ui.production_assets_ui import ProductionAssetsTab
from ui.production_shot_tasks_ui import ProductionShotTasksTab
from ui.asset_tree_ui import AssetTreeWidget
from ui.shot_task_tree_ui import ShotTaskTreeWidget


class ProductionTab(QtWidgets.QWidget):
    def __init__(self, dcc_interface: DCCInterface):
        super().__init__()

        self.dcc_interface = dcc_interface
        self.main_workspace_path = ffu.get_main_workspace_path()

        self.assignment_data = ffu.get_assignment_data()
        self.users = ffu.get_users()

        self.selected_item = None

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create all widgets for the UI"""
        # Tab 3: Assignment


    def create_layout(self):
        """Create all layouts and add widgets to them"""
        # Tab 3: Production
        production_layout = QtWidgets.QVBoxLayout(self)
        production_main_tab = QtWidgets.QTabWidget()

        production_user_tasks_tab = ProductionUserTasksTab(self.dcc_interface)
        production_main_tab.addTab(production_user_tasks_tab, "My Tasks")

        production_assets_tab = ProductionAssetsTab(self.dcc_interface)
        production_main_tab.addTab(production_assets_tab, "Assets")

        production_shots_tab = ProductionShotTasksTab(self.dcc_interface)
        production_main_tab.addTab(production_shots_tab, "Shots / Sequences")

        production_layout.addWidget(production_main_tab)
        production_main_tab.setCurrentIndex(1)

    def create_connections(self):
        """Create all connections for the UI"""
        return
