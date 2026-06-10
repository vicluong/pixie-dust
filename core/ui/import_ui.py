import sys

try:
    from PySide6 import QtWidgets, QtCore
except:
    from PySide2 import QtWidgets, QtCore

from dcc_manager.dcc_interface import DCCInterface
from ui.asset_tree_ui import AssetTreeWidget


class ImportDialog(QtWidgets.QDialog):
    dlg_instance = None

    @classmethod
    def show_dialog(cls, dcc_interface: DCCInterface):
        if cls.dlg_instance is None:
            cls.dlg_instance = ImportDialog(dcc_interface)

        cls.dlg_instance.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()
        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    @classmethod
    def _clear_instance(cls):
        cls.dlg_instance = None

    def __init__(self, dcc_interface: DCCInterface):
        super(ImportDialog, self).__init__()

        self.setWindowTitle("Import / Reference")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.destroyed.connect(ImportDialog._clear_instance)

        self.dcc_interface = dcc_interface
        self.main_window = self.dcc_interface.get_main_window()

        size = self.main_window.screen().size()
        screen_w, screen_h = size.width(), size.height()
        self.resize(int(screen_w * 0.25), int(screen_h * 0.3))

        if sys.platform == "darwin":
            self.setWindowFlag(QtCore.Qt.Tool, True)

        self.scene_folder = self.dcc_interface.get_scene_folder()
        self.file_extensions = self.dcc_interface.get_file_extensions()

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.assets_tree = AssetTreeWidget(extra_info=False)

        # self.publish_label = QtWidgets.QLabel("Published Versions")
        # self.publish_label.setAlignment(QtCore.Qt.AlignCenter) 
        self.files_list = QtWidgets.QListWidget()

        self.file_info_le = QtWidgets.QLineEdit()
        self.reference_btn = QtWidgets.QPushButton("Reference")
        self.import_btn = QtWidgets.QPushButton("Import")

    def create_layout(self):
        main_layout = QtWidgets.QHBoxLayout(self)

        assets_layout = QtWidgets.QVBoxLayout()
        assets_layout.addWidget(self.assets_tree)

        extensions_layout = QtWidgets.QVBoxLayout()
        extensions_layout.addWidget(self.files_list)

        import_layout = QtWidgets.QVBoxLayout()
        # import_layout.addStretch()
        import_layout.addWidget(self.file_info_le)
        import_layout.addWidget(self.reference_btn)
        import_layout.addWidget(self.import_btn)

        main_layout.addLayout(assets_layout)
        main_layout.addLayout(extensions_layout)
        main_layout.addLayout(import_layout)

    def create_connections(self):
        self.assets_tree.itemClicked.connect(self.show_latest_publishes)
        self.import_btn.clicked.connect(self.import_file)
        self.reference_btn.clicked.connect(self.reference_file)

    def show_latest_publishes(self, tree_item):
        self.files_list.clear()
        
        parents = 0
        parent = tree_item.parent()

        while parent:
            parents += 1
            parent = parent.parent()

        if parents == 2:
            asset_step_item = self.assets_tree.currentItem()
            asset_step = asset_step_item.text(0)
            asset_name_item = asset_step_item.parent()
            asset_name = asset_name_item.text(0)
            asset_type_item = asset_name_item.parent()
            asset_type = asset_type_item.text(0)

            latest_publishes = self.dcc_interface.get_latest_published_files(asset_name, asset_type, asset_step)
            for latest_publish in latest_publishes:
                latest_publish_info = latest_publish[0].suffix + " - " + latest_publish[1].stem.rsplit("_", 1)[1]
                list_item = QtWidgets.QListWidgetItem(latest_publish_info)
                list_item.setData(QtCore.Qt.UserRole, latest_publish[0])
                self.files_list.addItem(list_item)

    def import_file(self):
        item = self.files_list.currentItem()
        path = item.data(QtCore.Qt.UserRole)
        
        print(f"Importing: {path.name}")

        self.dcc_interface.import_file(path)


    def reference_file(self):
        item = self.files_list.currentItem()
        path = item.data(QtCore.Qt.UserRole)
        
        print(f"Referencing: {path.name}")

        self.dcc_interface.reference_file(path)
