try:
    from PySide6 import QtCore
    from PySide6 import QtWidgets
except:
    from PySide2 import QtCore
    from PySide2 import QtWidgets

import utils.file_folder_utils as ffu


class ShotTaskTreeWidget(QtWidgets.QTreeWidget):
    def __init__(self, extra_info: bool = True, uid: str = ""):
        super().__init__()

        self.main_workspace_path = ffu.get_main_workspace_path()
        self.extra_info = extra_info

        if self.extra_info:
            self.setHeaderLabels(["Shot Tasks", "Assignees", "Progress"])
        else:
            self.setHeaderLabels(["Shot Tasks"])

        if not uid:
            self.generate_tree()
        else:
            self.generate_specific_user_tree(uid)

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

                steps = [x for x in shot.iterdir() if x.is_dir()]

                for step in steps:
                    step_item = QtWidgets.QTreeWidgetItem()
                    step_item.setText(0, step.name)
                    shot_item.addChild(step_item)

                    tasks = [x for x in step.iterdir() if x.is_dir()]

                    for task in tasks:
                        task_item = QtWidgets.QTreeWidgetItem()
                        task_item.setText(0, task.name)
                        step_item.addChild(task_item)

                        if self.extra_info:
                            assignments = self.assignment_data
                            assignees = []
                            completed = False

                            for assignment in assignments.values():
                                if (assignment["entity_type"] == "shot"
                                    and assignment["sequence_name"] == sequence.name
                                    and assignment["shot_name"] == shot.name
                                    and assignment["step_name"] == step.name
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

                            shot_task_path = str(ffu.get_main_workspace_path() / "sequences" / sequence / shot / step / task)

                            # Store assignment information in all asset part cells for later use
                            assignment_data = {
                                "entity_type": "shot",
                                "sequence_name": sequence.name,
                                "shot_name": shot.name,
                                "step_name": step.name,
                                "task_name": task.name,
                                "task_path": shot_task_path,
                                "assignees": assignees,
                                "completed": completed
                            }

                            task_item.setData(1, QtCore.Qt.UserRole, assignment_data)

        self.addTopLevelItems(top_level_items)
        self.expandAll()
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def generate_specific_user_tree(self, uid: str):
        tree_model = self.model()
        tree_model.removeRows(0, tree_model.rowCount())

        assignments = ffu.get_assignment_data()

        top_level_items = []

        for assignment in assignments.values():
            if assignment["entity_type"] == "shot" and uid in assignment["assignees"]:
                seqeunce_item = QtWidgets.QTreeWidgetItem()
                seqeunce_item.setText(0, assignment["sequence_name"])
                top_level_items.append(seqeunce_item)

                shot_item = QtWidgets.QTreeWidgetItem()
                shot_item.setText(0, assignment["shot_name"])
                seqeunce_item.addChild(shot_item)

                step_name_item = QtWidgets.QTreeWidgetItem()
                step_name_item.setText(0, assignment["step_name"])
                shot_item.addChild(step_name_item)   

                task_item = QtWidgets.QTreeWidgetItem()
                task_item.setText(0, assignment["task_name"])
                step_name_item.addChild(task_item)                 

        self.addTopLevelItems(top_level_items)
        self.expandAll()
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
