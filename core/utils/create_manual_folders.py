from pathlib import Path


workspace_path = Path("F:\\ALA Projects\\Pixie Dust\\sheeping_beauty\\03_production")

def create_manual_folders(main_folder: Path):
    # Create manual folders where there were previous none with wip and publishes folders.
    # Very rare use
    subdirs = [f for f in main_folder.iterdir() if f.is_dir()]

    for folder in subdirs:
        if folder.is_dir():
            if (any(child.is_dir() for child in folder.glob("wip"))
                and any(child.is_dir() for child in folder.glob("publishes"))):
                manual_path = folder / "manual"
                manual_path.mkdir(exist_ok=True)
            create_manual_folders(folder)

create_manual_folders(workspace_path)
