import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime

from env_vars import CONFIG_PATH

def _load_config():
    try:
        with open(str(CONFIG_PATH), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")
    except Exception as e:
        raise RuntimeError(f"Failed to read config file {CONFIG_PATH}: {e}")

@contextmanager
def _get_connection():
    """Helper context manager to easily open/close connections and handle commits."""
    config = _load_config()
    db_path = config.get("database_path", "database.db")  # Fallback if key differs
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Returns rows as dictionary-like objects
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def _is_valid_name(cursor, name, table):
    cursor.execute(f"SELECT name FROM {table}")
    names = [dict(row)["name"] for row in cursor.fetchall()]
    if name in names:
        return False
    else:
        return True

def get_data_from_table(table, id=None, name=None):
    if id and name:
        print("Input either id or name - not both!")

    if id is not None:
        query = f"SELECT * FROM {table} WHERE id = ?"
        param = id
    elif name is not None:
        query = f"SELECT * FROM {table} WHERE name = ?"
        param = name
    else:
        return None

    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (param,))
        row = cursor.fetchone()
        return dict(row) if row else None

def add_project_to_database(name, status=None, start_date=None, end_date=None, description=None, image=None):
    if status == None:
        status = "in-progress"
    if start_date == None:
        now = datetime.now() 
        start_date = now.strftime("%m/%d/%Y, %H:%M:%S")

    with _get_connection() as conn:
        cursor = conn.cursor()
        if _is_valid_name(cursor, name, "Projects"):
            cursor.execute(
                """INSERT INTO Projects (name, status, start_date, end_date, description, image)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (name, status, start_date, end_date, description, image)
            )
            return cursor.lastrowid

def add_sequence_to_database(name, project_id, description=None):
    with _get_connection() as conn:
        cursor = conn.cursor()
        if _is_valid_name(cursor, name, "Sequences"):
            cursor.execute(
                "INSERT INTO Sequences (name, project_id, description) VALUES (?, ?, ?)",
                (name, project_id, description)
            )
            return cursor.lastrowid

def add_shot_to_database(name, sequence_id, description=None, image=None):
    with _get_connection() as conn:
        cursor = conn.cursor()
        if _is_valid_name(cursor, name, "Shots"):
            cursor.execute(
                "INSERT INTO Shots (name, sequence_id, description, image) VALUES (?, ?, ?, ?)",
                (name, sequence_id, description, image)
            )
            return cursor.lastrowid

def add_asset_to_database(name, project_id, asset_type, description=None, image=None):
    with _get_connection() as conn:
        cursor = conn.cursor()
        if _is_valid_name(cursor, name, "Assets"):
            cursor.execute(
                """INSERT INTO Assets (name, project_id, asset_type, description, image)
                VALUES (?, ?, ?, ?, ?)""",
                (name, project_id, asset_type, description, image)
            )
            return cursor.lastrowid

def add_entity_to_database(entity_type, entity_id):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Entities (entity_type, entity_id) VALUES (?, ?)",
            (entity_type, entity_id)
        )
        return cursor.lastrowid

def add_task_to_database(name, user_id, entity_id, status_id, start_date, end_date, priority=None, latest_publish=None):
    with _get_connection() as conn:
        cursor = conn.cursor()
        if _is_valid_name(cursor, name, "Tasks"):
            cursor.execute(
                """INSERT INTO Tasks (name, user_id, entity_id, status_id, start_date, end_date, priority, latest_publish)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (name, user_id, entity_id, status_id, start_date, end_date, priority, latest_publish)
            )
            return cursor.lastrowid

def add_user_to_database(name, email, image, department):
    with _get_connection() as conn:
        cursor = conn.cursor()
        if _is_valid_name(cursor, name, "Users"):
            cursor.execute(
                "INSERT INTO Users (name, email, image, department) VALUES (?, ?, ?, ?)",
                (name, email, image, department)
            )
            return cursor.lastrowid

def add_wip_file_to_database(name, task_id, creation_date, version, path, thumbnail=None):
    with _get_connection() as conn:
        cursor = conn.cursor()
        if _is_valid_name(cursor, name, "WipFiles"):
            cursor.execute(
                """INSERT INTO WipFiles (name, task_id, creation_date, version, path, thumbnail)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (name, task_id, creation_date, version, path, thumbnail)
            )
            return cursor.lastrowid

def add_published_file_to_database(name, task_id, creation_date, version, path, thumbnail=None):
    with _get_connection() as conn:
        cursor = conn.cursor()
        if _is_valid_name(cursor, name, "PublishedFiles"):
            cursor.execute(
                """INSERT INTO PublishedFiles (name, task_id, creation_date, version, path, thumbnail)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (name, task_id, creation_date, version, path, thumbnail)
            )
            return cursor.lastrowid

def add_reviewable_to_database(name, task_id, creation_date, user_id, path):
    with _get_connection() as conn:
        cursor = conn.cursor()
        if _is_valid_name(cursor, name, "Reviewables"):
            cursor.execute(
                """INSERT INTO Reviewables (name, task_id, creation_date, user_id, path)
                VALUES (?, ?, ?, ?, ?)""",
                (name, task_id, creation_date, user_id, path)
            )
            return cursor.lastrowid

def add_note_to_database(name, description, reviewable_id):
    with _get_connection() as conn:
        cursor = conn.cursor()
        if _is_valid_name(cursor, name, "Notes"):
            cursor.execute(
                "INSERT INTO Notes (name, description, reviewable_id) VALUES (?, ?, ?)",
                (name, description, reviewable_id)
            )
            return cursor.lastrowid
