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


class AssignmentTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        config_path = hf.get_code_dir() / "config.json"

        with open(str(config_path), 'r') as file:
            config_data = json.load(file)
            self.main_folder_path = Path(config_data["main_folder_path"])
            self.assignment_data_path = Path(config_data["assignment_data_path"])

        self.assignment_data = hf.get_assignment_data()

        self.users = hf.get_users()

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create all widgets for the UI"""

        # Tab 2: Assignment
        self.assignment_type_dropdown = QtWidgets.QComboBox()
        self.assignment_type_dropdown.addItems(["Asset", "Sequence/Shot"])

        self.users_list = QtWidgets.QListWidget()
        self.users_list.addItems(self.users)

        self.assignment_btn = QtWidgets.QPushButton("Assign")

        self.assets_tree = QtWidgets.QTreeWidget()
        self.assets_tree.setHeaderLabels(["Assets", "Assignees"])

    def create_layout(self):
        assignment_layout = QtWidgets.QHBoxLayout(self)

        assignment_menu_layout = QtWidgets.QVBoxLayout()
        assignment_menu_layout.addWidget(self.assignment_type_dropdown)
        assignment_menu_layout.addWidget(self.users_list)
        assignment_menu_layout.addWidget(self.assignment_btn)

        assignment_table_layout = QtWidgets.QVBoxLayout()
        assignment_table_layout.addWidget(self.assets_tree)

        assignment_layout.addLayout(assignment_menu_layout, 1)
        assignment_layout.addLayout(assignment_table_layout, 5)

    def create_connections(self):
        """Create all connections for the UI"""
        self.assignment_btn.pressed.connect(self.assign_user)

    def show_asset_assignment_table(self, *_):
        tree_model = self.assets_tree.model()
        tree_model.removeRows(0, tree_model.rowCount())

        self.assignment_data = hf.get_assignment_data()

        assets_path = self.main_folder_path / "assets"
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

                    assignments = self.assignment_data["assignments"]
                    assignees = []
                    for assignment in assignments:
                        if (assignment["main_type"] == "asset" 
                            and assignment["asset_type"] == assets_type.name
                            and assignment["asset_name"] == asset.name
                            and assignment["asset_part"] == asset_part.name 
                            ):
                            assignees.append(assignment["assignee"])

                            asset_part_item.setText(1, ", ".join(assignees))

                    # Store assignment information in all asset part cells for later use
                    assignment_data = {
                        "main_type": "asset",
                        "asset_type": assets_type.name,
                        "asset_name": asset.name,
                        "asset_part": asset_part.name
                    }

                    asset_part_item.setData(1, QtCore.Qt.UserRole, assignment_data)

        self.assets_tree.addTopLevelItems(top_level_items)
        self.assets_tree.expandAll()
        self.assets_tree.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def assign_user(self):
        selected_user_item = self.users_list.currentItem()
        if not selected_user_item:
            QtWidgets.QMessageBox.warning(
                None, 
                "Assignment Error", 
                "Please select a user to assign."
            )
            return

        selected_user = selected_user_item.text()
        assignment_table_item = self.assets_tree.currentItem()
        assignment_table_item_index = self.assets_tree.currentIndex()

        # Checks that there must be at least two parents to signify that a
        # asset part has been selected
        count = 0
        while assignment_table_item_index.parent().isValid():
            count += 1
            assignment_table_item_index = assignment_table_item_index.parent()

        if count != 2:
            QtWidgets.QMessageBox.warning(
                None, 
                "Assignment Error", 
                "Select an asset part."
            )
            return

        # Gather assignment data from an asset part cell for comparison
        assignment_data = assignment_table_item.data(1, QtCore.Qt.UserRole)

        if assignment_data:
            assignment_data["assignee"] = selected_user

            with open(self.assignment_data_path, 'r') as file:
                data = json.load(file)
                for assignment in data["assignments"]:
                    if (assignment["main_type"] == assignment_data["main_type"]
                        and assignment["asset_name"] == assignment_data["asset_name"]
                        and assignment["asset_part"] == assignment_data["asset_part"]
                        and assignment["assignee"] == selected_user):
                        QtWidgets.QMessageBox.warning(
                        None, 
                        "Assignment Error", 
                        "Assignee already assigned to this asset part."
                        )
                        return
                    
                data["assignments"].append(assignment_data)

            with open(self.assignment_data_path, 'w') as file:
                json.dump(data, file, indent=4)

            self.assignment_data = data
            print(f"Assigned: {assignment_data}")

            self.show_asset_assignment_table(1)
        else:
            QtWidgets.QMessageBox.warning(
                None, 
                "Assignment Error", 
                "Select a valid cell in the assignee column."
            )
            return
