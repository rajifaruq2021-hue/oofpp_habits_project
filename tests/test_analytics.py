"""
tests/test_analytics.py

I test all the analytics functions to make sure they give correct results.
I use Python's built-in unittest module.
"""

import unittest
import sys
import os

# I add the parent folder to the path so Python can find analytics.py and habit.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from habit import Habit
import analytics


def make_habit(name, periodicity, checkoffs):
    """
    I create a Habit object and give it a ready-made list of check-offs.
    This is a helper I use in multiple tests.
    """
    h = Habit(name=name, description="test", periodicity=periodicity)
    h.checkoffs = checkoffs
    return h


class TestAnalytics(unittest.TestCase):
    """
    I group all analytics tests inside this class.
    """

    def setUp(self):
        """
        I create a small set of test habits before each test.
        """
        self.daily1 = make_habit("Run",  "daily",  [
            "2024-01-01 08:00:00", "2024-01-02 08:00:00", "2024-01-03 08:00:00"
        ])
        self.daily2 = make_habit("Read", "daily",  [
            "2024-01-01 08:00:00", "2024-01-02 08:00:00"
        ])
        self.weekly1 = make_habit("Review", "weekly", [
            "2024-01-01 08:00:00", "2024-01-08 08:00:00"
        ])
        self.weekly2 = make_habit("Call",   "weekly", [
            "2024-01-01 08:00:00"
        ])
        self.all_habits = [self.daily1, self.daily2, self.weekly1, self.weekly2]

    def test_get_all_habits_returns_all_four(self):
        """
        I check that get_all_habits() returns all four habits.
        """
        result = analytics.get_all_habits(self.all_habits)
        self.assertEqual(len(result), 4)

    def test_get_daily_habits_returns_two(self):
        """
        I check that filtering by "daily" returns only the two daily habits.
        """
        result = analytics.get_habits_by_periodicity(self.all_habits, "daily")
        self.assertEqual(len(result), 2)
        for h in result:
            self.assertEqual(h.periodicity, "daily")

    def test_get_weekly_habits_returns_two(self):
        """
        I check that filtering by "weekly" returns only the two weekly habits.
        """
        result = analytics.get_habits_by_periodicity(self.all_habits, "weekly")
        self.assertEqual(len(result), 2)
        for h in result:
            self.assertEqual(h.periodicity, "weekly")

    def test_get_longest_streak_all_returns_correct_value(self):
        """
        I check that the best streak across all habits is found correctly.
        The daily1 habit has 3 days in a row, so the answer should be 3.
        """
        result = analytics.get_longest_streak_all(self.all_habits)
        self.assertEqual(result, 3)

    def test_get_longest_streak_all_returns_zero_for_empty_list(self):
        """
        I check that passing an empty list returns 0 and does not cause an error.
        """
        result = analytics.get_longest_streak_all([])
        self.assertEqual(result, 0)

    def test_get_longest_streak_for_run_habit(self):
        """
        I check that the longest streak for the "Run" habit is 3.
        """
        result = analytics.get_longest_streak_for_habit(self.all_habits, "Run")
        self.assertEqual(result, 3)

    def test_get_longest_streak_for_read_habit(self):
        """
        I check that the longest streak for the "Read" habit is 2.
        """
        result = analytics.get_longest_streak_for_habit(self.all_habits, "Read")
        self.assertEqual(result, 2)

    def test_get_longest_streak_returns_minus_one_for_unknown_habit(self):
        """
        I check that looking for a habit that does not exist returns -1.
        """
        result = analytics.get_longest_streak_for_habit(self.all_habits, "Unknown Habit")
        self.assertEqual(result, -1)

    def test_get_habit_summary_has_correct_keys(self):
        """
        I check that get_habit_summary() returns a dictionary with the right keys.
        """
        summary = analytics.get_habit_summary(self.daily1)
        self.assertIn("name",           summary)
        self.assertIn("periodicity",    summary)
        self.assertIn("current_streak", summary)
        self.assertIn("longest_streak", summary)
        self.assertIn("total_checkoffs",summary)

    def test_get_habit_summary_values_are_correct(self):
        """
        I check that the summary values for the Run habit are all correct.
        """
        summary = analytics.get_habit_summary(self.daily1)
        self.assertEqual(summary["name"],            "Run")
        self.assertEqual(summary["periodicity"],     "daily")
        self.assertEqual(summary["total_checkoffs"], 3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
