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


class ProductionAssetsTab(QtWidgets.QWidget):
    def __init__(self, dcc_interface: DCCInterface):
        super().__init__()

        self.dcc_interface = dcc_interface

        config_path = ffu.get_code_dir() / "config.json"

        with open(str(config_path), 'r') as file:
            config_data = json.load(file)
            self.main_folder_path = Path(config_data["main_folder_path"])
            self.assignment_data_path = Path(config_data["assignment_data_path"])

        self.assignment_data = ffu.get_assignment_data()
        self.users = ffu.get_users()

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create all widgets for the UI"""
        # Tab 3: Assignment
        self.current_user_dropdown = QtWidgets.QComboBox()
        self.current_user_dropdown.addItems([x for x in self.users])

            # Assets Tab
        self.assets_tree = QtWidgets.QTreeWidget()
        self.assets_tree.setHeaderLabels(["Assets"])
        self.show_production_assets()

        self.wip_label = QtWidgets.QLabel("WIP Versions")
        self.wip_label.setAlignment(QtCore.Qt.AlignCenter) 
        self.wip_list = QtWidgets.QTreeWidget()
        self.wip_list.setHeaderLabels(["Version"])
        item = QtWidgets.QTreeWidgetItem(["v0001"])
        self.wip_list.addTopLevelItem(item)

        self.publish_label = QtWidgets.QLabel("Published Versions")
        self.publish_label.setAlignment(QtCore.Qt.AlignCenter) 
        self.publish_list = QtWidgets.QTreeWidget()
        self.publish_list.setHeaderLabels(["Version"])
        item = QtWidgets.QTreeWidgetItem(["v0001"])
        self.publish_list.addTopLevelItem(item)

        self.new_file_btn = QtWidgets.QPushButton("New File")
        self.open_file_btn = QtWidgets.QPushButton("Open File")

    def create_layout(self):
        """Create all layouts and add widgets to them"""
        # Tab 3: Production
        assets_layout = QtWidgets.QVBoxLayout(self)
        assets_info_layout = QtWidgets.QHBoxLayout()
        assets_info_layout.addWidget(self.assets_tree)

        assets_wip_layout = QtWidgets.QVBoxLayout(self)
        assets_wip_layout.addWidget(self.wip_label)
        assets_wip_layout.addWidget(self.wip_list)
        assets_info_layout.addLayout(assets_wip_layout)

        assets_publish_layout = QtWidgets.QVBoxLayout(self)
        assets_publish_layout.addWidget(self.publish_label)
        assets_publish_layout.addWidget(self.publish_list)
        assets_info_layout.addLayout(assets_publish_layout)

        assets_layout.addLayout(assets_info_layout)

        file_creation_layout = QtWidgets.QHBoxLayout()
        file_creation_layout.addWidget(self.new_file_btn)
        file_creation_layout.addWidget(self.open_file_btn)
        assets_layout.addLayout(file_creation_layout)

    def create_connections(self):
        """Create all connections for the UI"""
        self.assets_tree.itemClicked.connect(self.show_asset_versions)
        self.new_file_btn.pressed.connect(self.create_new_file)

    def show_asset_versions(self, tree_item):
        parents = 0
        parent = tree_item.parent()

        while parent:
            parents += 1
            parent = parent.parent()

        if parents == 2:
            asset_part_index = self.assets_tree.currentIndex()
            asset_part = asset_part_index.data()

            asset_name_index = asset_part_index.parent()
            if asset_name_index.isValid():
                asset_name = asset_name_index.data()
                print(f"Asset Name: {asset_name}")
            else:
                return

            asset_type_index = asset_name_index.parent()
            if asset_type_index.isValid():
                asset_type = asset_type_index.data()
                print(f"Asset Type: {asset_type}")
            else:
                return
            
            wip_asset_files = self.dcc_interface.get_asset_files(asset_name, asset_type, asset_part, "wip")
            wip_asset_versions = [f.stem.rsplit("_", 1)[1] for f in wip_asset_files]

            published_asset_files = self.dcc_interface.get_asset_files(asset_name, asset_type, asset_part, "publishes")
            published_asset_versions = [f.stem.rsplit("_", 1)[1] for f in published_asset_files]

            self.wip_list.clear()
            for wip_asset_version in reversed(wip_asset_versions):
                self.wip_list.addTopLevelItem(QtWidgets.QTreeWidgetItem([wip_asset_version]))

            self.publish_list.clear()
            for published_asset_version in reversed(published_asset_versions):
                self.publish_list.addTopLevelItem(QtWidgets.QTreeWidgetItem([published_asset_version]))

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
        
        self.dcc_interface.create_new_asset_file(asset_name, asset_type, asset_part)

    def show_production_assets(self):
        tree_model = self.assets_tree.model()
        tree_model.removeRows(0, tree_model.rowCount())

        self.assignment_data = ffu.get_assignment_data()

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

                    assignments = self.assignment_data
                    # assignees = []
                    for assignment in assignments.values():
                        if (assignment["entity_type"] == "asset" 
                            and assignment["asset_type"] == assets_type.name
                            and assignment["asset_name"] == asset.name
                            and assignment["asset_part"] == asset_part.name 
                            ):
                            # assignees.append(assignment["assignee"])
                            print(assignment)

        self.assets_tree.addTopLevelItems(top_level_items)
        self.assets_tree.expandAll()

    def create_new_asset_file(self):
        asset_part_index = self.assets_tree.currentIndex()
        asset_part = asset_part_index.data()

        asset_name_index = asset_part_index.parent()
        if asset_name_index.isValid():
            asset_name = asset_name_index.data()
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
            asset_type = asset_type_index.data()
            print(f"Asset Type: {asset_type}")
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Wrong Selection",
                "Please select an asset part to create a new file for."
            )
            return
        
        self.dcc_interface.create_new_asset_file(asset_name, asset_type, asset_part)
