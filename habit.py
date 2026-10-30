"""
habit.py
--------
I define the main Habit class here.
A Habit is the core building block of my habit tracker.
Think of it like a container that holds:
  - the name of the habit (e.g., "Drink Water")
  - how often you must do it (daily or weekly)
  - the date it was created
  - a list of all the times the user has checked it off (completed it)
"""

# I import datetime so I can work with dates and times easily
from datetime import datetime, date, timedelta


class Habit:
    """
    I am the Habit class. I represent ONE habit the user wants to track.

    Attributes:
        name (str):         The name of the habit, e.g. "Exercise".
        description (str):  A short explanation of what the habit is about.
        periodicity (str):  How often the habit must be done — "daily" or "weekly".
        creation_date (str):The date and time when this habit was first created.
        checkoffs (list):   A list of date-time strings, one for each time
                            the user marked this habit as done (checked it off).
    """

    def __init__(self, name: str, description: str, periodicity: str,
                 creation_date: str = None, checkoffs: list = None):
        """
        I use __init__ to set up a brand-new Habit object.
        This runs automatically whenever I create a new Habit.

        Args:
            name (str):         The name of this habit.
            description (str):  A short description of the habit.
            periodicity (str):  Either "daily" or "weekly".
            creation_date (str):The timestamp when this habit was created.
                                If I leave it empty, I use right now.
            checkoffs (list):   A list of previous check-off timestamps.
                                If I leave it empty, I start with an empty list.
        """

        # I store the name of the habit (e.g. "Drink 2 Litres of Water")
        self.name = name

        # I store a short description so the user knows what this habit is about
        self.description = description

        # I make sure the periodicity is either "daily" or "weekly" — nothing else allowed
        if periodicity not in ("daily", "weekly"):
            raise ValueError(
                f"Periodicity must be 'daily' or 'weekly', but I got '{periodicity}'."
            )
        self.periodicity = periodicity

        # I record when this habit was created.
        # If no date was given, I use the current date and time.
        self.creation_date = creation_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # I start with an empty check-off list if the user did not provide any previous data
        self.checkoffs = checkoffs if checkoffs is not None else []

    # ------------------------------------------------------------------
    # Method 1: Check off the habit (mark it as done for today/this week)
    # ------------------------------------------------------------------
    def checkoff(self, timestamp: str = None):
        """
        I call this method to mark the habit as completed right now.
        I record the exact date and time so we know when it was done.

        Args:
            timestamp (str): Optional. If I provide a date-time string like
                             "2024-01-15 09:00:00", I use that. Otherwise I
                             use the current moment.
        """

        # I use the timestamp the user gave me, or I create one right now
        ts = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # I add this timestamp to the list of check-offs for this habit
        self.checkoffs.append(ts)

    # ------------------------------------------------------------------
    # Method 2: Get all the periods (days or weeks) when this habit was done
    # ------------------------------------------------------------------
    def get_completed_periods(self) -> list:
        """
        I look at all the check-off timestamps and figure out which
        time periods (days or weeks) the user actually completed this habit.

        For a DAILY habit: a "period" is one calendar day (e.g. 2024-01-15).
        For a WEEKLY habit: a "period" is one ISO calendar week (e.g. 2024-W03).

        Returns:
            list: A sorted list of unique period labels where the habit was done.
        """

        # I create an empty set to collect unique periods (sets avoid duplicates automatically)
        completed = set()

        # I go through every single check-off timestamp one by one
        for ts in self.checkoffs:
            # I convert the string timestamp into a real Python datetime object
            dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")

            if self.periodicity == "daily":
                # For daily habits, the "period" is just the date (e.g. "2024-01-15")
                period_label = dt.strftime("%Y-%m-%d")
            else:
                # For weekly habits, the "period" is the ISO year + week number
                # Example: "2024-W03" means week 3 of the year 2024
                year, week, _ = dt.isocalendar()
                period_label = f"{year}-W{week:02d}"

            # I add this label to the set (duplicates are ignored automatically)
            completed.add(period_label)

        # I return the unique periods sorted from oldest to newest
        return sorted(completed)

    # ------------------------------------------------------------------
    # Method 3: Calculate the current streak (consecutive periods done)
    # ------------------------------------------------------------------
    def get_current_streak(self) -> int:
        """
        I calculate how many periods IN A ROW the user has been doing this habit
        UP TO AND INCLUDING the most recent completed period.

        For example:
        - If I did a daily habit on Jan 13, 14, 15 and today is Jan 15, streak = 3.
        - If I missed Jan 14, the streak resets to 1 (only Jan 15 counts).

        Returns:
            int: The number of consecutive periods completed (the current streak).
        """

        # I get the list of all completed periods in sorted order
        completed = self.get_completed_periods()

        # If there are no check-offs at all, the streak is obviously zero
        if not completed:
            return 0

        # I start counting from 1 (the most recent period always counts)
        streak = 1

        # I look backwards through the list of completed periods (from most recent)
        # and count how many are consecutive (no gaps)
        for i in range(len(completed) - 1, 0, -1):
            # I check if the current period and the previous period are right next to each other
            if self._are_consecutive(completed[i - 1], completed[i]):
                # They are consecutive! I add 1 to the streak
                streak += 1
            else:
                # There is a gap — the streak is broken, so I stop counting
                break

        return streak

    # ------------------------------------------------------------------
    # Method 4: Calculate the LONGEST streak ever achieved
    # ------------------------------------------------------------------
    def get_longest_streak(self) -> int:
        """
        I look at ALL the check-off history and find the longest chain of
        consecutive periods the user ever achieved — not just the current one.

        For example, if the user did 7 days in a row in January but then broke
        the streak, and is now on a 3-day streak, this method returns 7.

        Returns:
            int: The all-time longest streak ever.
        """

        # I get all the completed periods in sorted order
        completed = self.get_completed_periods()

        # If there are no check-offs, the longest streak is zero
        if not completed:
            return 0

        # I start with a current streak of 1 and a max streak of 1
        current_streak = 1
        max_streak = 1

        # I go through the list of completed periods from the second item onward
        for i in range(1, len(completed)):
            if self._are_consecutive(completed[i - 1], completed[i]):
                # These two periods are back-to-back — the streak continues
                current_streak += 1
                # I update the maximum if this streak is the longest so far
                if current_streak > max_streak:
                    max_streak = current_streak
            else:
                # There is a gap — I reset the current streak back to 1
                current_streak = 1

        return max_streak

    # ------------------------------------------------------------------
    # Method 5 (helper): Check if two period labels are consecutive
    # ------------------------------------------------------------------
    def _are_consecutive(self, period_a: str, period_b: str) -> bool:
        """
        I check whether period_b comes exactly one step after period_a.
        - For daily habits: one step = one calendar day.
        - For weekly habits: one step = one calendar week.

        I use an underscore at the start of the name (_are_consecutive) to show
        that this is a "private helper" method — it's meant to be used only
        inside this class, not by outside code.

        Args:
            period_a (str): The earlier period label.
            period_b (str): The later period label.

        Returns:
            bool: True if period_b is exactly one step after period_a, else False.
        """

        if self.periodicity == "daily":
            # I convert the date strings back into Python date objects so I can do math
            date_a = date.fromisoformat(period_a)   # e.g. "2024-01-14" → date object
            date_b = date.fromisoformat(period_b)   # e.g. "2024-01-15" → date object

            # I check if exactly 1 day separates the two dates
            return (date_b - date_a) == timedelta(days=1)

        else:  # weekly
            # Weekly labels look like "2024-W03". I split them to get year and week number.
            year_a, week_a = int(period_a[:4]), int(period_a[6:])
            year_b, week_b = int(period_b[:4]), int(period_b[6:])

            # I convert both week labels to actual Monday dates, then compare them
            # Python's fromisocalendar(year, week, 1) gives the Monday of that ISO week
            monday_a = date.fromisocalendar(year_a, week_a, 1)
            monday_b = date.fromisocalendar(year_b, week_b, 1)

            # I check if exactly 7 days (= 1 week) separates the two Mondays
            return (monday_b - monday_a) == timedelta(weeks=1)

    # ------------------------------------------------------------------
    # Method 6: Convert this Habit to a dictionary (for saving to JSON/DB)
    # ------------------------------------------------------------------
    def to_dict(self) -> dict:
        """
        I convert this Habit object into a plain Python dictionary.
        This makes it easy to save the habit to a file or database.

        Returns:
            dict: A dictionary containing all the habit's data.
        """

        # I pack all the important data into a dictionary and return it
        return {
            "name":          self.name,
            "description":   self.description,
            "periodicity":   self.periodicity,
            "creation_date": self.creation_date,
            "checkoffs":     self.checkoffs,
        }

    # ------------------------------------------------------------------
    # Method 7 (class method): Create a Habit from a dictionary
    # ------------------------------------------------------------------
    @classmethod
    def from_dict(cls, data: dict):
        """
        I create a Habit object from a dictionary.
        This is the reverse of to_dict() — I use it when LOADING data
        from a file or database back into a Habit object.

        The @classmethod decorator means I call this method on the class
        itself (Habit.from_dict(data)) rather than on an instance.

        Args:
            data (dict): A dictionary with habit data (same format as to_dict()).

        Returns:
            Habit: A fully reconstructed Habit object.
        """

        # I create and return a new Habit using the values from the dictionary
        return cls(
            name=data["name"],
            description=data["description"],
            periodicity=data["periodicity"],
            creation_date=data.get("creation_date"),
            checkoffs=data.get("checkoffs", []),
        )

    # ------------------------------------------------------------------
    # Method 8: A nice readable string representation of this habit
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        """
        I define how this Habit looks when I print it or inspect it.
        This is useful for debugging — Python calls __repr__ automatically
        when I print a Habit object.
        """

        # I return a short, readable description of the habit
        return (
            f"Habit(name='{self.name}', periodicity='{self.periodicity}', "
            f"streak={self.get_current_streak()})"
        )
