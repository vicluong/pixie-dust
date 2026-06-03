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
from ui.production_assets_ui import ProductionAssetsTab
from ui.production_shot_tasks_ui import ProductionShotTasksTab


class ProductionTab(QtWidgets.QWidget):
    def __init__(self, dcc_interface: DCCInterface):
        super().__init__()

        self.dcc_interface = dcc_interface
        self.main_workspace_path = ffu.get_main_workspace_path()

        self.assignment_data = ffu.get_assignment_data()
        self.users = ffu.get_users()

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        """Create all widgets for the UI"""
        # Tab 3: Assignment
        self.current_user_dropdown = QtWidgets.QComboBox()
        self.current_user_dropdown.addItems([x for x in self.users])

            # Bottom File Buttons
        self.get_tasks_btn = QtWidgets.QPushButton("Get Tasks")

    def create_layout(self):
        """Create all layouts and add widgets to them"""
        # Tab 3: Production
        production_layout = QtWidgets.QVBoxLayout(self)

        current_user_layout = QtWidgets.QFormLayout()
        current_user_layout.addRow("Current User:", self.current_user_dropdown)
        production_layout.addLayout(current_user_layout)

        production_main_tab = QtWidgets.QTabWidget()
        # production_tasks_tab = QtWidgets.QWidget()
        production_assets_tab = ProductionAssetsTab(self.dcc_interface)
        production_shots_tab = ProductionShotTasksTab(self.dcc_interface)
        # production_main_tab.addTab(production_tasks_tab, "My Tasks")
        production_main_tab.addTab(production_assets_tab, "Assets")
        production_main_tab.addTab(production_shots_tab, "Shots / Sequences")
        production_layout.addWidget(production_main_tab)

        # self.production_tasks_layout = QtWidgets.QHBoxLayout(production_tasks_tab)

    def create_connections(self):
        """Create all connections for the UI"""
        # self.get_tasks_btn.pressed.connect(self.show_tasks_table)
        # self.current_user_dropdown.currentTextChanged.connect(self.show_tasks_table)

    # def show_tasks_table(self):
    #     self.clear_layout(self.production_tasks_layout)

    #     card_data = []

    #     for assignment in self.assignment_data.values():
    #         current_assignee_uid = ffu.get_uid(self.current_user_dropdown.currentText())
    #         if current_assignee_uid in assignment["assignees"]: 
    #             if "asset_name" in assignment and "asset_part" in assignment:
    #                 card_data.append((assignment["asset_name"], assignment["asset_part"]))
    #             elif "task_name" in assignment and "sequence_name" in assignment and "shot_name" in assignment:
    #                 card_data.append((assignment["task_name"], f"{assignment['sequence_name']}, {assignment['shot_name']}"))

    #     card_data.sort()

    #     for card in card_data:
    #         card_widget = Card(card[0], card[1])
    #         card_widget.setMaximumWidth(300)
    #         card_widget.setMaximumHeight(200)
    #         self.production_tasks_layout.addWidget(card_widget)
        
    #     self.production_tasks_layout.addStretch()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()
            child_layout = item.layout()

            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

            elif child_layout is not None:
                self.clear_layout(child_layout)

class Card(QtWidgets.QFrame):
    def __init__(self, title: str, content: str):
        super().__init__()

        self.setObjectName("card")

        layout = QtWidgets.QVBoxLayout(self)

        title_label = QtWidgets.QLabel(title)
        content_label = QtWidgets.QLabel(content)

        layout.addWidget(title_label)
        layout.addWidget(content_label)

        self.setStyleSheet("""
        QFrame#card {
            border-radius: 10px;
            border: 1px solid #ddd;
            padding: 10px;
        }
        QLabel {
            font-size: 30px;
        }
        """)
