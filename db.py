"""
db.py
-----
I handle all saving and loading of habit data here.
I use Python's built-in SQLite database (sqlite3) — a simple file-based database
that requires NO installation. The database is stored as a single file: habits.db

Think of this file as the "memory" of the app — without it, all habits would
be forgotten every time the user closes the program.
"""

# I import sqlite3 — Python comes with this built-in, no pip install needed!
import sqlite3

# I import os so I can build file paths that work on any operating system
import os

# I import the Habit class from my habit.py file so I can work with Habit objects
from habit import Habit


# I define the name of the database file here in one place.
# If I ever want to rename or move the file, I only change it in ONE spot.
DB_FILE = "habits.db"


def get_connection(db_path: str = DB_FILE):
    """
    I open a connection to the SQLite database file.
    If the file does not exist yet, SQLite creates it automatically for me.

    Args:
        db_path (str): The path to the .db file. Default is "habits.db".

    Returns:
        sqlite3.Connection: An open connection to the database.
    """

    # I connect to (or create) the SQLite database file
    conn = sqlite3.connect(db_path)
    return conn


def setup_database(db_path: str = DB_FILE):
    """
    I create the database tables if they don't already exist.
    I must call this function ONCE when the app starts for the first time.

    My database has 2 tables:
      1. habits       — stores the name, description, periodicity, creation_date
      2. checkoffs    — stores each time a habit was checked off (completed)

    The two tables are linked: each checkoff row knows which habit it belongs to
    (this is called a FOREIGN KEY relationship).

    Args:
        db_path (str): The path to the .db file.
    """

    # I open a connection to the database
    conn = get_connection(db_path)

    # I get a "cursor" — think of it as a pen I use to write SQL commands
    cursor = conn.cursor()

    # I create the "habits" table if it does not exist yet.
    # Each habit has: an auto-generated ID, a name, description, periodicity, and creation_date.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL UNIQUE,
            description   TEXT,
            periodicity   TEXT    NOT NULL,
            creation_date TEXT    NOT NULL
        )
    """)

    # I create the "checkoffs" table if it does not exist yet.
    # Each row records ONE check-off event: which habit was checked and when.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkoffs (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_name TEXT    NOT NULL,
            timestamp  TEXT    NOT NULL,
            FOREIGN KEY (habit_name) REFERENCES habits (name)
        )
    """)

    # I save (commit) the changes to the database file
    conn.commit()

    # I close the connection — good practice to always close when done
    conn.close()


def save_habit(habit: Habit, db_path: str = DB_FILE):
    """
    I save ONE habit to the database.
    If a habit with this name already exists, I update it instead of adding a duplicate.

    Args:
        habit (Habit): The Habit object I want to save.
        db_path (str): The path to the .db file.
    """

    # I open the database
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # I use "INSERT OR REPLACE" — this inserts a new row, OR replaces the existing one
    # if a habit with the same name is already in the database
    cursor.execute("""
        INSERT OR REPLACE INTO habits (name, description, periodicity, creation_date)
        VALUES (?, ?, ?, ?)
    """, (habit.name, habit.description, habit.periodicity, habit.creation_date))

    # I now save all the check-offs for this habit.
    # First, I delete any old check-offs so I don't create duplicates
    cursor.execute("DELETE FROM checkoffs WHERE habit_name = ?", (habit.name,))

    # Then, I insert ALL the check-offs fresh from the Habit object
    for ts in habit.checkoffs:
        cursor.execute("""
            INSERT INTO checkoffs (habit_name, timestamp)
            VALUES (?, ?)
        """, (habit.name, ts))

    # I save all my changes to the database file
    conn.commit()

    # I close the connection
    conn.close()


def load_all_habits(db_path: str = DB_FILE) -> list:
    """
    I load ALL habits from the database and return them as a list of Habit objects.

    Returns:
        list: A list of Habit objects loaded from the database.
    """

    # I open the database
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # I fetch all rows from the habits table
    cursor.execute("SELECT name, description, periodicity, creation_date FROM habits")
    habit_rows = cursor.fetchall()  # I get all results at once

    # I build a list of Habit objects from the database rows
    habits = []
    for row in habit_rows:
        name, description, periodicity, creation_date = row

        # I fetch all check-offs that belong to this specific habit
        cursor.execute(
            "SELECT timestamp FROM checkoffs WHERE habit_name = ? ORDER BY timestamp",
            (name,)
        )
        checkoff_rows = cursor.fetchall()

        # I extract just the timestamp string from each row (each row is a tuple like ("2024-01-01 09:00:00",))
        checkoffs = [r[0] for r in checkoff_rows]

        # I create a Habit object and add it to my list
        habit = Habit(
            name=name,
            description=description,
            periodicity=periodicity,
            creation_date=creation_date,
            checkoffs=checkoffs,
        )
        habits.append(habit)

    # I close the connection and return the full list
    conn.close()
    return habits


def delete_habit(name: str, db_path: str = DB_FILE):
    """
    I permanently delete a habit (and all its check-offs) from the database.

    Args:
        name (str): The exact name of the habit to delete.
        db_path (str): The path to the .db file.
    """

    # I open the database
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # I delete all check-offs for this habit first (so I don't leave orphaned data behind)
    cursor.execute("DELETE FROM checkoffs WHERE habit_name = ?", (name,))

    # Now I delete the habit itself from the habits table
    cursor.execute("DELETE FROM habits WHERE name = ?", (name,))

    # I save (commit) the deletion to the database file
    conn.commit()

    # I close the connection
    conn.close()


def habit_exists(name: str, db_path: str = DB_FILE) -> bool:
    """
    I check whether a habit with the given name already exists in the database.

    Args:
        name (str): The habit name to look for.
        db_path (str): The path to the .db file.

    Returns:
        bool: True if the habit exists, False if it does not.
    """

    # I open the database
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # I search for a habit with this exact name
    cursor.execute("SELECT 1 FROM habits WHERE name = ?", (name,))

    # fetchone() returns one row if found, or None if not found
    result = cursor.fetchone()

    # I close the connection and return True if I found something, False otherwise
    conn.close()
    return result is not None
