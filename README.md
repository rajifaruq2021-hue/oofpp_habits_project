# Habit Tracker App
## IU International University of Applied Sciences

Student project for Object Oriented and Functional Programming with Python (DLBDSOOFPP01)


## What is this?

This is a Python Habit Tracking App that runs in the command line. It lets you:
- Create and manage habits (daily or weekly)
- Check off habits when you complete them
- See your habit streaks and progress
- Save everything to a local database so nothing is lost


## Project File Structure

`
OOFPP_Habits_Project/
|
|-- main.py            I run this file to start the whole app
|-- habit.py           I define the Habit class here (OOP)
|-- analytics.py       I put all analytics functions here (Functional Programming)
|-- db.py              I handle all database saving and loading here
|-- seed_data.py       I load 5 pre-defined habits with 4 weeks of example data
|-- requirements.txt   I list all the Python packages needed
|
+-- tests/
    |-- __init__.py          Tells Python this folder is a package
    |-- test_habit.py        I test the Habit class (10 tests)
    +-- test_analytics.py    I test the analytics module (10 tests)
`


## Requirements

- Python 3.7 or later (I recommend Python 3.9+)
- pytest (for running the unit tests)
- No other external libraries are needed. I use only Python built-in modules:
  - sqlite3 for saving habit data to a local database
  - datetime for working with dates and times
  - os for clearing the terminal screen
  - unittest for writing unit tests


## How to Install and Run

### Step 1: Make sure Python is installed
Open a terminal or Command Prompt and type:
`ash
python --version
`
You should see something like Python 3.12.0. If you do not have Python,
download it from https://www.python.org/downloads/

### Step 2: Go into the project folder
Open a terminal (PowerShell on Windows, Terminal on Mac/Linux) and type:
`ash
cd path/to/OOFPP_Habits_Project
`
Replace path/to/ with where you saved the project.

### Step 3: Install pytest
`ash
pip install pytest
`

### Step 4: Run the app
`ash
python main.py
`
The app will:
1. Create the database file (habits.db) automatically
2. Load 5 pre-defined habits with 4 weeks of example data
3. Show you the main menu


## How to Use the App

When you run python main.py, you see this menu:

`
==================================================
      HABIT TRACKER APP
      2024-01-01  09:00
==================================================

What would you like to do?

1. View all habits
2. Add a new habit
3. Check off a habit
4. Delete a habit
5. Analyse habits
6. Exit

Pick an option (1-6):
`

Just type a number and press Enter to choose an option.

### Adding a New Habit
1. Choose option 2
2. Type the habit name (for example Drink Water)
3. Type a short description
4. Choose daily or weekly
5. Your habit is saved

### Checking Off a Habit
1. Choose option 3
2. You see a numbered list of your habits
3. Type the number of the habit you just completed
4. The app records the current date and time and updates your streak

### Looking at Your Habits
1. Choose option 5
2. A sub-menu appears with options:
   - View all daily habits
   - View all weekly habits
   - See the longest streak across all habits
   - See the longest streak for one specific habit


## The 5 Pre-Defined Habits

When you run the app for the first time, these 5 habits are added automatically
with 4 weeks of example check-off data (Jan 1 to Jan 28, 2024):

| No. | Habit Name      | Type    | Description                                  |
|-----|-----------------|---------|----------------------------------------------|
| 1   | Morning Run     | Daily   | Go for a 20-minute run each morning          |
| 2   | Read a Book     | Daily   | Read at least 10 pages of a book             |
| 3   | Drink Water     | Daily   | Drink 8 glasses of water each day            |
| 4   | Weekly Review   | Weekly  | Review goals and plan for next week          |
| 5   | Call Family     | Weekly  | Call a family member to check in             |


## How to Run the Unit Tests

The project has 20 unit tests that check the core logic is correct.

To run all tests, open a terminal in the project folder and type:
`ash
python -m pytest tests/ -v
`

You should see output like:
`
tests/test_analytics.py::TestAnalytics::test_get_all_habits_returns_all_four PASSED
tests/test_analytics.py::TestAnalytics::test_get_daily_habits_returns_two PASSED
... (20 tests total)
======================== 20 passed in 0.09s ========================
`

All 20 tests should pass.


## Design Decisions

### Why SQLite?
I chose SQLite (using Python built-in sqlite3 module) because:
- It needs no installation, it is already part of Python
- Data is stored in a single file (habits.db) which is easy to understand
- It is a real relational database, which is better than a JSON file
- It teaches important ideas like tables, rows, and foreign keys

### Object Oriented Programming (OOP)
The Habit class in habit.py is the main part of the OOP design:
- Each habit is its own object with its own data (name, description, checkoffs)
- The class has methods that work on that data (checkoff, get_current_streak, etc.)
- I use to_dict() and from_dict() to convert habits for saving and loading

### Functional Programming
The analytics.py module is written in a functional style:
- Every function takes data in and returns a result out without changing anything
- I use filter(), map(), max(), and generator expressions
- Functions never change the habit objects, they just read and compute


## GitHub Repository
https://github.com/rajifaruq2021-hue/oofpp_habits_project
