# My Habit Tracker — DLBDSOOFPP01 Portfolio Project
## IU International University of Applied Sciences

> **Student project for:** *Object Oriented and Functional Programming with Python (DLBDSOOFPP01)*

---

## What is this?

This is a **Python-based Habit Tracking App** — a command-line program that helps you:
- ✅ Create and manage habits (daily or weekly)
- 🔁 Check off habits to record when you complete them
- 📊 Analyse your habit streaks and progress
- 💾 Save everything to a local database so nothing is lost

---

## Project File Structure

```
OOFPP_Habits_Project/
│
├── main.py          ← I run this file to start the whole app
├── habit.py         ← I define the Habit class here (OOP)
├── analytics.py     ← I put all analytics functions here (Functional Programming)
├── db.py            ← I handle all database saving and loading here
├── seed_data.py     ← I load 5 pre-defined habits with 4 weeks of example data
├── requirements.txt ← I list all the Python packages needed
│
└── tests/
    ├── __init__.py          ← Tells Python this folder is a package
    ├── test_habit.py        ← I test the Habit class (10 tests)
    └── test_analytics.py    ← I test the analytics module (10 tests)
```

---

## Requirements

- **Python 3.7 or later** (I recommend Python 3.9+)
- **pytest** (for running the unit tests — easily installed below)
- No other external libraries are needed! I use only Python's built-in modules:
  - `sqlite3` — for saving habit data to a local database
  - `datetime` — for working with dates and times
  - `os` — for clearing the terminal screen
  - `unittest` — for writing unit tests

---

## How to Install and Run

### Step 1 — Make sure Python is installed
Open a terminal or Command Prompt and type:
```bash
python --version
```
You should see something like `Python 3.12.0`. If you don't have Python,
download it from [python.org](https://www.python.org/downloads/).

---

### Step 2 — Navigate to the project folder
Open a terminal (PowerShell on Windows, Terminal on Mac/Linux) and go into the project folder:
```bash
cd path\to\OOFPP_Habits_Project
```
*(Replace `path\to\` with where you saved the project.)*

---

### Step 3 — Install the only extra dependency (pytest)
```bash
pip install pytest
```

---

### Step 4 — Run the app!
```bash
python main.py
```
The app will:
1. Create the database file (`habits.db`) automatically
2. Load 5 pre-defined habits with 4 weeks of example data
3. Show you the main interactive menu

---

## How to Use the App

When you run `python main.py`, you see this menu:

```
=======================================================
      🌟  MY HABIT TRACKER  🌟
      Friday, 01 January 2024  |  09:00
=======================================================
  1. 📋  View all my habits
  2. ➕  Add a new habit
  3. ✅  Check off a habit (mark as done today)
  4. 🗑️  Delete a habit
  5. 📊  Analyse my habits
  6. 🚪  Exit
-------------------------------------------------------
```

Just **type a number** and press **Enter** to choose an option!

### Adding a New Habit
1. Choose option `2`
2. Type the habit name (e.g. `Drink Water`)
3. Type a short description
4. Choose `1` for Daily or `2` for Weekly
5. Your habit is saved!

### Checking Off a Habit
1. Choose option `3`
2. You see a numbered list of your habits
3. Type the number of the habit you just completed
4. The app records the current date/time and updates your streak

### Analysing Your Habits
1. Choose option `5`
2. An analysis sub-menu appears with 5 options:
   - View all daily habits
   - View all weekly habits
   - See the longest streak across ALL habits
   - See the longest streak for ONE specific habit
   - See which habits you're struggling with

---

## The 5 Pre-Defined Habits (Test Fixtures)

When you run the app for the first time, these 5 habits are added automatically
with **4 weeks of example check-off data** (Jan 1 – Jan 28, 2024):

| # | Habit Name      | Type    | Description                                   |
|---|-----------------|---------|-----------------------------------------------|
| 1 | Drink Water     | Daily   | Drink at least 2 litres of water every day    |
| 2 | Exercise        | Daily   | Do at least 30 minutes of exercise every day  |
| 3 | Read a Book     | Daily   | Read at least 20 pages of a book every day    |
| 4 | Weekly Review   | Weekly  | Review the week's achievements and plan ahead |
| 5 | Clean the House | Weekly  | Thoroughly clean every room of the house      |

---

## How to Run the Unit Tests

The project includes **20 unit tests** that automatically verify the core logic is correct.

To run all tests, open a terminal in the project folder and type:
```bash
python -m pytest tests/ -v
```

You should see output like:
```
tests/test_analytics.py::TestAnalytics::test_get_all_habits_returns_all PASSED
tests/test_analytics.py::TestAnalytics::test_get_habits_by_periodicity_daily PASSED
... (20 tests total)
======================== 20 passed in 0.17s ========================
```

All 20 tests should pass ✅

---

## Design Decisions

### Why SQLite?
I chose SQLite (via Python's built-in `sqlite3` module) because:
- It requires **zero installation** — it's part of Python already
- Data is stored in a **single file** (`habits.db`) which is easy to understand
- It's a real relational database, which is more professional than a JSON file
- It teaches important concepts (tables, rows, foreign keys)

### Object-Oriented Programming (OOP)
The `Habit` class in `habit.py` is the heart of the OOP design:
- Each habit is its own **object** with its own data (name, description, checkoffs)
- The class has **methods** that operate on that data (`checkoff()`, `get_current_streak()`, etc.)
- I use `to_dict()` / `from_dict()` for easy serialisation

### Functional Programming
The `analytics.py` module is written in a **functional style**:
- Every function takes data **in** and returns a result **out** — no side effects
- I use `filter()`, `map()`, `max()`, and generator expressions
- Functions never modify the habit objects — they just read and compute

---

## GitHub Repository
https://github.com/YOUR_USERNAME/oofpp_habits_project

*(Replace YOUR_USERNAME with your actual GitHub username after pushing)*

---

*Built with ❤️ for the IU DLBDSOOFPP01 portfolio assignment.*
