try:
    from PySide6 import QtWidgets
except:
    from PySide2 import QtWidgets

import utils.file_folder_utils as ffu
from dcc_manager.dcc_interface import DCCInterface
from ui.production_user_tasks import ProductionUserTasksTab
from ui.production_assets_ui import ProductionAssetsTab
from ui.production_shot_tasks_ui import ProductionShotTasksTab


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
        return

    def create_layout(self):
        """Create all layouts and add widgets to them"""
        # Tab 3: Production
        production_layout = QtWidgets.QVBoxLayout(self)
        self.production_main_tab = QtWidgets.QTabWidget()

        self.production_user_tasks_tab = ProductionUserTasksTab(self.dcc_interface)
        self.production_main_tab.addTab(self.production_user_tasks_tab, "My Tasks")

        self.production_assets_tab = ProductionAssetsTab(self.dcc_interface)
        self.production_main_tab.addTab(self.production_assets_tab, "Assets")

        self.production_shots_tab = ProductionShotTasksTab(self.dcc_interface)
        self.production_main_tab.addTab(self.production_shots_tab, "Shots / Sequences")

        production_layout.addWidget(self.production_main_tab)
        self.production_main_tab.setCurrentIndex(1)

    def create_connections(self):
        """Create all connections for the UI"""
        self.production_main_tab.tabBarClicked.connect(self.refresh_view)

    def refresh_view(self):
        self.production_user_tasks_tab.asset_task_trees.generate_tree()
        self.production_user_tasks_tab.shot_task_trees.generate_tree()
        self.production_assets_tab.assets_tree.generate_tree()
        self.production_shots_tab.shot_tasks_tree.generate_tree()
