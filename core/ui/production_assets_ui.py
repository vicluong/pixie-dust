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


class ProductionAssetsTab(QtWidgets.QWidget):
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

        self.assets_tree = AssetTreeWidget(extra_info=False)

        self.wip_label = QtWidgets.QLabel("WIP Versions")
        self.wip_label.setAlignment(QtCore.Qt.AlignCenter) 
        self.wip_list = QtWidgets.QTreeWidget()
        self.wip_list.setHeaderLabels(["Version"])

        self.publish_label = QtWidgets.QLabel("Published Versions")
        self.publish_label.setAlignment(QtCore.Qt.AlignCenter) 
        self.publish_list = QtWidgets.QTreeWidget()
        self.publish_list.setHeaderLabels(["Version"])

        self.new_file_btn = QtWidgets.QPushButton("New File")
        self.open_file_btn = QtWidgets.QPushButton("Open File")

    def create_layout(self):
        """Create all layouts and add widgets to them"""
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
        self.wip_list.itemClicked.connect(self.focus_list)
        self.publish_list.itemClicked.connect(self.focus_list)
        self.new_file_btn.pressed.connect(self.create_new_file)
        self.open_file_btn.pressed.connect(self.open_file)

    def focus_list(self, list_item_widget):
        self.wip_list.clearSelection()
        self.publish_list.clearSelection()

        list_item_widget.treeWidget().setCurrentItem(list_item_widget)
        self.focused_version_item = list_item_widget

    def show_asset_versions(self, tree_item):
        self.wip_list.clear()
        self.publish_list.clear()
        
        parents = 0
        parent = tree_item.parent()

        while parent:
            parents += 1
            parent = parent.parent()

        if parents == 2:
            asset_part_item = self.assets_tree.currentItem()
            asset_part = asset_part_item.text(0)
            asset_name_item = asset_part_item.parent()
            asset_name = asset_name_item.text(0)
            asset_type_item = asset_name_item.parent()
            asset_type = asset_type_item.text(0)
            
            wip_asset_files = self.dcc_interface.get_native_asset_files(asset_name, asset_type, asset_part, "wip")
            if wip_asset_files:
                for wip_asset_file in reversed(wip_asset_files):
                    wip_asset_version = wip_asset_file.stem.rsplit("_", 1)[1]
                    wip_asset_item = QtWidgets.QTreeWidgetItem([wip_asset_version])
                    wip_asset_item.setData(0, QtCore.Qt.UserRole, wip_asset_file)
                    self.wip_list.addTopLevelItem(wip_asset_item)
                
            published_asset_files = self.dcc_interface.get_native_asset_files(asset_name, asset_type, asset_part, "publishes")
            if published_asset_files:
                for published_asset_file in reversed(published_asset_files):
                    published_asset_version = published_asset_file.stem.rsplit("_", 1)[1]
                    published_asset_item = QtWidgets.QTreeWidgetItem([published_asset_version])
                    published_asset_item.setData(0, QtCore.Qt.UserRole, published_asset_file)
                    self.publish_list.addTopLevelItem(published_asset_item)

    def create_new_file(self):
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

        self.window().close()

    def open_file(self):
        file_path = self.focused_version_item.data(0, QtCore.Qt.UserRole)
        self.dcc_interface.open_file(file_path)

        self.window().close()
