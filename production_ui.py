from pathlib import Path
import json
import sys

try:
    from PySide6 import QtCore
    from PySide6 import QtWidgets
except:
    from PySide2 import QtCore
    from PySide2 import QtWidgets

import maya.cmds as cmds

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
        self.assignee_tasks_le = QtWidgets.QLineEdit()

            # Assets Tab
        self.assets_tree = QtWidgets.QTreeWidget()
        self.assets_tree.setHeaderLabels(["Assets"])
        self.show_production_assets()

        self.wip_label = QtWidgets.QLabel("WIP Versions")
        self.wip_label.setAlignment(QtCore.Qt.AlignCenter) 
        self.wip_list = QtWidgets.QTreeWidget()
        self.wip_list.setHeaderLabels(["Version", "Creator"])
        item = QtWidgets.QTreeWidgetItem(["v001", "Jim"])
        self.wip_list.addTopLevelItem(item)

        self.publish_label = QtWidgets.QLabel("Published Versions")
        self.publish_label.setAlignment(QtCore.Qt.AlignCenter) 
        self.publish_list = QtWidgets.QTreeWidget()
        self.publish_list.setHeaderLabels(["Version", "Creator"])
        item = QtWidgets.QTreeWidgetItem(["v001", "Jim"])
        self.publish_list.addTopLevelItem(item)

        self.new_file_btn = QtWidgets.QPushButton("New File")
        self.open_file_btn = QtWidgets.QPushButton("Open File")

            # Bottom File Buttons
        self.get_tasks_btn = QtWidgets.QPushButton("Get Tasks")

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

        self.production_tasks_layout = QtWidgets.QVBoxLayout(production_tasks_tab)

        assets_layout = QtWidgets.QVBoxLayout(production_assets_tab)
        assets_info_layout = QtWidgets.QHBoxLayout()
        assets_info_layout.addWidget(self.assets_tree)
        assets_wip_layout = QtWidgets.QVBoxLayout(production_assets_tab)
        assets_wip_layout.addWidget(self.wip_label)
        assets_wip_layout.addWidget(self.wip_list)
        assets_info_layout.addLayout(assets_wip_layout)
        assets_publish_layout = QtWidgets.QVBoxLayout(production_assets_tab)
        assets_publish_layout.addWidget(self.publish_label)
        assets_publish_layout.addWidget(self.publish_list)
        assets_info_layout.addLayout(assets_publish_layout)
        assets_layout.addLayout(assets_info_layout)

        file_creation_layout = QtWidgets.QHBoxLayout()
        # file_creation_layout.addWidget(self.get_tasks_btn)
        file_creation_layout.addWidget(self.new_file_btn)
        file_creation_layout.addWidget(self.open_file_btn)
        assets_layout.addLayout(file_creation_layout)

    def create_connections(self):
        """Create all connections for the UI"""
        # self.get_tasks_btn.pressed.connect(self.show_tasks_table)
        self.new_file_btn.pressed.connect(self.create_new_file)

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

    def show_production_assets(self):
        tree_model = self.assets_tree.model()
        tree_model.removeRows(0, tree_model.rowCount())

        self.assignment_data = hf.get_assignment_data()

        assets_path = self.main_folder_path / "assets"
        assets_types = [x for x in assets_path.iterdir() if x.is_dir()]

        top_level_items = []

        for assets_type in assets_types:
            asset_type_item = QtWidgets.QTreeWidgetItem()
            asset_type_item.setText(0, assets_type.name)

            top_level_items.append(asset_type_item)

            assets = [x for x in assets_type.iterdir() if x.is_dir()]

            for asset in assets:
                asset_name_item = QtWidgets.QTreeWidgetItem()
                asset_name_item.setText(0, asset.name)
                asset_type_item.addChild(asset_name_item)

                asset_parts = [x for x in asset.iterdir() if x.is_dir()]

                for asset_part in asset_parts:
                    asset_part_item = QtWidgets.QTreeWidgetItem()
                    asset_part_item.setText(0, asset_part.name)
                    asset_name_item.addChild(asset_part_item)

                    assignments = self.assignment_data["assignments"]
                    assignees = []
                    for assignment in assignments:
                        if (assignment["main_type"] == "asset" 
                            and assignment["asset_type"] == assets_type.name
                            and assignment["asset_name"] == asset.name
                            and assignment["asset_part"] == asset_part.name 
                            ):
                            assignees.append(assignment["assignee"])

        self.assets_tree.addTopLevelItems(top_level_items)
        self.assets_tree.expandAll()

    def create_new_file(self):
        asset_part_index = self.assets_tree.currentIndex()
        asset_part = asset_part_index.data()

        asset_name_index = asset_part_index.parent()
        if asset_name_index.isValid():
            asset_name = asset_name_index.data() # Returns the text of the parent
            print(f"Asset Name: {asset_name}")
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Wrong Selection",
                "Please select an asset part to create a new file for."
            )
            return

        asset_type_index = asset_name_index.parent()
        if asset_type_index.isValid():
            asset_type = asset_type_index.data() # Returns the text of the parent
            print(f"Asset Type: {asset_type}")
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Wrong Selection",
                "Please select an asset part to create a new file for."
            )
            return
        
        cmds.file(new=True, force=True)
        main_folder_path = hf.get_main_folder_path()
        file_path = str(main_folder_path / "assets" / asset_type / asset_name / asset_part 
                        / "wip" / f"{asset_name}_{asset_type}_{asset_part}_v000.mb")

        cmds.file(rename=f"{str(file_path)}")

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
