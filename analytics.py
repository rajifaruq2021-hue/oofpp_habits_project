"""
analytics.py

I provide all the analysis functions for the habit tracker.

The course requires that analytics be written using Functional Programming.
In functional programming I use functions as the main building blocks.
I also use built-in Python tools like filter(), map(), and max()
that work on lists without changing the original data.

Think of each function here as a question you can ask about your habits.
"""

# I import List from typing so it is clear what each function expects
from typing import List

# I import the Habit class so I can work with Habit objects
from habit import Habit


def get_all_habits(habits: List[Habit]) -> List[Habit]:
    """
    I return a list of every habit the user is tracking.
    This is the simplest function. I just give back the full list.

    Args:
        habits (List[Habit]): the full list of all Habit objects.

    Returns:
        List[Habit]: the same list with every habit in it.
    """

    # I return all habits with no filter applied
    return habits


def get_habits_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    """
    I return only the habits that match a given periodicity.
    For example, if I pass "daily" I get back only the daily habits.

    I use Python's built-in filter() function here.
    filter() goes through each item in the list and keeps only the ones
    where the condition is True.

    Args:
        habits (List[Habit]): the full list of all habits.
        periodicity (str)   : either "daily" or "weekly".

    Returns:
        List[Habit]: only the habits whose periodicity matches.
    """

    # I use filter() with a short lambda function to keep only matching habits
    # I wrap the result in list() because filter() gives back an iterator
    return list(filter(lambda h: h.periodicity == periodicity, habits))


def get_longest_streak_all(habits: List[Habit]) -> int:
    """
    I look at all habits and return the single highest streak
    that any habit has ever reached.

    This answers the question: what is my best streak across all habits?

    I use map() and max() here, which is functional programming.

    Args:
        habits (List[Habit]): the full list of all habits.

    Returns:
        int: the highest streak number across all habits.
             Returns 0 if there are no habits.
    """

    # I return 0 straight away if there are no habits
    if not habits:
        return 0

    # I use map() to call get_longest_streak() on each habit
    # Then I use max() to find the biggest number from all those results
    return max(map(lambda h: h.get_longest_streak(), habits))


def get_longest_streak_for_habit(habits: List[Habit], habit_name: str) -> int:
    """
    I find a specific habit by name and return its longest ever streak.

    This answers the question: what is my best streak for habit X?

    Args:
        habits (List[Habit]): the full list of all habits.
        habit_name (str)    : the exact name of the habit to look up.

    Returns:
        int: the longest streak for that habit.
             Returns -1 if the habit is not found.
    """

    # I use next() to find the first habit whose name matches
    # If no match is found, next() returns None
    found = next((h for h in habits if h.name == habit_name), None)

    # I return -1 to show the habit was not found
    if found is None:
        return -1

    return found.get_longest_streak()


def get_habit_summary(habit: Habit) -> dict:
    """
    I create a short summary of one habit and return it as a dictionary.
    The summary includes the name, type, current streak, and best streak.

    Args:
        habit (Habit): the habit to summarise.

    Returns:
        dict: a dictionary with the key details about the habit.
    """

    return {
        "name":           habit.name,
        "periodicity":    habit.periodicity,
        "current_streak": habit.get_current_streak(),
        "longest_streak": habit.get_longest_streak(),
        "total_checkoffs": len(habit.checkoffs),
    }
