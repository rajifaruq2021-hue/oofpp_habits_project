"""
seed_data.py

I create five example habits and fill them with four weeks of check-off data.
This gives the user some ready-made data to explore when they first open the app.

The five habits are:
    1. Morning Run         (daily)
    2. Read a Book         (daily)
    3. Drink Water         (daily)
    4. Weekly Review       (weekly)
    5. Call Family         (weekly)

All check-off data covers January 2024.
"""

# I import the Habit and db modules I need
from habit import Habit
import db


def load_predefined_habits():
    """
    I create five habits with four weeks of check-off data
    and save them all to the database.

    I skip any habit that already exists in the database
    so existing user data is never overwritten.
    """

    # I define the five predefined habits as a list of tuples
    # Each tuple has: (name, description, periodicity)
    predefined = [
        ("Morning Run",   "Go for a 20-minute run each morning.", "daily"),
        ("Read a Book",   "Read at least 10 pages of a book.",    "daily"),
        ("Drink Water",   "Drink 8 glasses of water each day.",   "daily"),
        ("Weekly Review", "Review goals and plan for next week.", "weekly"),
        ("Call Family",   "Call a family member to check in.",    "weekly"),
    ]

    # I define four weeks of daily dates in January 2024
    # Each date is one day in January
    daily_dates = [
        "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05",
        "2024-01-06", "2024-01-07", "2024-01-08", "2024-01-09", "2024-01-10",
        "2024-01-11", "2024-01-12", "2024-01-13", "2024-01-14", "2024-01-15",
        "2024-01-16", "2024-01-17", "2024-01-18", "2024-01-19", "2024-01-20",
        "2024-01-21", "2024-01-22", "2024-01-23", "2024-01-24", "2024-01-25",
        "2024-01-26", "2024-01-27", "2024-01-28",
    ]

    # I define four weekly check-off dates (one per week in January 2024)
    weekly_dates = [
        "2024-01-01",  # Week 1
        "2024-01-08",  # Week 2
        "2024-01-15",  # Week 3
        "2024-01-22",  # Week 4
    ]

    # I go through each predefined habit
    for name, description, periodicity in predefined:

        # I skip this habit if it already exists in the database
        if db.habit_exists(name):
            print(f"  Habit already exists, skipping: {name}")
            continue

        # I choose daily or weekly dates based on the habit type
        if periodicity == "daily":
            dates = daily_dates
        else:
            dates = weekly_dates

        # I build the list of check-off timestamps
        # I use 08:00:00 as the time for all of them
        checkoffs = [f"{date} 08:00:00" for date in dates]

        # I create the Habit object with all the check-off data
        habit = Habit(
            name=name,
            description=description,
            periodicity=periodicity,
            creation_date="2024-01-01 00:00:00",
            checkoffs=checkoffs
        )

        # I save the habit to the database
        db.save_habit(habit)
        print(f"  Saved habit: {name}")
