"""
db.py

I handle all communication between the app and the database.
I use SQLite, which is a simple file-based database built into Python.
No extra software is needed.

The database file is called habits.db and it sits in the same folder
as the rest of the project.
"""

# I import sqlite3 to talk to the database
import sqlite3

# I import json so I can save the list of check-off times as text
import json

# I import the Habit class so I can create Habit objects from database rows
from habit import Habit


def setup_database():
    """
    I create the two database tables if they do not already exist.
    This runs every time the app starts, but it only creates tables
    if they are missing, so existing data is never deleted.

    Tables created:
        habits   : stores one row per habit
        checkoffs: stores one row per completion record
    """

    # I open a connection to the database file
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    # I create the habits table to store each habit's basic details
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT UNIQUE NOT NULL,
            description   TEXT,
            periodicity   TEXT,
            creation_date TEXT
        )
    """)

    # I create the checkoffs table to store each time a habit was completed
    # habit_name links back to the habits table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkoffs (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_name TEXT NOT NULL,
            timestamp  TEXT NOT NULL,
            FOREIGN KEY (habit_name) REFERENCES habits(name)
        )
    """)

    # I save the changes and close the connection
    conn.commit()
    conn.close()


def save_habit(habit):
    """
    I save a habit to the database.
    If the habit already exists, I update it.
    If it is new, I add it.
    I also save all its check-off records.

    Args:
        habit (Habit): the Habit object to save.
    """

    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    # I insert the habit or replace it if it already exists
    cursor.execute("""
        INSERT OR REPLACE INTO habits (name, description, periodicity, creation_date)
        VALUES (?, ?, ?, ?)
    """, (habit.name, habit.description, habit.periodicity, habit.creation_date))

    # I remove old check-off records for this habit before saving the new ones
    cursor.execute("DELETE FROM checkoffs WHERE habit_name = ?", (habit.name,))

    # I save each check-off timestamp as a separate row in the checkoffs table
    for timestamp in habit.checkoffs:
        cursor.execute(
            "INSERT INTO checkoffs (habit_name, timestamp) VALUES (?, ?)",
            (habit.name, timestamp)
        )

    conn.commit()
    conn.close()


def load_all_habits():
    """
    I load all habits from the database and return them as a list of Habit objects.

    Returns:
        List[Habit]: a list of all habits with their check-off records included.
    """

    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    # I get all rows from the habits table
    cursor.execute("SELECT name, description, periodicity, creation_date FROM habits")
    rows = cursor.fetchall()

    habits = []
    for row in rows:
        name, description, periodicity, creation_date = row

        # I get all check-off timestamps for this habit
        cursor.execute(
            "SELECT timestamp FROM checkoffs WHERE habit_name = ? ORDER BY timestamp",
            (name,)
        )
        checkoff_rows = cursor.fetchall()
        # I pull the timestamp string out of each row tuple
        checkoffs = [r[0] for r in checkoff_rows]

        # I create a Habit object with all the loaded data
        habit = Habit(
            name=name,
            description=description,
            periodicity=periodicity,
            creation_date=creation_date,
            checkoffs=checkoffs
        )
        habits.append(habit)

    conn.close()
    return habits


def delete_habit(habit_name):
    """
    I remove a habit and all its check-off records from the database.

    Args:
        habit_name (str): the name of the habit to delete.
    """

    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    # I delete the check-off records first because they link to the habit
    cursor.execute("DELETE FROM checkoffs WHERE habit_name = ?", (habit_name,))

    # I then delete the habit itself
    cursor.execute("DELETE FROM habits WHERE name = ?", (habit_name,))

    conn.commit()
    conn.close()


def habit_exists(habit_name):
    """
    I check whether a habit with a given name already exists in the database.

    Args:
        habit_name (str): the name to look up.

    Returns:
        bool: True if the habit exists, False if it does not.
    """

    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM habits WHERE name = ?", (habit_name,))
    result = cursor.fetchone()

    conn.close()

    # I return True if a row was found, False if not
    return result is not None
