"""
tests/test_habit.py
-------------------
I write all the unit tests for the Habit class here.

What is a unit test?
  A unit test is a small automatic check that verifies a specific piece of
  code works correctly. Instead of testing the whole app manually, I write
  short functions that test ONE specific behaviour at a time.

I use Python's built-in 'unittest' framework — no extra installation needed!

To run these tests, I open a terminal in the project folder and type:
    python -m pytest tests/
  or:
    python -m unittest discover tests/
"""

# I import the unittest module — it's built into Python, no installation needed
import unittest

# I import the datetime module to create test timestamps
from datetime import datetime, timedelta, date

# I go up one directory level so Python can find my project files
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# I import the Habit class that I want to test
from habit import Habit


# =========================================================================
# I create a test class that groups all tests for the Habit class together.
# Every test class must inherit from unittest.TestCase.
# =========================================================================
class TestHabitClass(unittest.TestCase):
    """
    I test all the methods of the Habit class.
    Each method starting with 'test_' is run automatically by the test runner.
    """

    # ------------------------------------------------------------------
    # setUp runs before EVERY single test method below.
    # I use it to create fresh Habit objects so each test starts clean.
    # ------------------------------------------------------------------
    def setUp(self):
        """
        I set up a fresh environment before each test.
        I create two simple habit objects — one daily, one weekly — to use in tests.
        """

        # I create a simple daily habit with no check-offs yet
        self.daily_habit = Habit(
            name="Test Daily Habit",
            description="A habit for testing",
            periodicity="daily",
            creation_date="2024-01-01 08:00:00",
            checkoffs=[]
        )

        # I create a weekly habit for testing weekly streak logic
        self.weekly_habit = Habit(
            name="Test Weekly Habit",
            description="A weekly habit for testing",
            periodicity="weekly",
            creation_date="2024-01-01 08:00:00",
            checkoffs=[]
        )

    # ------------------------------------------------------------------
    # Test 1: Make sure I can create a Habit object correctly
    # ------------------------------------------------------------------
    def test_habit_creation(self):
        """
        I verify that creating a Habit sets all its attributes correctly.
        This is the most basic test — if the object isn't created right,
        nothing else will work.
        """

        # I check that the name was stored correctly
        self.assertEqual(self.daily_habit.name, "Test Daily Habit")

        # I check that the description is correct
        self.assertEqual(self.daily_habit.description, "A habit for testing")

        # I check that the periodicity is "daily"
        self.assertEqual(self.daily_habit.periodicity, "daily")

        # I check that the checkoff list starts empty
        self.assertEqual(self.daily_habit.checkoffs, [])

    # ------------------------------------------------------------------
    # Test 2: Make sure an invalid periodicity raises an error
    # ------------------------------------------------------------------
    def test_invalid_periodicity_raises_error(self):
        """
        I verify that trying to create a Habit with a bad periodicity
        (e.g. "monthly" or "hourly") raises a ValueError.
        """

        # I use assertRaises to expect a ValueError to be raised
        with self.assertRaises(ValueError):
            # I try to create a habit with an invalid periodicity
            bad_habit = Habit(
                name="Bad Habit",
                description="This should fail",
                periodicity="monthly"   # Invalid! Only "daily" or "weekly" allowed
            )

    # ------------------------------------------------------------------
    # Test 3: Test that check-off works correctly
    # ------------------------------------------------------------------
    def test_checkoff_adds_timestamp(self):
        """
        I verify that calling checkoff() adds exactly one timestamp to the
        checkoffs list of the habit.
        """

        # I start with zero check-offs
        self.assertEqual(len(self.daily_habit.checkoffs), 0)

        # I check off the habit
        self.daily_habit.checkoff("2024-01-15 09:00:00")

        # I verify that exactly 1 check-off was added
        self.assertEqual(len(self.daily_habit.checkoffs), 1)

        # I verify that the correct timestamp was stored
        self.assertEqual(self.daily_habit.checkoffs[0], "2024-01-15 09:00:00")

    # ------------------------------------------------------------------
    # Test 4: Test that multiple check-offs on the same day count as ONE period
    # ------------------------------------------------------------------
    def test_multiple_checkoffs_same_day_counts_as_one_period(self):
        """
        I verify that if the user checks off a habit multiple times on the
        SAME day, it only counts as ONE completed period (not multiple).
        """

        # I add two check-offs on the same day (different times)
        self.daily_habit.checkoff("2024-01-15 08:00:00")
        self.daily_habit.checkoff("2024-01-15 14:00:00")  # Same day!

        # I get the list of completed periods
        completed = self.daily_habit.get_completed_periods()

        # I expect only ONE period (one day), not two
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0], "2024-01-15")

    # ------------------------------------------------------------------
    # Test 5: Test daily streak of 3 consecutive days
    # ------------------------------------------------------------------
    def test_daily_streak_three_consecutive_days(self):
        """
        I verify that doing a daily habit 3 days in a row gives a streak of 3.
        """

        # I add check-offs for three consecutive days
        self.daily_habit.checkoff("2024-01-13 09:00:00")
        self.daily_habit.checkoff("2024-01-14 09:00:00")
        self.daily_habit.checkoff("2024-01-15 09:00:00")

        # I expect the current streak to be 3
        self.assertEqual(self.daily_habit.get_current_streak(), 3)

    # ------------------------------------------------------------------
    # Test 6: Test that a gap in daily check-offs breaks the streak
    # ------------------------------------------------------------------
    def test_daily_streak_broken_by_gap(self):
        """
        I verify that missing one day breaks the current streak.
        The current streak should restart from the most recent consecutive run.
        """

        # I check off Jan 13 and Jan 14, then skip Jan 15, then do Jan 16
        self.daily_habit.checkoff("2024-01-13 09:00:00")
        self.daily_habit.checkoff("2024-01-14 09:00:00")
        # Jan 15 is MISSING — streak breaks here!
        self.daily_habit.checkoff("2024-01-16 09:00:00")

        # I expect the current streak to be 1 (only Jan 16 is in the current run)
        self.assertEqual(self.daily_habit.get_current_streak(), 1)

    # ------------------------------------------------------------------
    # Test 7: Test that longest streak is tracked correctly
    # ------------------------------------------------------------------
    def test_longest_streak_after_break(self):
        """
        I verify that after breaking a streak, the longest-ever streak
        is still remembered correctly.
        """

        # I build a 5-day streak, then break it, then start a 2-day streak
        self.daily_habit.checkoff("2024-01-01 09:00:00")  # Day 1
        self.daily_habit.checkoff("2024-01-02 09:00:00")  # Day 2
        self.daily_habit.checkoff("2024-01-03 09:00:00")  # Day 3
        self.daily_habit.checkoff("2024-01-04 09:00:00")  # Day 4
        self.daily_habit.checkoff("2024-01-05 09:00:00")  # Day 5 — max streak = 5

        # I skip Jan 6 — streak breaks!

        self.daily_habit.checkoff("2024-01-07 09:00:00")  # New streak starts (Day 1)
        self.daily_habit.checkoff("2024-01-08 09:00:00")  # Day 2 of new streak

        # I check the current streak (should be 2)
        self.assertEqual(self.daily_habit.get_current_streak(), 2)

        # I check the LONGEST streak ever (should still be 5)
        self.assertEqual(self.daily_habit.get_longest_streak(), 5)

    # ------------------------------------------------------------------
    # Test 8: Test streak when there are zero check-offs
    # ------------------------------------------------------------------
    def test_zero_checkoffs_gives_zero_streak(self):
        """
        I verify that a habit with no check-offs has a streak of 0.
        """

        # I haven't checked off this habit at all
        self.assertEqual(self.daily_habit.get_current_streak(), 0)
        self.assertEqual(self.daily_habit.get_longest_streak(), 0)

    # ------------------------------------------------------------------
    # Test 9: Test WEEKLY habit streak
    # ------------------------------------------------------------------
    def test_weekly_streak_two_consecutive_weeks(self):
        """
        I verify that completing a weekly habit two weeks in a row gives a streak of 2.
        Week 1 = ISO week 2024-W01, Week 2 = ISO week 2024-W02
        """

        # I check off in week 1 (Jan 1-7) and week 2 (Jan 8-14)
        # I use Monday Jan 1 for week 1, and Monday Jan 8 for week 2
        self.weekly_habit.checkoff("2024-01-01 10:00:00")  # Week 1
        self.weekly_habit.checkoff("2024-01-08 10:00:00")  # Week 2 (next week)

        # I expect a streak of 2 weeks
        self.assertEqual(self.weekly_habit.get_current_streak(), 2)

    # ------------------------------------------------------------------
    # Test 10: Test to_dict() and from_dict() roundtrip
    # ------------------------------------------------------------------
    def test_to_dict_and_from_dict_roundtrip(self):
        """
        I verify that converting a Habit to a dict and back again gives
        the exact same Habit with all the same data.
        This is important for saving and loading habits from the database.
        """

        # I add a check-off to the original habit
        self.daily_habit.checkoff("2024-01-15 09:00:00")

        # I convert the habit to a dictionary
        habit_dict = self.daily_habit.to_dict()

        # I recreate the habit from the dictionary
        recreated_habit = Habit.from_dict(habit_dict)

        # I check that all the fields match exactly
        self.assertEqual(recreated_habit.name,        self.daily_habit.name)
        self.assertEqual(recreated_habit.description, self.daily_habit.description)
        self.assertEqual(recreated_habit.periodicity, self.daily_habit.periodicity)
        self.assertEqual(recreated_habit.checkoffs,   self.daily_habit.checkoffs)


# =========================================================================
# I tell Python to run all the tests when this file is executed directly
# =========================================================================
if __name__ == "__main__":
    # I run all the tests and show a detailed report
    unittest.main(verbosity=2)
