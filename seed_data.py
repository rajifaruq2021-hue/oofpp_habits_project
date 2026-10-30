"""
seed_data.py
------------
I create 5 pre-defined "sample" habits here — including example tracking data
for 4 weeks (28 days). The assignment requires this as a "test fixture".

What is a test fixture?
  A test fixture is a set of pre-made, known data that you use for testing.
  Instead of typing in habits and check-offs by hand every time, I load
  this pre-made data automatically. It also makes it easy to test the analytics.

I have 5 habits here:
  1. Drink Water          (daily)
  2. Exercise / Work Out  (daily)
  3. Read a Book          (daily)
  4. Weekly Review        (weekly)
  5. Clean the House      (weekly)
"""

# I import the Habit class from my habit.py file
from habit import Habit

# I import the db module so I can save these habits to the database
import db


def load_predefined_habits(db_path: str = "habits.db"):
    """
    I insert the 5 pre-defined habits (with 4 weeks of example data) into the database.
    I only add a habit if it does NOT already exist — so running this twice won't create duplicates.

    Args:
        db_path (str): The path to the SQLite database file.
    """

    # ------------------------------------------------------------------
    # I define all 5 pre-defined habits here as a list of dictionaries.
    # Each dictionary contains:
    #   - "name"        : the habit name
    #   - "description" : a short description
    #   - "periodicity" : "daily" or "weekly"
    #   - "creation_date": when the habit was started (4 weeks ago)
    #   - "checkoffs"   : a list of timestamps representing 4 weeks of data
    # ------------------------------------------------------------------

    predefined = [

        # ---------------------------------------------------------------
        # Habit 1: Drink Water — DAILY
        # I set this up as if the habit started on 2024-01-01.
        # The user completed it on most days but missed a few (realistic data).
        # ---------------------------------------------------------------
        {
            "name":          "Drink Water",
            "description":   "I drink at least 2 litres of water every day.",
            "periodicity":   "daily",
            "creation_date": "2024-01-01 08:00:00",
            "checkoffs": [
                # Week 1 — I checked off every single day
                "2024-01-01 08:30:00",
                "2024-01-02 09:00:00",
                "2024-01-03 07:45:00",
                "2024-01-04 08:00:00",
                "2024-01-05 10:00:00",
                "2024-01-06 09:30:00",
                "2024-01-07 08:00:00",
                # Week 2 — I checked off every day
                "2024-01-08 08:15:00",
                "2024-01-09 07:30:00",
                "2024-01-10 09:00:00",
                "2024-01-11 08:45:00",
                "2024-01-12 08:00:00",
                "2024-01-13 11:00:00",
                "2024-01-14 08:30:00",
                # Week 3 — I missed Jan 17 (streak broken!)
                "2024-01-15 08:00:00",
                "2024-01-16 09:00:00",
                # Missed Jan 17 — no checkoff!
                "2024-01-18 08:30:00",
                "2024-01-19 09:15:00",
                "2024-01-20 08:00:00",
                "2024-01-21 10:00:00",
                # Week 4 — I was consistent again
                "2024-01-22 08:00:00",
                "2024-01-23 08:30:00",
                "2024-01-24 09:00:00",
                "2024-01-25 08:00:00",
                "2024-01-26 07:45:00",
                "2024-01-27 08:30:00",
                "2024-01-28 09:00:00",
            ],
        },

        # ---------------------------------------------------------------
        # Habit 2: Exercise / Work Out — DAILY
        # I set this up as if the habit started on 2024-01-01.
        # The user exercised on most days but had a few rest days.
        # ---------------------------------------------------------------
        {
            "name":          "Exercise",
            "description":   "I do at least 30 minutes of exercise every day.",
            "periodicity":   "daily",
            "creation_date": "2024-01-01 06:00:00",
            "checkoffs": [
                # Week 1
                "2024-01-01 06:30:00",
                "2024-01-02 06:30:00",
                "2024-01-03 06:30:00",
                # Missed Jan 4 — rest day
                "2024-01-05 06:45:00",
                "2024-01-06 07:00:00",
                "2024-01-07 06:30:00",
                # Week 2
                "2024-01-08 06:30:00",
                "2024-01-09 06:30:00",
                "2024-01-10 06:30:00",
                "2024-01-11 06:30:00",
                "2024-01-12 06:30:00",
                "2024-01-13 07:00:00",
                "2024-01-14 06:30:00",
                # Week 3 — missed 2 days
                "2024-01-15 06:30:00",
                "2024-01-16 06:30:00",
                # Missed Jan 17, 18
                "2024-01-19 06:30:00",
                "2024-01-20 07:00:00",
                "2024-01-21 06:30:00",
                # Week 4
                "2024-01-22 06:30:00",
                "2024-01-23 06:30:00",
                "2024-01-24 06:30:00",
                "2024-01-25 06:30:00",
                "2024-01-26 06:30:00",
                "2024-01-27 07:00:00",
                "2024-01-28 06:30:00",
            ],
        },

        # ---------------------------------------------------------------
        # Habit 3: Read a Book — DAILY
        # The user reads at least 20 pages every day.
        # They were very consistent here — almost no missed days.
        # ---------------------------------------------------------------
        {
            "name":          "Read a Book",
            "description":   "I read at least 20 pages of a book every day.",
            "periodicity":   "daily",
            "creation_date": "2024-01-01 21:00:00",
            "checkoffs": [
                # Week 1 — perfect
                "2024-01-01 21:30:00",
                "2024-01-02 21:00:00",
                "2024-01-03 22:00:00",
                "2024-01-04 21:30:00",
                "2024-01-05 21:00:00",
                "2024-01-06 20:30:00",
                "2024-01-07 21:00:00",
                # Week 2 — perfect
                "2024-01-08 21:00:00",
                "2024-01-09 21:30:00",
                "2024-01-10 22:00:00",
                "2024-01-11 21:00:00",
                "2024-01-12 21:30:00",
                "2024-01-13 21:00:00",
                "2024-01-14 21:00:00",
                # Week 3 — missed only one day
                "2024-01-15 21:00:00",
                "2024-01-16 21:30:00",
                "2024-01-17 21:00:00",
                # Missed Jan 18
                "2024-01-19 21:00:00",
                "2024-01-20 21:30:00",
                "2024-01-21 21:00:00",
                # Week 4 — perfect
                "2024-01-22 21:00:00",
                "2024-01-23 21:30:00",
                "2024-01-24 22:00:00",
                "2024-01-25 21:00:00",
                "2024-01-26 21:30:00",
                "2024-01-27 21:00:00",
                "2024-01-28 21:00:00",
            ],
        },

        # ---------------------------------------------------------------
        # Habit 4: Weekly Review — WEEKLY
        # Every Sunday the user does a weekly review of goals and tasks.
        # This spans 4 weeks (4 Sundays), so 4 check-offs.
        # ---------------------------------------------------------------
        {
            "name":          "Weekly Review",
            "description":   "I review my week: achievements, goals, and plan for next week.",
            "periodicity":   "weekly",
            "creation_date": "2024-01-01 10:00:00",
            "checkoffs": [
                # Sunday of Week 1 (Jan 7 = Sunday)
                "2024-01-07 20:00:00",
                # Sunday of Week 2 (Jan 14 = Sunday)
                "2024-01-14 20:00:00",
                # Sunday of Week 3 (Jan 21 = Sunday)
                "2024-01-21 20:00:00",
                # Sunday of Week 4 (Jan 28 = Sunday)
                "2024-01-28 20:00:00",
            ],
        },

        # ---------------------------------------------------------------
        # Habit 5: Clean the House — WEEKLY
        # Every weekend the user cleans the house.
        # They completed this for 3 out of 4 weeks (missed one week).
        # ---------------------------------------------------------------
        {
            "name":          "Clean the House",
            "description":   "I thoroughly clean my house — every room, every week.",
            "periodicity":   "weekly",
            "creation_date": "2024-01-01 10:00:00",
            "checkoffs": [
                # Week 1 — cleaned on Saturday Jan 6
                "2024-01-06 11:00:00",
                # Week 2 — cleaned on Saturday Jan 13
                "2024-01-13 11:30:00",
                # Week 3 — MISSED this week! No checkoff for week 3.
                # Week 4 — cleaned on Saturday Jan 27
                "2024-01-27 11:00:00",
            ],
        },

    ]

    # ------------------------------------------------------------------
    # I now loop through all 5 habits and save each one to the database.
    # I check first so I don't overwrite existing data if already loaded.
    # ------------------------------------------------------------------
    for data in predefined:
        # I only add this habit if it's not already in the database
        if not db.habit_exists(data["name"], db_path):
            # I create a Habit object from the dictionary data
            habit = Habit(
                name=data["name"],
                description=data["description"],
                periodicity=data["periodicity"],
                creation_date=data["creation_date"],
                checkoffs=data["checkoffs"],
            )
            # I save it to the database
            db.save_habit(habit, db_path)
            print(f"  [+] Pre-defined habit loaded: '{habit.name}'")
        else:
            # I skip it because it already exists
            print(f"  [-] Habit already exists, skipping: '{data['name']}'")
