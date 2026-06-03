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


class ShotTaskTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, extra_info: bool = True):
        super().__init__()

        self.main_workspace_path = ffu.get_main_workspace_path()
        self.extra_info = extra_info

        if self.extra_info:
            self.setHeaderLabels(["Shot Tasks", "Assignees", "Progress"])
        else:
            self.setHeaderLabels(["Shot Tasks"])

        self.generate_tree()

    def generate_tree(self):
        tree_model = self.model()
        tree_model.removeRows(0, tree_model.rowCount())

        self.assignment_data = ffu.get_assignment_data()

        sequences_path = self.main_workspace_path / "sequences"
        sequences = [x for x in sequences_path.iterdir() if x.is_dir()]

        top_level_items = []

        # Loop through all of the sequences folder to store assignment information 
        # about the shot tasks and display who has been assigned already
        for sequence in sequences:
            sequence_item = QtWidgets.QTreeWidgetItem()
            sequence_item.setText(0, sequence.name)

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

                        if self.extra_info:
                            assignments = self.assignment_data
                            assignees = []
                            completed = False

                            for assignment in assignments.values():
                                if (assignment["entity_type"] == "shot"
                                    and assignment["sequence_name"] == sequence.name
                                    and assignment["shot_name"] == shot.name
                                    and assignment["shot_dep"] == department.name
                                    and assignment["task_name"] == task.name 
                                    ):
                                    assignees = assignment["assignees"]
                                    assignees_names = []

                                    for assignee_uid in assignment["assignees"]:
                                        assignee_name = ffu.get_user_name(assignee_uid)
                                        assignees_names.append(assignee_name)

                                    task_item.setText(1, ", ".join(assignees_names))

                                    completed = assignment["completed"]

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
                                "assignees": assignees,
                                "completed": completed
                            }

                            task_item.setData(1, QtCore.Qt.UserRole, assignment_data)

        self.addTopLevelItems(top_level_items)
        self.expandAll()
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
