try:
    from PySide6 import QtWidgets
except:
    from PySide2 import QtWidgets

import utils.file_folder_utils as ffu
from dcc_manager.dcc_interface import DCCInterface
from ui.asset_tree_ui import AssetTreeWidget
from ui.shot_task_tree_ui import ShotTaskTreeWidget


class CreationTab(QtWidgets.QWidget):
    def __init__(self, dcc_interface: DCCInterface):
        super().__init__()

        self.dcc_interface = dcc_interface
        self.main_workspace_path = ffu.get_main_workspace_path()

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create all widgets for the UI"""
        # Tab 1: Creation
        self.creation_type_dropdown = QtWidgets.QComboBox()
        self.creation_type_dropdown.addItems(["Asset", "Sequence/Shot"])

            # Asset
        self.create_asset_dropdown = QtWidgets.QComboBox()
        self.create_asset_dropdown.addItems(["camera", "character", "charfx", "fx", "prop", "set", "setPiece"])
        self.create_asset_le = QtWidgets.QLineEdit()
        self.create_asset_btn = QtWidgets.QPushButton("Create Asset")

            # Sequence
        self.create_sequence_le = QtWidgets.QLineEdit()
        self.create_sequence_btn = QtWidgets.QPushButton("Create Sequence")

            # Shot
        self.create_shot_le = QtWidgets.QLineEdit()
        self.create_shot_label = QtWidgets.QLabel("Select a sequence from the list to the right.")
        self.create_shot_btn = QtWidgets.QPushButton("Create Shot")

            # Shot Task
        self.create_shot_task_le = QtWidgets.QLineEdit()
        self.create_shot_task_label = QtWidgets.QLabel("Select a shot step from the list to the right.")
        self.create_shot_task_btn = QtWidgets.QPushButton("Create Shot Task")

        self.asset_tree = AssetTreeWidget(extra_info=True)
        self.shot_tree = ShotTaskTreeWidget(extra_info=True)
        self.shot_tree.setVisible(False)

    def create_layout(self):
        # Tab 1: Creation
        creation_layout = QtWidgets.QHBoxLayout(self)

        creation_menu_layout = QtWidgets.QVBoxLayout()

        creation_tree_layout = QtWidgets.QVBoxLayout()
        creation_tree_layout.addWidget(self.asset_tree)
        creation_tree_layout.addWidget(self.shot_tree)

        creation_layout.addLayout(creation_menu_layout)
        creation_layout.addLayout(creation_tree_layout)

        creation_type__form_layout = QtWidgets.QFormLayout()
        creation_type__form_layout.addRow("Create:", self.creation_type_dropdown)
        creation_menu_layout.addLayout(creation_type__form_layout)

            # Asset Layout
        self.creation_asset_widget = QtWidgets.QWidget()
        creation_asset_layout = QtWidgets.QVBoxLayout()

        creation_asset_form_layout = QtWidgets.QFormLayout()
        creation_asset_form_layout.addRow("Asset Type:", self.create_asset_dropdown)
        creation_asset_form_layout.addRow("Asset Name:", self.create_asset_le)
        creation_asset_layout.addLayout(creation_asset_form_layout)

        creation_asset_layout.addWidget(self.create_asset_btn)

        creation_asset_layout.addStretch()
        self.creation_asset_widget.setLayout(creation_asset_layout)
        creation_menu_layout.addWidget(self.creation_asset_widget)

            # Shot / Sequence Layout
        self.creation_shot_sequence_widget = QtWidgets.QWidget()
        self.creation_shot_sequence_layout = QtWidgets.QVBoxLayout()
        self.creation_shot_sequence_widget.setLayout(self.creation_shot_sequence_layout)

            # Sequence Layout
        creation_sequence_group = QtWidgets.QGroupBox("Sequence")
        creation_sequence_layout = QtWidgets.QVBoxLayout()

        creation_sequence_form_layout = QtWidgets.QFormLayout()
        creation_sequence_form_layout.addRow("Sequence Name:", self.create_sequence_le)

        creation_sequence_layout.addLayout(creation_sequence_form_layout)
        creation_sequence_layout.addWidget(self.create_sequence_btn)

        creation_sequence_group.setLayout(creation_sequence_layout)

            # Shot Layout
        creation_shot_group = QtWidgets.QGroupBox("Shot")
        creation_shot_layout = QtWidgets.QVBoxLayout()

        creation_shot_form_layout = QtWidgets.QFormLayout()
        creation_shot_form_layout.addWidget(self.create_shot_label)
        creation_shot_form_layout.addRow("Shot Name:", self.create_shot_le)

        creation_shot_layout.addLayout(creation_shot_form_layout)
        creation_shot_layout.addWidget(self.create_shot_btn)

        creation_shot_group.setLayout(creation_shot_layout)

            # Shot Task Layout
        creation_shot_task_group = QtWidgets.QGroupBox("Shot Task")
        creation_shot_task_layout = QtWidgets.QVBoxLayout()

        creation_shot_task_form_layout = QtWidgets.QFormLayout()
        creation_shot_task_form_layout.addWidget(self.create_shot_task_label)
        creation_shot_task_form_layout.addRow("Shot Task Name:", self.create_shot_task_le)

        creation_shot_task_layout.addLayout(creation_shot_task_form_layout)
        creation_shot_task_layout.addWidget(self.create_shot_task_btn)

        creation_shot_task_group.setLayout(creation_shot_task_layout)

            # Add Groups
        self.creation_shot_sequence_layout.addWidget(creation_sequence_group)
        self.creation_shot_sequence_layout.addWidget(creation_shot_group)
        self.creation_shot_sequence_layout.addWidget(creation_shot_task_group)
        self.creation_shot_sequence_layout.addStretch()

        creation_menu_layout.addWidget(self.creation_shot_sequence_widget)

    def create_connections(self):
        """Create all connections for the UI"""
        self.creation_type_dropdown.currentTextChanged.connect(self.show_creation_type)
        self.create_asset_btn.pressed.connect(self.create_asset)
        self.create_sequence_btn.pressed.connect(self.create_sequence)
        self.create_shot_btn.pressed.connect(self.create_shot)
        self.create_shot_task_btn.pressed.connect(self.create_shot_task)

    def show_creation_type(self):
        creation_type = self.creation_type_dropdown.currentText()

        # self.creation_tree.verticalHeader().setVisible(False)
        self.creation_asset_widget.setVisible(False)
        self.creation_shot_sequence_widget.setVisible(False)

        if creation_type == "Asset":
            self.creation_asset_widget.setVisible(True)
            self.asset_tree.setVisible(True)
            self.shot_tree.setVisible(False)
            self.asset_tree.generate_tree()
        elif creation_type == "Sequence/Shot":
            self.creation_shot_sequence_widget.setVisible(True)
            self.asset_tree.setVisible(False)
            self.shot_tree.setVisible(True)
            self.shot_tree.generate_tree()

    def create_asset(self):
        asset_type = self.create_asset_dropdown.currentText()
        asset_name = self.create_asset_le.text()

        if not asset_name:
            QtWidgets.QMessageBox.warning(
                None, 
                "File Error", 
                f"Please input a name for the asset."
            )
            return

        try:
            ffu.create_asset_folders(self.main_workspace_path, asset_type, asset_name)
            QtWidgets.QMessageBox.information(
                None, 
                "Creation Succeeded", 
                f"Asset {asset_name} of asset type {asset_type} has been created."
            )
        except FileNotFoundError as e:
            QtWidgets.QMessageBox.warning(
                None, 
                "File Error", 
                f"{e}"
            )
        except FileExistsError as e:
            QtWidgets.QMessageBox.warning(
                None, 
                "File Error", 
                f"There is already an asset type of {asset_type} called {asset_name}."
            )
        self.show_creation_type()

    def create_sequence(self):
        sequence_name = self.create_sequence_le.text()

        if not sequence_name:
            QtWidgets.QMessageBox.warning(
                None, 
                "File Error", 
                f"Please input a name for the asset."
            )
            return

        sequence_path = self.main_workspace_path / "sequences" / sequence_name

        try:
            sequence_path.mkdir()
            QtWidgets.QMessageBox.information(
                None, 
                "Creation Succeeded", 
                f"Sequence {sequence_name} has been created."
            )
        except FileNotFoundError as e:
            QtWidgets.QMessageBox.warning(
                None, 
                "File Error", 
                f"{e}"
            )
        except FileExistsError as e:
            QtWidgets.QMessageBox.warning(
                None, 
                "File Error", 
                f"There is already a sequence called {sequence_name}."
            )
        self.show_creation_type()

    def create_shot(self):
        selected_item = self.shot_tree.currentItem()

        if not selected_item.parent():
            sequence_name = selected_item.text(0)
            shot_name = self.create_shot_le.text()

            if not shot_name:
                QtWidgets.QMessageBox.warning(
                    None, 
                    "File Error", 
                    f"Please input a name for the shot."
                )
                return

            shot_path = self.main_workspace_path / "sequences" / sequence_name / shot_name

            try:
                ffu.create_shot_folders(shot_path)
                QtWidgets.QMessageBox.information(
                    None, 
                    "Creation Succeeded", 
                    f"Shot {shot_name} has been created."
                )
            except FileNotFoundError as e:
                QtWidgets.QMessageBox.warning(
                    None, 
                    "File Error", 
                    f"{e}"
                )
            except FileExistsError as e:
                QtWidgets.QMessageBox.warning(
                    None, 
                    "File Error", 
                    f"There is already a shot called {shot_name}."
                )
        else:
            QtWidgets.QMessageBox.warning(
                None, 
                "Selection Error", 
                f"Select a sequence."
            )

        self.show_creation_type()

    def create_shot_task(self):
        selected_item = self.shot_tree.currentItem()

        count = 0
        item_iter = selected_item
        while item_iter.parent():
            count += 1
            item_iter = item_iter.parent()

        if count == 2:
            shot_task_name = self.create_shot_task_le.text()

            if not shot_task_name:
                QtWidgets.QMessageBox.warning(
                    None, 
                    "File Error", 
                    f"Please input a name for the shot task."
                )
                return

            step_name = selected_item.text(0)
            shot_name = selected_item.parent().text(0)
            sequence_name = selected_item.parent().parent().text(0)
            shot_task_path = self.main_workspace_path / "sequences" / sequence_name / shot_name / step_name / shot_task_name

            try:
                ffu.create_shot_task_folders(shot_task_path)
                QtWidgets.QMessageBox.information(
                    None, 
                    "Creation Succeeded", 
                    f"Shot task {shot_task_name} has been created."
                )
            except FileNotFoundError as e:
                QtWidgets.QMessageBox.warning(
                    None, 
                    "File Error", 
                    f"{e}"
                )
            except FileExistsError as e:
                QtWidgets.QMessageBox.warning(
                    None, 
                    "File Error", 
                    f"There is already a shot task called {shot_task_name}."
                )
        else:
            QtWidgets.QMessageBox.warning(
                None, 
                "Assignment Error", 
                "Select the step of a shot."
            )
            return

        self.show_creation_type()
