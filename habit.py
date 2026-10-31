"""
habit.py

I am the Habit class. This file is the main building block of the app.
Each habit the user creates is stored as one object made from this class.

I use Object Oriented Programming (OOP) here.
That means I group all the data and actions for a habit together in one place.

When the user runs the app, Python creates one Habit object for every habit.
"""

# I import datetime so I can work with dates and times
from datetime import datetime, timedelta


class Habit:
    """
    I represent one habit that the user wants to track.

    Each habit has:
        name        : a short label, for example "Morning Run"
        description : a sentence about why the habit matters
        periodicity : how often to do it, either "daily" or "weekly"
        creation_date: the date the habit was first added
        checkoffs   : a list of timestamps showing when it was completed
    """

    def __init__(self, name, description, periodicity, creation_date=None, checkoffs=None):
        """
        I set up a new Habit object with the given details.

        Args:
            name (str)          : the habit name, for example "Read a Book"
            description (str)   : a short sentence about the habit
            periodicity (str)   : "daily" or "weekly"
            creation_date (str) : when this habit was created (optional)
            checkoffs (list)    : list of past completion timestamps (optional)
        """

        # I store the basic details about this habit
        self.name = name
        self.description = description
        self.periodicity = periodicity

        # I record when this habit was created
        # If no date is given, I use today as the creation date
        if creation_date is None:
            self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.creation_date = creation_date

        # I store the list of times the habit was completed
        # If nothing is given, I start with an empty list
        if checkoffs is None:
            self.checkoffs = []
        else:
            self.checkoffs = checkoffs

    def checkoff(self, timestamp=None):
        """
        I mark this habit as done.
        I add the current time (or a given time) to the list of completions.

        Args:
            timestamp (str): the time to record (optional).
                             If not given, I use right now.
        """

        # I use the given time, or the current time if none is given
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # I add the timestamp to the list of completions
        self.checkoffs.append(timestamp)

    def get_current_streak(self):
        """
        I count how many periods in a row this habit has been completed
        up to the most recent check-off.

        For a daily habit, one period = one day.
        For a weekly habit, one period = one week.

        Returns:
            int: the number of periods completed in a row.
                 Returns 0 if the habit has never been completed.
        """

        # I return 0 right away if there are no completions yet
        if not self.checkoffs:
            return 0

        # I sort the completions from oldest to newest so I can read them in order
        sorted_times = sorted(self.checkoffs)

        if self.periodicity == "daily":
            # I get only the date part (no time) from each timestamp
            # I also remove duplicate dates so one day counts as one completion
            dates = sorted(set(
                datetime.strptime(t, "%Y-%m-%d %H:%M:%S").date()
                for t in sorted_times
            ))

            # I start counting from 1 because the last date always counts
            streak = 1
            # I go backwards through the dates, checking if each one is one day before the next
            for i in range(len(dates) - 1, 0, -1):
                if (dates[i] - dates[i - 1]).days == 1:
                    # I add one because this day is right after the one before it
                    streak += 1
                else:
                    # The chain is broken so I stop counting
                    break
            return streak

        else:
            # For weekly habits, I get the ISO week number from each timestamp
            # I also remove duplicate weeks so one week counts as one completion
            weeks = sorted(set(
                datetime.strptime(t, "%Y-%m-%d %H:%M:%S").isocalendar()[:2]
                for t in sorted_times
            ))

            # I start counting from 1 because the last week always counts
            streak = 1
            # I go backwards and check if each week is exactly one week before the next
            for i in range(len(weeks) - 1, 0, -1):
                year_now,  week_now  = weeks[i]
                year_prev, week_prev = weeks[i - 1]
                # I convert the week to a number so subtraction is easy
                total_now  = year_now  * 52 + week_now
                total_prev = year_prev * 52 + week_prev
                if total_now - total_prev == 1:
                    streak += 1
                else:
                    break
            return streak

    def get_longest_streak(self):
        """
        I find the longest run of consecutive periods this habit has ever had.
        This is the all-time best, not just the current run.

        Returns:
            int: the best streak this habit has ever reached.
                 Returns 0 if the habit has never been completed.
        """

        # I return 0 right away if there are no completions
        if not self.checkoffs:
            return 0

        sorted_times = sorted(self.checkoffs)

        if self.periodicity == "daily":
            dates = sorted(set(
                datetime.strptime(t, "%Y-%m-%d %H:%M:%S").date()
                for t in sorted_times
            ))

            # I keep track of the best and current run
            best = 1
            current = 1
            for i in range(1, len(dates)):
                if (dates[i] - dates[i - 1]).days == 1:
                    # I add one because today follows yesterday
                    current += 1
                    # I update the best if the current run is now longer
                    if current > best:
                        best = current
                else:
                    # The run broke so I reset to 1
                    current = 1
            return best

        else:
            weeks = sorted(set(
                datetime.strptime(t, "%Y-%m-%d %H:%M:%S").isocalendar()[:2]
                for t in sorted_times
            ))

            best = 1
            current = 1
            for i in range(1, len(weeks)):
                y1, w1 = weeks[i - 1]
                y2, w2 = weeks[i]
                if y2 * 52 + w2 - (y1 * 52 + w1) == 1:
                    current += 1
                    if current > best:
                        best = current
                else:
                    current = 1
            return best

    def to_dict(self):
        """
        I turn this Habit object into a plain dictionary.
        This makes it easy to save the habit to the database.

        Returns:
            dict: a dictionary with all the habit data.
        """

        return {
            "name":          self.name,
            "description":   self.description,
            "periodicity":   self.periodicity,
            "creation_date": self.creation_date,
            "checkoffs":     self.checkoffs,
        }

    @classmethod
    def from_dict(cls, data):
        """
        I create a new Habit object from a dictionary.
        This is used when loading habits from the database.

        Args:
            data (dict): a dictionary with the habit data.

        Returns:
            Habit: a new Habit object with all the saved data.
        """

        return cls(
            name          = data["name"],
            description   = data["description"],
            periodicity   = data["periodicity"],
            creation_date = data.get("creation_date"),
            checkoffs     = data.get("checkoffs", []),
        )
