from pathlib import Path
import json
import sys
from functools import partial

try:
    from PySide6 import QtCore
    from PySide6 import QtWidgets
    from PySide6 import QtGui
    from shiboken6 import wrapInstance
except:
    from PySide2 import QtCore
    from PySide2 import QtWidgets
    from PySide2 import QtGui
    from shiboken2 import wrapInstance

import utils.file_folder_utils as hf
from dcc_manager.dcc_interface import DCCInterface
from ui.creation_ui import CreationTab
from ui.assignment_ui import AssignmentTab
from ui.production_ui import ProductionTab


class PixieDustDialog(QtWidgets.QDialog):
    dlg_instance = None
    
    @classmethod
    def show_dialog(cls, dcc_interface: DCCInterface):
        if not cls.dlg_instance:
            cls.dlg_instance = PixieDustDialog(dcc_interface)
            
        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self, dcc_interface: DCCInterface):
        """Initialise PixieDustDialog"""
        super(PixieDustDialog, self).__init__()

        self.setWindowTitle("Pixie Dust")

        self.dcc_interface = dcc_interface
        self.main_window = self.dcc_interface.get_main_window()

        size = self.main_window.screen().size()
        screen_w, screen_h = size.width(), size.height()
        self.resize(int(screen_w * 0.3), int(screen_h * 0.5))
        
        # On macOS make the window a Tool to keep it on top of Maya
        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.Tool, True)

        config_path = hf.get_code_dir() / "config.json"

        with open(str(config_path), 'r') as file:
            config_data = json.load(file)
            self.main_folder_path = Path(config_data["main_folder_path"])
            self.assignment_data_path = Path(config_data["assignment_data_path"])

        self.assignment_data = hf.get_assignment_data()

        self.create_widgets()
        self.create_layout()
        self.create_connections()

        self.creation_tab.switch_creation_type(0)
        self.assignment_tab.show_asset_assignment_table(1)
        self.production_tab.show_tasks_table()

    def create_widgets(self):
        """Create all widgets for the UI"""
        # Tab 5: Generate Info
        self.generate_btn = QtWidgets.QPushButton("Generate")

    def create_layout(self):
        """Create all layouts and add widgets to them"""

        # Create tab widget
        self.main_tab_widget = QtWidgets.QTabWidget()

        # Tab 1: Creation
        self.creation_tab = CreationTab()
        self.main_tab_widget.addTab(self.creation_tab, "Creation")

        # Tab 2: Assignment
        self.assignment_tab = AssignmentTab()
        self.main_tab_widget.addTab(self.assignment_tab, "Assignment")

        # Tab 3: Production
        self.production_tab = ProductionTab()
        self.main_tab_widget.addTab(self.production_tab, "Production")

        # Tab 4: Save
        save_tab = QtWidgets.QWidget()
        save_layout = QtWidgets.QVBoxLayout(save_tab)

        self.main_tab_widget.addTab(save_tab, "Save")

        # Tab 4: Publish
        publish_tab = QtWidgets.QWidget()
        publish_layout = QtWidgets.QVBoxLayout(publish_tab)

        self.main_tab_widget.addTab(publish_tab, "Publish")

        # Tab 5: Import/Reference
        import_tab = QtWidgets.QWidget()
        import_layout = QtWidgets.QVBoxLayout(import_tab)

        self.main_tab_widget.addTab(import_tab, "Import/Reference")

        # Tab 6: Information
        information_tab = QtWidgets.QWidget()
        information_layout = QtWidgets.QVBoxLayout(information_tab)
        information_layout.addWidget(self.generate_btn)

        self.main_tab_widget.addTab(information_tab, "Information")
        
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.main_tab_widget)

    def create_connections(self):
        """Create all connections for the UI"""
        self.main_tab_widget.tabBarClicked.connect(self.creation_tab.switch_creation_type)
        self.main_tab_widget.tabBarClicked.connect(self.assignment_tab.show_asset_assignment_table)

if __name__ == "__main__":
    PixieDustDialog.show_dialog()
