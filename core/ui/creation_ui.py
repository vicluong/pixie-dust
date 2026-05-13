from pathlib import Path
import json
import sys

try:
    from PySide6 import QtWidgets
except:
    from PySide2 import QtWidgets

import core.utils.file_folder_utils as hf


class CreationTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        config_path = hf.get_code_dir() / "config.json"

        with open(str(config_path), 'r') as file:
            config_data = json.load(file)
            self.main_folder_path = Path(config_data["main_folder_path"])
            self.assignment_data_path = Path(config_data["assignment_data_path"])

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
        self.create_shot_dropdown = QtWidgets.QComboBox()
        self.create_shot_le = QtWidgets.QLineEdit()
        self.create_shot_btn = QtWidgets.QPushButton("Create Shot")

        self.creation_tree = QtWidgets.QTableWidget()
        self.creation_tree = QtWidgets.QTreeWidget()
        self.creation_tree.setHeaderLabels(["Assets"])

    def create_layout(self):
        # Tab 1: Creation
        creation_layout = QtWidgets.QHBoxLayout(self)

        creation_menu_layout = QtWidgets.QVBoxLayout()

        creation_tree_layout = QtWidgets.QVBoxLayout()
        creation_tree_layout.addWidget(self.creation_tree)

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
        creation_shot_form_layout.addRow("Sequence:", self.create_shot_dropdown)
        creation_shot_form_layout.addRow("Shot Name:", self.create_shot_le)

        creation_shot_layout.addLayout(creation_shot_form_layout)
        creation_shot_layout.addWidget(self.create_shot_btn)

        creation_shot_group.setLayout(creation_shot_layout)

            # Add Groups
        self.creation_shot_sequence_layout.addWidget(creation_sequence_group)
        self.creation_shot_sequence_layout.addWidget(creation_shot_group)
        self.creation_shot_sequence_layout.addStretch()

        creation_menu_layout.addWidget(self.creation_shot_sequence_widget)

    def create_connections(self):
        """Create all connections for the UI"""
        self.creation_type_dropdown.currentTextChanged.connect(self.switch_creation_type)
        self.create_asset_btn.pressed.connect(self.create_asset)
        self.create_sequence_btn.pressed.connect(self.create_sequence)
        self.create_shot_btn.pressed.connect(self.create_shot)

    def switch_creation_type(self, *_):
        creation_type = self.creation_type_dropdown.currentText()

        # self.creation_tree.verticalHeader().setVisible(False)
        self.creation_asset_widget.setVisible(False)
        self.creation_shot_sequence_widget.setVisible(False)

        if creation_type == "Asset":
            self.creation_asset_widget.setVisible(True)
            self.show_creation_asset_widgets()
        elif creation_type == "Sequence/Shot":
            self.creation_shot_sequence_widget.setVisible(True)
            self.show_creation_shot_sequence_widgets()  

    def show_creation_asset_widgets(self):
        tree_model = self.creation_tree.model()
        tree_model.removeRows(0, tree_model.rowCount())

        self.assignment_data = hf.get_assignment_data()

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

        self.creation_tree.addTopLevelItems(top_level_items)
        self.creation_tree.expandAll()

    def show_creation_shot_sequence_widgets(self):
        tree_model = self.creation_tree.model()
        tree_model.removeRows(0, tree_model.rowCount())

        self.assignment_data = hf.get_assignment_data()

        sequences_path = self.main_folder_path / "sequences"
        sequences = [x for x in sequences_path.iterdir() if x.is_dir()]

        current_sequence = self.create_shot_dropdown.currentText()
        self.create_shot_dropdown.clear()
        self.create_shot_dropdown.addItems([x.name for x in sequences])
        self.create_shot_dropdown.setCurrentText(current_sequence)

        top_level_items = []

        for sequence in sequences:
            sequence_item = QtWidgets.QTreeWidgetItem()
            sequence_item.setText(0, sequence.name)

            top_level_items.append(sequence_item)

            shots = [x for x in sequence.iterdir() if x.is_dir()]

            for shot in shots:
                shot_item = QtWidgets.QTreeWidgetItem()
                shot_item.setText(0, shot.name)
                sequence_item.addChild(shot_item)


        self.creation_tree.addTopLevelItems(top_level_items)
        self.creation_tree.expandAll()

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
            hf.create_asset_folders(self.main_folder_path, asset_type, asset_name)
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
        self.show_creation_asset_widgets()

    def create_sequence(self):
        sequence_name = self.create_sequence_le.text()
        sequence_path = self.main_folder_path / "sequences" / sequence_name

        if not sequence_name:
            QtWidgets.QMessageBox.warning(
                None, 
                "File Error", 
                f"Please input a name for the asset."
            )
            return

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
        self.show_creation_shot_sequence_widgets()

    def create_shot(self):
        sequence_name = self.create_shot_dropdown.currentText()
        shot_name = self.create_shot_le.text()
        shot_path = self.main_folder_path / "sequences" / sequence_name / shot_name

        if not sequence_name:
            QtWidgets.QMessageBox.warning(
                None, 
                "File Error", 
                f"Make sure a sequence exists first."
            )
            return

        if not shot_name:
            QtWidgets.QMessageBox.warning(
                None, 
                "File Error", 
                f"Please input a name for the shot."
            )
            return

        try:
            hf.create_shot_folders(shot_path)
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
        self.show_creation_shot_sequence_widgets()
