import json

try:
    from PySide6 import QtCore
    from PySide6 import QtWidgets
except:
    from PySide2 import QtCore
    from PySide2 import QtWidgets

import utils.file_folder_utils as ffu
from dcc_manager.dcc_interface import DCCInterface
from ui.asset_tree_ui import AssetTreeWidget
from ui.shot_task_tree_ui import ShotTaskTreeWidget


class AssignmentTab(QtWidgets.QWidget):
    def __init__(self, dcc_interface: DCCInterface):
        super().__init__()

        self.dcc_interface = dcc_interface
        self.main_workspace_path = ffu.get_main_workspace_path()
        self.assignment_data_path = ffu.get_assignment_data_path()
        self.assignment_data = ffu.get_assignment_data()
        self.users = ffu.get_users()

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

        self.assignment_btn = QtWidgets.QPushButton("Toggle Assignment")
        self.toggle_progress_btn = QtWidgets.QPushButton("Toggle Progress")

        self.assets_tree = AssetTreeWidget(extra_info=True)

        self.shot_tasks_tree = ShotTaskTreeWidget(extra_info=True)
        self.shot_tasks_tree.setVisible(False)

    def create_layout(self):
        assignment_layout = QtWidgets.QHBoxLayout(self)

        assignment_menu_layout = QtWidgets.QVBoxLayout()
        assignment_menu_layout.addWidget(self.assignment_type_dropdown)
        assignment_menu_layout.addWidget(self.users_list)
        assignment_menu_layout.addWidget(self.assignment_btn)
        assignment_menu_layout.addWidget(self.toggle_progress_btn)

        assignment_table_layout = QtWidgets.QVBoxLayout()
        assignment_table_layout.addWidget(self.assets_tree)
        assignment_table_layout.addWidget(self.shot_tasks_tree)

        assignment_layout.addLayout(assignment_menu_layout, 1)
        assignment_layout.addLayout(assignment_table_layout, 5)

    def create_connections(self):
        """Create all connections for the UI"""
        self.assignment_btn.pressed.connect(self.toggle_assignment_of_task)
        self.toggle_progress_btn.pressed.connect(self.toggle_progress_of_task)
        self.assignment_type_dropdown.currentIndexChanged.connect(self.show_assignment_table)

    def show_assignment_table(self):
        if self.assignment_type_dropdown.currentText() == "Asset":
            self.assets_tree.setVisible(True)
            self.shot_tasks_tree.setVisible(False)
            self.show_asset_assignment_table()
        else:
            self.assets_tree.setVisible(False)
            self.shot_tasks_tree.setVisible(True)
            self.show_shot_task_assignment_table()

    def show_asset_assignment_table(self, *_):
        self.assets_tree.generate_tree()

    def show_shot_task_assignment_table(self):
        self.shot_tasks_tree.generate_tree()

    def toggle_assignment_of_task(self):
        if self.assignment_type_dropdown.currentText() == "Asset":
            self.toggle_assignment_of_asset()
        else:
            self.toggle_assignment_of_shot_task()

    def toggle_assignment_of_asset(self):
        selected_user_item = self.users_list.currentItem()
        if not selected_user_item:
            QtWidgets.QMessageBox.warning(
                None, 
                "Assignment Error", 
                "Please select a user to assign/unassign."
            )
            return

        selected_user = ffu.get_uid(selected_user_item.text())
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
        assignment_cell_data = assignment_table_item.data(1, QtCore.Qt.UserRole)

        if assignment_cell_data:
            self.assignment_data = ffu.get_assignment_data()

            assignment_exists = False
            # If the assignment already exists, remove or add the uid from the existing users
            for ass_id, assignment in self.assignment_data.items():
                if (assignment["entity_type"] == assignment_cell_data["entity_type"]
                    and assignment["asset_name"] == assignment_cell_data["asset_name"]
                    and assignment["asset_step"] == assignment_cell_data["asset_step"]):
                    if selected_user in assignment["assignees"]:
                        self.assignment_data[ass_id]["assignees"].remove(selected_user)
                    else:
                        self.assignment_data[ass_id]["assignees"].append(selected_user)
                    assignment_exists = True
            
            if not assignment_exists:
                assignment_cell_data["assignees"].append(selected_user)

                # Get latest assignment id
                max_num = 0
                for key in self.assignment_data.keys():
                    num = int(key.removeprefix("ass"))
                    max_num = max(max_num, num)
                padded_value = f"{max_num+1:04d}"

                self.assignment_data[f"ass{padded_value}"] = assignment_cell_data

            with open(self.assignment_data_path, 'w') as file:
                json.dump(self.assignment_data, file, indent=4)

            self.show_asset_assignment_table(1)
        else:
            QtWidgets.QMessageBox.warning(
                None, 
                "Assignment Error", 
                "Select a valid cell in the assignee column."
            )
            return
        
    def toggle_assignment_of_shot_task(self):
        selected_user_item = self.users_list.currentItem()
        if not selected_user_item:
            QtWidgets.QMessageBox.warning(
                None, 
                "Assignment Error", 
                "Please select a user to assign/unassign."
            )
            return

        selected_user = ffu.get_uid(selected_user_item.text())
        assignment_table_item = self.shot_tasks_tree.currentItem()

        count = 0
        item_iter = assignment_table_item
        while item_iter.parent():
            count += 1
            item_iter = item_iter.parent()

        if count != 3:
            QtWidgets.QMessageBox.warning(
                None, 
                "Assignment Error", 
                "Select a shot task."
            )
            return

        # Gather assignment data from a shot task cell for comparison
        assignment_cell_data = assignment_table_item.data(1, QtCore.Qt.UserRole)

        if assignment_cell_data:
            self.assignment_data = ffu.get_assignment_data()

            assignment_exists = False
            # If the assignment already exists, remove or add the uid from the existing users
            for ass_id, assignment in self.assignment_data.items():
                if (assignment["entity_type"] == "shot"
                    and assignment["sequence"] == assignment_cell_data["sequence"]
                    and assignment["shot"] == assignment_cell_data["shot"]
                    and assignment["step"] == assignment_cell_data["step"]
                    and assignment["task"] == assignment_cell_data["task"]
                    ):
                    if selected_user in assignment["assignees"]:
                        self.assignment_data[ass_id]["assignees"].remove(selected_user)
                    else:
                        self.assignment_data[ass_id]["assignees"].append(selected_user)
                    assignment_exists = True
            
            if not assignment_exists:
                assignment_cell_data["assignees"].append(selected_user)

                # Get latest assignment id
                max_num = 0
                for key in self.assignment_data.keys():
                    num = int(key.removeprefix("ass"))
                    max_num = max(max_num, num)
                padded_value = f"{max_num+1:04d}"

                self.assignment_data[f"ass{padded_value}"] = assignment_cell_data

            with open(self.assignment_data_path, 'w') as file:
                json.dump(self.assignment_data, file, indent=4)

            self.show_shot_task_assignment_table()
        else:
            QtWidgets.QMessageBox.warning(
                None, 
                "Assignment Error", 
                "Select a valid cell in the assignee column."
            )
            return

    def toggle_progress_of_task(self):
        if self.assignment_type_dropdown.currentText() == "Asset":
            self.toggle_progress_of_asset_task()
        else:
            self.toggle_progress_of_shot_task()

    def toggle_progress_of_asset_task(self):
        assignment_table_item = self.assets_tree.currentItem()

        count = 0
        item_iter = assignment_table_item
        while item_iter.parent():
            count += 1
            item_iter = item_iter.parent()

        if count != 2:
            QtWidgets.QMessageBox.warning(
                None, 
                "Assignment Error", 
                "Select an asset part."
            )
            return

        # Gather assignment data from an asset part cell for comparison
        assignment_cell_data = assignment_table_item.data(1, QtCore.Qt.UserRole)

        if assignment_cell_data:
            self.assignment_data = ffu.get_assignment_data()

            assignment_exists = False
            # If the assignment already exists, remove or add the uid from the existing users
            for ass_id, assignment in self.assignment_data.items():
                if (assignment["entity_type"] == assignment_cell_data["entity_type"]
                    and assignment["asset_name"] == assignment_cell_data["asset_name"]
                    and assignment["asset_step"] == assignment_cell_data["asset_step"]
                    ):
                    self.assignment_data[ass_id]["completed"] = not assignment_cell_data["completed"]
                    assignment_exists = True
            
            if not assignment_exists:
                assignment_cell_data["completed"] = True

                # Get latest assignment id
                max_num = 0
                for key in self.assignment_data.keys():
                    num = int(key.removeprefix("ass"))
                    max_num = max(max_num, num)
                padded_value = f"{max_num+1:04d}"

                self.assignment_data[f"ass{padded_value}"] = assignment_cell_data

            with open(self.assignment_data_path, 'w') as file:
                json.dump(self.assignment_data, file, indent=4)

            self.show_asset_assignment_table(1)

    def toggle_progress_of_shot_task(self):
        assignment_table_item = self.shot_tasks_tree.currentItem()

        count = 0
        item_iter = assignment_table_item
        while item_iter.parent():
            count += 1
            item_iter = item_iter.parent()

        if count != 3:
            QtWidgets.QMessageBox.warning(
                None, 
                "Assignment Error", 
                "Select a shot task."
            )
            return

        # Gather assignment data from an asset part cell for comparison
        assignment_cell_data = assignment_table_item.data(1, QtCore.Qt.UserRole)

        if assignment_cell_data:
            self.assignment_data = ffu.get_assignment_data()

            assignment_exists = False
            # If the assignment already exists, remove or add the uid from the existing users
            for ass_id, assignment in self.assignment_data.items():
                if (assignment["entity_type"] == "shot"
                    and assignment["sequence"] == assignment_cell_data["sequence"]
                    and assignment["shot"] == assignment_cell_data["shot"]
                    and assignment["step"] == assignment_cell_data["step"]
                    and assignment["task"] == assignment_cell_data["task"]
                    ):
                    self.assignment_data[ass_id]["completed"] = not assignment_cell_data["completed"]
                    assignment_exists = True
            
            if not assignment_exists:
                assignment_cell_data["completed"] = True

                # Get latest assignment id
                max_num = 0
                for key in self.assignment_data.keys():
                    num = int(key.removeprefix("ass"))
                    max_num = max(max_num, num)
                padded_value = f"{max_num+1:04d}"

                self.assignment_data[f"ass{padded_value}"] = assignment_cell_data

            with open(self.assignment_data_path, 'w') as file:
                json.dump(self.assignment_data, file, indent=4)

            self.show_shot_task_assignment_table()
