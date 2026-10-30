"""
analytics.py
------------
I provide all the ANALYSIS functions for my habit tracker here.

The assignment requires that analytics be written using FUNCTIONAL PROGRAMMING.
In functional programming, I:
  - Use functions (not objects/classes) as the main building blocks
  - Use built-in tools like filter(), map(), and max() that work on lists
  - Avoid modifying data — each function just takes input and returns output

Think of these functions as "questions you can ask about your habits".
"""

# I import List from typing so my function signatures are crystal clear
# about what kind of data they accept and return
from typing import List

# I import the Habit class so I can work with Habit objects in my functions
from habit import Habit


# ----------------------------------------------------------------------
# Function 1: Return ALL habits
# ----------------------------------------------------------------------
def get_all_habits(habits: List[Habit]) -> List[Habit]:
    """
    I return a list of every habit the user is currently tracking.
    This is the simplest possible function — I just return the full list as-is.

    Args:
        habits (List[Habit]): The full list of all Habit objects.

    Returns:
        List[Habit]: The same list, containing every habit.
    """

    # I simply return every habit in the list — nothing filtered out
    return habits


# ----------------------------------------------------------------------
# Function 2: Return habits filtered by their periodicity
# ----------------------------------------------------------------------
def get_habits_by_periodicity(habits: List[Habit], periodicity: str) -> List[Habit]:
    """
    I filter the list of habits and return ONLY those that match a given periodicity.
    For example, if I pass "daily", I get back only the daily habits.

    I use Python's built-in filter() function here — that's functional programming!
    filter() goes through every item in the list and keeps only those where
    the condition (the lambda function) is True.

    Args:
        habits (List[Habit]):  The full list of all habits.
        periodicity (str):     Either "daily" or "weekly".

    Returns:
        List[Habit]: Only the habits whose periodicity matches the given value.
    """

    # I use filter() with a lambda (anonymous function) to select matching habits.
    # The lambda checks: "does this habit's periodicity match what I want?"
    # I wrap the result in list() because filter() returns a lazy iterator, not a list.
    return list(filter(lambda h: h.periodicity == periodicity, habits))


# ----------------------------------------------------------------------
# Function 3: Return the single longest streak across ALL habits
# ----------------------------------------------------------------------
def get_longest_streak_all(habits: List[Habit]) -> int:
    """
    I look at ALL habits and return the single highest (longest) streak
    that any habit has ever achieved.

    This answers the question: "What is my personal best streak across all habits?"

    I use Python's built-in max() function — that's functional programming!
    max() combined with map() is a very clean functional way to find the biggest value.

    Args:
        habits (List[Habit]): The full list of all habits.

    Returns:
        int: The highest streak number across all habits combined.
             Returns 0 if there are no habits.
    """

    # I return 0 immediately if there are no habits to analyse
    if not habits:
        return 0

    # I use map() to call get_longest_streak() on every single habit.
    # map() is a functional programming tool that applies a function to every item.
    # Then I use max() to find the biggest value from all those streak numbers.
    return max(map(lambda h: h.get_longest_streak(), habits))


# ----------------------------------------------------------------------
# Function 4: Return the longest streak for ONE specific habit
# ----------------------------------------------------------------------
def get_longest_streak_for_habit(habits: List[Habit], habit_name: str) -> int:
    """
    I find a specific habit by name and return its longest-ever streak.

    This answers: "What is my best streak for habit X?"

    Args:
        habits (List[Habit]): The full list of all habits.
        habit_name (str):     The exact name of the habit to look up.

    Returns:
        int: The longest streak for that habit. Returns -1 if the habit is not found.
    """

    # I use next() with a generator expression to find the first habit
    # whose name matches. If no match is found, I return None.
    # This is a clean functional way to search a list without a for-loop.
    found_habit = next(
        (h for h in habits if h.name.lower() == habit_name.lower()),
        None   # I return None as the default if nothing is found
    )

    # If I didn't find the habit, I return -1 to signal "not found"
    if found_habit is None:
        return -1

    # I found the habit! I return its all-time longest streak.
    return found_habit.get_longest_streak()


# ----------------------------------------------------------------------
# Function 5: Return a summary for ALL habits (name + current streak)
# ----------------------------------------------------------------------
def get_habit_summary(habits: List[Habit]) -> List[dict]:
    """
    I create a summary list — one dictionary entry per habit — containing
    each habit's name, periodicity, current streak, and longest streak ever.

    This is useful for displaying an overview table to the user.

    I use map() here — I apply a "make a summary dictionary" function to
    every habit in the list. That's functional programming!

    Args:
        habits (List[Habit]): The full list of all habits.

    Returns:
        List[dict]: A list of dictionaries, each summarising one habit.
    """

    # I use map() to transform each Habit object into a summary dictionary
    def make_summary(h: Habit) -> dict:
        """
        I am a small helper function that turns ONE Habit into a summary dict.
        """
        return {
            "name":           h.name,
            "description":    h.description,
            "periodicity":    h.periodicity,
            "current_streak": h.get_current_streak(),
            "longest_streak": h.get_longest_streak(),
            "total_checkoffs": len(h.checkoffs),
        }

    # I apply make_summary() to every habit and return the result as a list
    return list(map(make_summary, habits))


# ----------------------------------------------------------------------
# Function 6: Find habits the user is struggling with (broken streaks)
# ----------------------------------------------------------------------
def get_struggling_habits(habits: List[Habit]) -> List[Habit]:
    """
    I return the habits where the user has check-off history BUT the current
    streak is 0 — meaning the user has broken the habit (missed at least one period).

    This answers: "Which habits am I failing to keep up with?"

    Args:
        habits (List[Habit]): The full list of all habits.

    Returns:
        List[Habit]: Habits that have been broken (streak = 0 but history exists).
    """

    # I use filter() to find habits where:
    # - the user has done the habit at least once (len(h.checkoffs) > 0)
    # - the current streak is 0 (they missed the most recent period)
    return list(filter(
        lambda h: len(h.checkoffs) > 0 and h.get_current_streak() == 0,
        habits
    ))
