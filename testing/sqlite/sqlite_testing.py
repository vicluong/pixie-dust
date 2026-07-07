import sqlite3

create_sql_statements = [ 
    """
    CREATE TABLE IF NOT EXISTS Projects (
        id INTEGER PRIMARY KEY, 
        name TEXT NOT NULL,
        status TEXT NOT NULL,
        start_date TEXT NOT NULL, 
        end_date TEXT NOT NULL,
        description TEXT,
        image TEXT
    );
    """,

    """
    CREATE TABLE IF NOT EXISTS Sequences (
        id INTEGER PRIMARY KEY, 
        name TEXT NOT NULL, 
        project_id INT NOT NULL, 
        description TEXT,
        FOREIGN KEY (project_id) REFERENCES projects (id)
            ON DELETE CASCADE 
            ON UPDATE CASCADE
    );
    """,

    """
    CREATE TABLE IF NOT EXISTS Shots (
        id INTEGER PRIMARY KEY, 
        name TEXT NOT NULL, 
        sequence_id INT NOT NULL, 
        description TEXT,
        image TEXT,
        FOREIGN KEY (sequence_id) REFERENCES sequences (id)
            ON DELETE CASCADE 
            ON UPDATE CASCADE
    );
    """,

    """
    CREATE TABLE IF NOT EXISTS Assets (
        id INTEGER PRIMARY KEY, 
        name TEXT NOT NULL, 
        project_id INT NOT NULL, 
        description TEXT,
        asset_type TEXT NOT NULL,
        image TEXT,
        FOREIGN KEY (project_id) REFERENCES projects (id)
            ON DELETE CASCADE 
            ON UPDATE CASCADE
    );
    """,

    """
    CREATE TABLE IF NOT EXISTS Entities (
        id INTEGER PRIMARY KEY, 
        entity_type TEXT NOT NULL, 
        entity_id INT NOT NULL
    );
    """,

    """
    CREATE TABLE IF NOT EXISTS Tasks (
        id INTEGER PRIMARY KEY, 
        name TEXT NOT NULL, 
        priority INT, 
        project_id INT NOT NULL, 
        entity_id INT NOT NULL,
        status_id INT NOT NULL, 
        start_date TEXT NOT NULL, 
        end_date TEXT NOT NULL, 
        latest_publish TEXT,
        FOREIGN KEY (project_id) REFERENCES projects (id)
            ON DELETE CASCADE 
            ON UPDATE CASCADE
        FOREIGN KEY (entity_id) REFERENCES entities (id)
            ON DELETE CASCADE 
            ON UPDATE CASCADE
    );
    """
]

insert_sql_statements = [ 
    """
    INSERT INTO Projects
    VALUES
    ('1', 's126', 'in-progress', datetime('now'), datetime('now','+5 day','localtime'), 'Project of 2026', 'image.png');
    """,
    """
    INSERT INTO Sequences
    VALUES
    ('1', 'seq0100', '1', 'First sequence');
    """,
    """
    INSERT INTO Shots
    VALUES
    ('1', 'shot0010', '1', 'First shot', 'shot.png'),
    ('2', 'shot0020', '1', 'Second shot', 'shot2.png');
    """,
    """
    INSERT INTO Assets
    VALUES
    ('1', 'asset01', '1', 'First asset', 'character', 'asset.png'),
    ('2', 'asset02', '1', 'Second asset', 'prop', 'asset2.png');
    """
]

# create a database connection
try:
    with sqlite3.connect('my.db') as conn:
        cursor = conn.cursor()

        for statement in create_sql_statements:
            cursor.execute(statement)

        for statement in insert_sql_statements:
            cursor.execute(statement)

        conn.commit()

        print("Tables created successfully.")
except sqlite3.OperationalError as e:
    print("Failed to create tables:", e)
