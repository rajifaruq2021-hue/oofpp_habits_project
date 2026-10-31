"""
tests/test_habit.py

I test the Habit class to make sure every method works correctly.
I use Python's built-in unittest module to write and run the tests.
"""

import unittest
from datetime import date, timedelta
import sys
import os

# I add the parent folder to the path so Python can find habit.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from habit import Habit


class TestHabit(unittest.TestCase):
    """
    I group all the tests for the Habit class inside this test class.
    Each method that starts with 'test_' is run automatically by unittest.
    """

    def setUp(self):
        """
        I run this before every single test.
        I create a fresh daily habit and a fresh weekly habit so each test
        starts with clean, empty habits and no check-offs.
        """
        self.daily_habit  = Habit("Test Daily",  "A daily test habit",  "daily")
        self.weekly_habit = Habit("Test Weekly", "A weekly test habit", "weekly")

    def test_habit_is_created_correctly(self):
        """
        I check that a new Habit object is set up with the correct values.
        """
        self.assertEqual(self.daily_habit.name,        "Test Daily")
        self.assertEqual(self.daily_habit.description, "A daily test habit")
        self.assertEqual(self.daily_habit.periodicity, "daily")
        self.assertEqual(self.daily_habit.checkoffs,   [])

    def test_checkoff_adds_a_timestamp(self):
        """
        I check that calling checkoff() adds one timestamp to the list.
        """
        self.daily_habit.checkoff("2024-01-15 09:00:00")
        self.assertEqual(len(self.daily_habit.checkoffs), 1)
        self.assertEqual(self.daily_habit.checkoffs[0], "2024-01-15 09:00:00")

    def test_multiple_checkoffs_are_all_stored(self):
        """
        I check that checking off a habit three times stores all three records.
        """
        self.daily_habit.checkoff("2024-01-15 09:00:00")
        self.daily_habit.checkoff("2024-01-16 09:00:00")
        self.daily_habit.checkoff("2024-01-17 09:00:00")
        self.assertEqual(len(self.daily_habit.checkoffs), 3)

    def test_current_streak_for_three_days_in_a_row(self):
        """
        I check that three consecutive daily check-offs give a streak of 3.
        """
        self.daily_habit.checkoff("2024-01-15 09:00:00")
        self.daily_habit.checkoff("2024-01-16 09:00:00")
        self.daily_habit.checkoff("2024-01-17 09:00:00")
        self.assertEqual(self.daily_habit.get_current_streak(), 3)

    def test_streak_breaks_when_a_day_is_missed(self):
        """
        I check that missing one day resets the current streak correctly.
        The streak should only count the days after the gap.
        """
        self.daily_habit.checkoff("2024-01-13 09:00:00")
        self.daily_habit.checkoff("2024-01-14 09:00:00")
        # Jan 15 is missing so the streak breaks here
        self.daily_habit.checkoff("2024-01-16 09:00:00")
        # The current streak should be 1 because only Jan 16 follows the gap
        self.assertEqual(self.daily_habit.get_current_streak(), 1)

    def test_longest_streak_is_remembered_after_a_break(self):
        """
        I check that the longest streak is still remembered after a gap.
        """
        self.daily_habit.checkoff("2024-01-01 09:00:00")
        self.daily_habit.checkoff("2024-01-02 09:00:00")
        self.daily_habit.checkoff("2024-01-03 09:00:00")
        self.daily_habit.checkoff("2024-01-04 09:00:00")
        self.daily_habit.checkoff("2024-01-05 09:00:00")
        # Jan 6 is missing, streak breaks
        self.daily_habit.checkoff("2024-01-07 09:00:00")
        self.daily_habit.checkoff("2024-01-08 09:00:00")
        # Current streak should be 2
        self.assertEqual(self.daily_habit.get_current_streak(), 2)
        # Best streak should still be 5
        self.assertEqual(self.daily_habit.get_longest_streak(), 5)

    def test_zero_checkoffs_gives_zero_streak(self):
        """
        I check that a habit with no check-offs has a streak of 0.
        """
        self.assertEqual(self.daily_habit.get_current_streak(), 0)
        self.assertEqual(self.daily_habit.get_longest_streak(), 0)

    def test_weekly_streak_for_two_weeks_in_a_row(self):
        """
        I check that completing a weekly habit two weeks in a row gives a streak of 2.
        """
        self.weekly_habit.checkoff("2024-01-01 10:00:00")  # Week 1
        self.weekly_habit.checkoff("2024-01-08 10:00:00")  # Week 2
        self.assertEqual(self.weekly_habit.get_current_streak(), 2)

    def test_to_dict_contains_correct_keys(self):
        """
        I check that to_dict() returns a dictionary with all the expected keys.
        """
        habit_dict = self.daily_habit.to_dict()
        self.assertIn("name",          habit_dict)
        self.assertIn("description",   habit_dict)
        self.assertIn("periodicity",   habit_dict)
        self.assertIn("creation_date", habit_dict)
        self.assertIn("checkoffs",     habit_dict)

    def test_to_dict_and_from_dict_roundtrip(self):
        """
        I check that converting a habit to a dict and back gives the same habit.
        """
        self.daily_habit.checkoff("2024-01-15 09:00:00")
        habit_dict     = self.daily_habit.to_dict()
        recreated      = Habit.from_dict(habit_dict)
        self.assertEqual(recreated.name,        self.daily_habit.name)
        self.assertEqual(recreated.description, self.daily_habit.description)
        self.assertEqual(recreated.periodicity, self.daily_habit.periodicity)
        self.assertEqual(recreated.checkoffs,   self.daily_habit.checkoffs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
