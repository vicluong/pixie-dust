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

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create all widgets for the UI"""

        # Tab 2: Assignment
        self.assignment_type_dropdown = QtWidgets.QComboBox()
        self.assignment_type_dropdown.addItems(["Asset", "Sequence/Shot"])

        self.users_list = QtWidgets.QListWidget()
        self.users_list.addItems(self.assignment_data["users"])

        self.assignment_btn = QtWidgets.QPushButton("Assign")

        self.assignment_table = QtWidgets.QTableWidget()

    def create_layout(self):
        assignment_layout = QtWidgets.QHBoxLayout(self)

        assignment_menu_layout = QtWidgets.QVBoxLayout()
        assignment_menu_layout.addWidget(self.assignment_type_dropdown)
        assignment_menu_layout.addWidget(self.users_list)
        assignment_menu_layout.addWidget(self.assignment_btn)

        assignment_table_layout = QtWidgets.QVBoxLayout()
        assignment_table_layout.addWidget(self.assignment_table)

        assignment_layout.addLayout(assignment_menu_layout, 1)
        assignment_layout.addLayout(assignment_table_layout, 5)

    def create_connections(self):
        """Create all connections for the UI"""
        self.assignment_btn.pressed.connect(self.assign_user)

    def show_asset_assignment_table(self, *_):
        self.assignment_data = hf.get_assignment_data()
        print(self.assignment_data)

        assets_path = self.main_folder_path / "assets"
        assets_types = [x for x in assets_path.iterdir() if x.is_dir()]

        self.assignment_table.setColumnCount(4)
        self.assignment_table.setHorizontalHeaderLabels(["Asset Type", "Asset Name", "Asset Part", "Assignees"])
        self.assignment_table.setRowCount(0)
        self.assignment_table.verticalHeader().setVisible(False)

        for assets_type in assets_types:
            index = self.assignment_table.rowCount()
            self.assignment_table.setRowCount(index + 1)

            asset_type_item = QtWidgets.QTableWidgetItem(assets_type.name)
            self.assignment_table.setItem(index, 0, asset_type_item)
            self.assignment_table.setSpan(index, 0, 1, 3)

            n_a_item = QtWidgets.QTableWidgetItem("N/A")
            self.assignment_table.setItem(index, 3, n_a_item)

            assets = [x for x in assets_type.iterdir() if x.is_dir()]

            for asset in assets:
                index = self.assignment_table.rowCount()
                self.assignment_table.setRowCount(index + 1)

                asset_item = QtWidgets.QTableWidgetItem(asset.name)
                self.assignment_table.setItem(index, 1, asset_item)
                self.assignment_table.setSpan(index, 1, 1, 2)

                n_a_item = QtWidgets.QTableWidgetItem("N/A")
                self.assignment_table.setItem(index, 3, n_a_item)

                asset_parts = [x for x in asset.iterdir() if x.is_dir()]

                for asset_part in asset_parts:
                    index = self.assignment_table.rowCount()
                    self.assignment_table.setRowCount(index + 1)

                    asset_part_item = QtWidgets.QTableWidgetItem(asset_part.name)
                    self.assignment_table.setItem(index, 2, asset_part_item)

                    assignments = self.assignment_data["assignments"]

                    assignees = []

                    for assignment in assignments:
                        if (assignment["main_type"] == "asset" 
                            and assignment["asset_type"] == assets_type.name
                            and assignment["asset_name"] == asset.name
                            and assignment["asset_part"] == asset_part.name 
                            ):
                            assignees.append(assignment["assignee"])
                    
                    assignment_item = QtWidgets.QTableWidgetItem(", ".join(assignees))

                    assignment_data = {
                        "main_type": "asset",
                        "asset_type": assets_type.name,
                        "asset_name": asset.name,
                        "asset_part": asset_part.name
                    }

                    assignment_item.setData(QtCore.Qt.UserRole, assignment_data)
                    self.assignment_table.setItem(index, 3, assignment_item)

        self.assignment_table.resizeColumnsToContents()

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
        assignment_table_item = self.assignment_table.currentItem()

        if not assignment_table_item:
            QtWidgets.QMessageBox.warning(
                None, 
                "Assignment Error", 
                "Select an assignee cell next to the asset part you want to assign the user to."
            )
            return

        assignment_data = assignment_table_item.data(QtCore.Qt.UserRole)

        print(f"First assignment: {assignment_data}")

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
                "Select a valid assignee cell."
            )
            return
