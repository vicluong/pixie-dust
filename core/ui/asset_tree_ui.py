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


class AssetTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, extra_info: bool, uid: str = ""):
        super().__init__()

        self.main_workspace_path = ffu.get_main_workspace_path()
        self.extra_info = extra_info

        if self.extra_info:
            self.setHeaderLabels(["Assets", "Assignees", "Progress"])
        else:
            self.setHeaderLabels(["Assets"])

        if not uid:
            self.generate_tree()
        else:
            self.generate_specific_user_tree(uid)

    def generate_tree(self):
        tree_model = self.model()
        tree_model.removeRows(0, tree_model.rowCount())

        assignments = ffu.get_assignment_data()

        assets_path = self.main_workspace_path / "assets"
        assets_types = [x for x in assets_path.iterdir() if x.is_dir()]

        top_level_items = []

        # Loop through all of the assets folder to store assignment information 
        # about the asset parts and display who has been assigned already
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

                    if self.extra_info:
                        assignees = []
                        completed = False

                        for assignment in assignments.values():
                            if (assignment["entity_type"] == "asset" 
                                and assignment["asset_type"] == assets_type.name
                                and assignment["asset_name"] == asset.name
                                and assignment["asset_part"] == asset_part.name 
                                ):

                                assignees = assignment["assignees"]
                                assignees_names = []

                                for assignee_uid in assignment["assignees"]:
                                    assignee_name = ffu.get_user_name(assignee_uid)
                                    assignees_names.append(assignee_name)

                                asset_part_item.setText(1, ", ".join(assignees_names))

                                completed = assignment["completed"]

                                if assignment["completed"]:
                                    asset_part_item.setText(2, "Completed")
                                else:
                                    asset_part_item.setText(2, "In Progress")

                        asset_path = str(ffu.get_main_workspace_path() / "assets" / assets_type.name / asset.name / asset_part.name)

                        # Store assignment information in all asset part cells for later use
                        assignment_data = {
                            "entity_type": "asset",
                            "asset_type": assets_type.name,
                            "asset_name": asset.name,
                            "asset_part": asset_part.name,
                            "task_path": str(asset_path),
                            "assignees": assignees,
                            "completed": completed
                        }

                        asset_part_item.setData(1, QtCore.Qt.UserRole, assignment_data)

        self.addTopLevelItems(top_level_items)
        self.expandAll()
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def generate_specific_user_tree(self, uid: str):
        tree_model = self.model()
        tree_model.removeRows(0, tree_model.rowCount())

        assignments = ffu.get_assignment_data()

        top_level_items = []

        for assignment in assignments.values():
            if assignment["entity_type"] == "asset" and uid in assignment["assignees"]:
                asset_type_item = QtWidgets.QTreeWidgetItem()
                asset_type_item.setText(0, assignment["asset_type"])
                top_level_items.append(asset_type_item)

                asset_name_item = QtWidgets.QTreeWidgetItem()
                asset_name_item.setText(0, assignment["asset_name"])
                asset_type_item.addChild(asset_name_item)

                asset_part_item = QtWidgets.QTreeWidgetItem()
                asset_part_item.setText(0, assignment["asset_part"])
                asset_name_item.addChild(asset_part_item)                

        self.addTopLevelItems(top_level_items)
        self.expandAll()
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
