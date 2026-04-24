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

import maya.OpenMayaUI as omui

code_dir = Path("F:\\ALA Projects\\Pixie Dust\\sheeping_beauty\\pixie-dust")
sys.path.append(str(code_dir))

import helper_functions as hf
from creation_ui import CreationTab
from assignment_ui import AssignmentTab

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class PixieDustDialog(QtWidgets.QDialog):
    dlg_instance = None
    
    @classmethod
    def show_dialog(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = PixieDustDialog()
            
        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    def __init__(self, parent=maya_main_window()):
        """Initialise PixieDustDialog"""
        super(PixieDustDialog, self).__init__(parent)

        self.setWindowTitle("Pixie Dust")

        size = maya_main_window().screen().size()
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
        self.show_tasks_table()

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

        # self.tasks_cards = QtWidgets.QListView()
        # self.tasks_cards.setViewMode(QtWidgets.QListView.ViewMode.IconMode)
        # model = QtGui.QStandardItemModel()
        # item = QtGui.QStandardItem("New Item Text")
        # model.appendRow(item)
        # self.tasks_cards.setModel(model)

        self.assignee_tasks_le = QtWidgets.QLineEdit()

        self.get_tasks_btn = QtWidgets.QPushButton("Get Tasks")
        self.new_file_btn = QtWidgets.QPushButton("New File")
        self.open_file_btn = QtWidgets.QPushButton("Open File")

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
        production_tab = QtWidgets.QWidget()
        production_layout = QtWidgets.QVBoxLayout(production_tab)

        production_layout.addWidget(self.assignee_tasks_le)

        production_main_tab = QtWidgets.QTabWidget()
        production_tasks_tab = QtWidgets.QWidget()
        production_assets_tab = QtWidgets.QWidget()
        production_shots_tab = QtWidgets.QWidget()
        production_main_tab.addTab(production_tasks_tab, "My Tasks")
        production_main_tab.addTab(production_assets_tab, "Assets")
        production_main_tab.addTab(production_shots_tab, "Shots / Sequences")
        production_layout.addWidget(production_main_tab)

        self.production_tasks_layout = QtWidgets.QVBoxLayout(production_tasks_tab)
        # production_tasks_layout.addWidget(self.tasks_cards)
        # production_tasks_layout.addWidget(self.card1)
        # production_tasks_layout.addWidget(self.card2)

        assets_layout = QtWidgets.QVBoxLayout(production_assets_tab)
        assets_layout.addWidget(self.assets_tree)

        file_creation_layout = QtWidgets.QHBoxLayout(production_tab)
        file_creation_layout.addWidget(self.get_tasks_btn)
        file_creation_layout.addWidget(self.new_file_btn)
        file_creation_layout.addWidget(self.open_file_btn)
        production_layout.addLayout(file_creation_layout)

        self.main_tab_widget.addTab(production_tab, "Production")

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
        self.get_tasks_btn.pressed.connect(self.show_tasks_table)

    def show_tasks_table(self):
        with open(self.assignment_data_path, 'r') as file:
            data = json.load(file)

        card_data = []

        for assignment in data["assignments"]:
            if assignment["assignee"] == self.assignee_tasks_le.text(): 
                card_data.append((assignment["asset_name"], assignment["asset_part"]))

        card_data.sort()

        for card in card_data:
            self.production_tasks_layout.addWidget(Card(card[0], card[1]))

        # self.tasks.setColumnCount(5)
        # self.assignment_table.setHorizontalHeaderLabels(["Main Type", "Asset Type", "Asset Name", "Asset Part", "Assignees"])
        # self.assignment_table.setRowCount(0)
        # self.assignment_table.verticalHeader().setVisible(False)

        # for assets_type in assets_types:
        #     index = self.assignment_table.rowCount()
        #     self.assignment_table.setRowCount(index + 1)

        #     asset_type_item = QtWidgets.QTableWidgetItem(assets_type.name)
        #     self.assignment_table.setItem(index, 0, asset_type_item)
        #     self.assignment_table.setSpan(index, 0, 1, 3)

        #     n_a_item = QtWidgets.QTableWidgetItem("N/A")
        #     self.assignment_table.setItem(index, 3, n_a_item)

        #     assets = [x for x in assets_type.iterdir() if x.is_dir()]

        #     for asset in assets:
        #         index = self.assignment_table.rowCount()
        #         self.assignment_table.setRowCount(index + 1)

        #         asset_item = QtWidgets.QTableWidgetItem(asset.name)
        #         self.assignment_table.setItem(index, 1, asset_item)
        #         self.assignment_table.setSpan(index, 1, 1, 2)

        #         n_a_item = QtWidgets.QTableWidgetItem("N/A")
        #         self.assignment_table.setItem(index, 3, n_a_item)

        #         asset_parts = [x for x in asset.iterdir() if x.is_dir()]

        #         for asset_part in asset_parts:
        #             index = self.assignment_table.rowCount()
        #             self.assignment_table.setRowCount(index + 1)

        #             asset_part_item = QtWidgets.QTableWidgetItem(asset_part.name)
        #             self.assignment_table.setItem(index, 2, asset_part_item)

        #             assignments = self.get_assignment_data()["assignments"]

        #             assignees = []

        #             for assignment in assignments:
        #                 if (assignment["main_type"] == "asset" 
        #                     and assignment["asset_type"] == assets_type.name
        #                     and assignment["asset_name"] == asset.name
        #                     and assignment["asset_part"] == asset_part.name 
        #                     ):
        #                     assignees.append(assignment["assignee"])
                    
        #             assignment_item = QtWidgets.QTableWidgetItem(", ".join(assignees))

        #             assignment_data = {
        #                 "main_type": "asset",
        #                 "asset_type": assets_type.name,
        #                 "asset_name": asset.name,
        #                 "asset_part": asset_part.name
        #             }

        #             assignment_item.setData(QtCore.Qt.UserRole, assignment_data)
        #             self.assignment_table.setItem(index, 3, assignment_item)

        # self.assignment_table.resizeColumnsToContents()

class Card(QtWidgets.QFrame):
    def __init__(self, title, content):
        super().__init__()

        self.setObjectName("card")

        layout = QtWidgets.QVBoxLayout(self)

        title_label = QtWidgets.QLabel(title)
        content_label = QtWidgets.QLabel(content)

        layout.addWidget(title_label)
        layout.addWidget(content_label)

        self.setStyleSheet("""
        QFrame#card {
            border-radius: 10px;
            border: 1px solid #ddd;
            padding: 10px;
        }
        QLabel {
            font-size: 30px;
        }
        """)

if __name__ == "__main__":
    PixieDustDialog.show_dialog()
