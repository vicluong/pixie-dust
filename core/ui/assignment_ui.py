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


class AssignmentTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

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

        # Tab 2: Assignment
        self.assignment_type_dropdown = QtWidgets.QComboBox()
        self.assignment_type_dropdown.addItems(["Asset", "Sequence/Shot"])

        self.users_list = QtWidgets.QListWidget()
        self.users_list.addItems(self.users)

        self.assignment_btn = QtWidgets.QPushButton("Toggle Assignment")
        self.toggle_progress_btn = QtWidgets.QPushButton("Toggle Progress")

        self.assets_tree = QtWidgets.QTreeWidget()
        self.assets_tree.setHeaderLabels(["Assets", "Assignees", "Progress"])

        self.shot_tasks_tree = QtWidgets.QTreeWidget()
        self.shot_tasks_tree.setHeaderLabels(["Shot Tasks", "Assignees", "Progress"])

    def create_layout(self):
        assignment_layout = QtWidgets.QHBoxLayout(self)

        assignment_menu_layout = QtWidgets.QVBoxLayout()
        assignment_menu_layout.addWidget(self.assignment_type_dropdown)
        assignment_menu_layout.addWidget(self.users_list)
        assignment_menu_layout.addWidget(self.assignment_btn)
        assignment_menu_layout.addWidget(self.toggle_progress_btn)

        assignment_table_layout = QtWidgets.QVBoxLayout()
        assignment_table_layout.addWidget(self.assets_tree)

        assignment_layout.addLayout(assignment_menu_layout, 1)
        assignment_layout.addLayout(assignment_table_layout, 5)

    def create_connections(self):
        """Create all connections for the UI"""
        self.assignment_btn.pressed.connect(self.assign_task_to_user)
        self.toggle_progress_btn.pressed.connect(self.toggle_progress_of_task)
        self.assignment_type_dropdown.currentIndexChanged.connect(self.show_assignment_table)

    def show_assignment_table(self):
        if self.assignment_type_dropdown.currentText == "Asset":
            self.show_asset_assignment_table()
        else:
            self.show_shot_task_assignment_table()

    def show_asset_assignment_table(self, *_):
        tree_model = self.assets_tree.model()
        tree_model.removeRows(0, tree_model.rowCount())

        self.assignment_data = ffu.get_assignment_data()

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

                    assignments = self.assignment_data
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

                    # Store assignment information in all asset part cells for later use
                    assignment_data = {
                        "entity_type": "asset",
                        "asset_type": assets_type.name,
                        "asset_name": asset.name,
                        "asset_part": asset_part.name,
                        "assignees": assignees,
                        "completed": completed
                    }

                    asset_part_item.setData(1, QtCore.Qt.UserRole, assignment_data)

        self.assets_tree.addTopLevelItems(top_level_items)
        self.assets_tree.expandAll()
        self.assets_tree.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def show_shot_task_assignment_table(self):
        """
        tree_model = self.shot_tasks_tree.model()
        tree_model.removeRows(0, tree_model.rowCount())

        self.assignment_data = ffu.get_assignment_data()

        sequences_path = self.main_folder_path / "sequences"
        sequences = [x for x in sequences_path.iterdir() if x.is_dir()]

        top_level_items = []

        # Loop through all of the sequences folder to store assignment information 
        # about the shot tasks and display who has been assigned already
        for sequence in sequences:
            sequence_item = QtWidgets.QTreeWidgetItem()
            sequence.setText(0, sequence.name)

            top_level_items.append(sequence_item)

            shots = [x for x in sequence.iterdir() if x.is_dir()]

            for shot in shots:
                shot_item = QtWidgets.QTreeWidgetItem()
                shot_item.setText(0, shot.name)
                sequence_item.addChild(shot_item)

                department_path = shot / "departments"

                departments = [x for x in department_path.iterdir() if x.is_dir()]

                for department in departments:
                    department_item = QtWidgets.QTreeWidgetItem()
                    department_item.setText(0, department.name)
                    shot_item.addChild(department_item)

                    tasks = [x for x in department.iterdir() if x.is_dir()]

                    for task in tasks:
                        task_item = QtWidgets.QTreeWidgetItem()
                        task_item.setText(0, task.name)
                        department_item.addChild(task_item)

                        assignments = self.assignment_data
                        assignees = []
                        for assignment in assignments.values():
                            if (assignment["entity_type"] == "shot"
                                and assignment["sequence_name"] == sequence.name
                                and assignment["shot_name"] == shot.name
                                and assignment["shot_dep"] == department.name
                                and assignment["task_name"] == task.name 
                                ):

                                assignee = ffu.get_user_name(assignment["assignee"])
                                assignees.append(assignee)

                                if assignment["completed"]:
                                    task_item.setText(2, "Completed")
                                else:
                                    task_item.setText(2, "In Progress")

                        # Store assignment information in all asset part cells for later use
                        assignment_data = {
                            "entity_type": "shot",
                            "sequence_name": sequence.name,
                            "shot_name": shot.name,
                            "shot_dep": department.name,
                            "task_name": task.name,
                        }

                        task_item.setData(1, QtCore.Qt.UserRole, assignment_data)

        self.shot_tasks_tree.addTopLevelItems(top_level_items)
        self.shot_tasks_tree.expandAll()
        self.shot_tasks_tree.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
"""
    def assign_task_to_user(self):
        if self.assignment_type_dropdown.currentText() == "Asset":
            self.assign_asset_to_user()
        else:
            self.assign_shot_task_to_user()

    def assign_asset_to_user(self):
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
                    and assignment["asset_part"] == assignment_cell_data["asset_part"]):
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

            print(f"Toggled Assignment: {self.assignment_data}")

            self.show_asset_assignment_table(1)
        else:
            QtWidgets.QMessageBox.warning(
                None, 
                "Assignment Error", 
                "Select a valid cell in the assignee column."
            )
            return

    def assign_shot_task_to_user(self):
        pass

    def toggle_progress_of_task(self):
        if self.assignment_type_dropdown.currentText() == "Asset":
            self.toggle_progress_of_asset_task()
        else:
            self.toggle_progress_of_shot_task()

    def toggle_progress_of_asset_task(self):
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
                    and assignment["asset_part"] == assignment_cell_data["asset_part"]):
                    print("Accepted")
                    print(assignment_cell_data["completed"])
                    print(self.assignment_data[ass_id]["completed"])
                    self.assignment_data[ass_id]["completed"] = not assignment_cell_data["completed"]
                    print(self.assignment_data[ass_id]["completed"])
                    assignment_exists = True
            
            if not assignment_exists:
                print("Not")
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
        pass
