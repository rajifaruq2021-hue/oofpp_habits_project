"""
main.py
-------
I am the MAIN entry point for the Habit Tracker App.
I provide a simple, interactive command-line menu that the user can navigate
by typing numbers. No complex commands needed — just pick a number!

When the user runs: python main.py
This file starts and shows the main menu.

Menu structure:
  1. View all habits
  2. Add a new habit
  3. Check off a habit (mark it as done)
  4. Delete a habit
  5. Analyse habits
  6. Exit
"""

# I import the os module so I can clear the screen (makes the menu look clean)
import os

# I import datetime so I can show the current date and time to the user
from datetime import datetime

# I import my own modules that I created for this project
import db           # handles saving and loading from the database
import analytics    # provides all the analysis functions
import seed_data    # loads the 5 pre-defined example habits
from habit import Habit  # the Habit class I defined in habit.py


# I define the path to my SQLite database file here in ONE place
# so it's easy to change later if needed
DB_PATH = "habits.db"


# =======================================================================
# HELPER FUNCTIONS — small tools I use throughout the app
# =======================================================================

def clear_screen():
    """
    I clear the terminal screen to keep the interface looking tidy.
    I use 'cls' on Windows and 'clear' on Mac/Linux.
    """
    # I check the operating system and run the right clear command
    os.system("cls" if os.name == "nt" else "clear")


def print_separator():
    """
    I print a simple line of dashes to visually separate sections in the menu.
    This makes the output much easier to read.
    """
    # I print 55 dashes as a visual divider
    print("-" * 55)


def press_enter_to_continue():
    """
    I pause the program and wait for the user to press Enter before continuing.
    This gives the user time to read the output before the screen changes.
    """
    # I display a prompt and wait for any input from the user
    input("\n  Press ENTER to return to the main menu...")


# =======================================================================
# DISPLAY FUNCTIONS — functions that show information to the user
# =======================================================================

def display_main_menu():
    """
    I draw the main menu on the screen.
    I show the current date and time so the user is aware of when they are.
    """

    # I clear the screen first for a fresh look
    clear_screen()

    # I get the current date and time and format it nicely
    now = datetime.now().strftime("%A, %d %B %Y  |  %H:%M")

    # I print the app header and the date/time
    print("\n" + "=" * 55)
    print("      🌟  MY HABIT TRACKER  🌟")
    print(f"      {now}")
    print("=" * 55)

    # I print each menu option with a number the user can type
    print("  1. 📋  View all my habits")
    print("  2. ➕  Add a new habit")
    print("  3. ✅  Check off a habit (mark as done today)")
    print("  4. 🗑️  Delete a habit")
    print("  5. 📊  Analyse my habits")
    print("  6. 🚪  Exit")
    print_separator()


def display_all_habits(habits: list):
    """
    I display a nicely formatted table of all habits.

    Args:
        habits (list): The list of Habit objects to display.
    """

    # I clear the screen and print a title
    clear_screen()
    print("\n" + "=" * 55)
    print("  📋  ALL MY HABITS")
    print("=" * 55)

    # I check if there are any habits to show at all
    if not habits:
        print("  You have no habits yet. Add one from the main menu!")
        return

    # I use the analytics module to get a summary for each habit
    summaries = analytics.get_habit_summary(habits)

    # I print each habit's summary in a readable format
    for i, s in enumerate(summaries, start=1):
        # I print the habit number, name, and periodicity
        print(f"\n  [{i}] {s['name']}  ({s['periodicity'].upper()})")
        print(f"      Description  : {s['description']}")
        print(f"      Current Streak: {s['current_streak']} {s['periodicity'].replace('daily','day(s)').replace('weekly','week(s)')}")
        print(f"      Longest Streak: {s['longest_streak']} {s['periodicity'].replace('daily','day(s)').replace('weekly','week(s)')}")
        print(f"      Total Check-offs: {s['total_checkoffs']}")
        print_separator()


def display_analysis_menu(habits: list):
    """
    I show the analytics sub-menu and let the user choose what to analyse.

    Args:
        habits (list): The list of Habit objects to analyse.
    """

    # I keep showing the analysis menu until the user chooses "Back"
    while True:
        clear_screen()
        print("\n" + "=" * 55)
        print("  📊  ANALYSE MY HABITS")
        print("=" * 55)
        print("  1. Show all daily habits")
        print("  2. Show all weekly habits")
        print("  3. Find the longest streak across ALL habits")
        print("  4. Find the longest streak for ONE specific habit")
        print("  5. Show habits I am struggling with")
        print("  6. ← Back to main menu")
        print_separator()

        # I ask the user to pick an option
        choice = input("  Enter your choice (1-6): ").strip()

        if choice == "1":
            # I want to see only the daily habits
            daily = analytics.get_habits_by_periodicity(habits, "daily")
            clear_screen()
            print("\n  📅  DAILY HABITS")
            print_separator()
            if not daily:
                print("  You have no daily habits yet.")
            else:
                for h in daily:
                    # I print each daily habit's name and current streak
                    print(f"  • {h.name}  |  Current streak: {h.get_current_streak()} day(s)")
            press_enter_to_continue()

        elif choice == "2":
            # I want to see only the weekly habits
            weekly = analytics.get_habits_by_periodicity(habits, "weekly")
            clear_screen()
            print("\n  🗓️  WEEKLY HABITS")
            print_separator()
            if not weekly:
                print("  You have no weekly habits yet.")
            else:
                for h in weekly:
                    print(f"  • {h.name}  |  Current streak: {h.get_current_streak()} week(s)")
            press_enter_to_continue()

        elif choice == "3":
            # I want to find the single best streak across all my habits
            best = analytics.get_longest_streak_all(habits)
            clear_screen()
            print("\n  🏆  LONGEST STREAK ACROSS ALL HABITS")
            print_separator()
            print(f"  My personal best streak is: {best} period(s) in a row!")
            press_enter_to_continue()

        elif choice == "4":
            # I want to look up the best streak for one particular habit
            clear_screen()
            print("\n  🔍  LONGEST STREAK FOR A SPECIFIC HABIT")
            print_separator()
            habit_name = input("  Enter the habit name: ").strip()
            result = analytics.get_longest_streak_for_habit(habits, habit_name)
            if result == -1:
                print(f"  ❌ I could not find a habit named '{habit_name}'.")
            else:
                print(f"  My longest streak for '{habit_name}' is: {result} period(s)!")
            press_enter_to_continue()

        elif choice == "5":
            # I want to see which habits I am struggling with (streak broken)
            struggling = analytics.get_struggling_habits(habits)
            clear_screen()
            print("\n  😓  HABITS I AM STRUGGLING WITH")
            print_separator()
            if not struggling:
                print("  Great job! I am not struggling with any habits right now.")
            else:
                for h in struggling:
                    print(f"  • {h.name}  ({h.periodicity})  — streak broken!")
            press_enter_to_continue()

        elif choice == "6":
            # I go back to the main menu
            break
        else:
            # The user typed something unexpected — I show an error
            print("  ⚠️  Please enter a number between 1 and 6.")
            press_enter_to_continue()


# =======================================================================
# ACTION FUNCTIONS — functions that make changes (add, check-off, delete)
# =======================================================================

def add_habit(habits: list) -> list:
    """
    I guide the user step by step to create a brand new habit.
    After creating it, I save it to the database and add it to my list.

    Args:
        habits (list): The current list of habits (I add the new one to it).

    Returns:
        list: The updated list of habits (with the new habit included).
    """

    clear_screen()
    print("\n" + "=" * 55)
    print("  ➕  ADD A NEW HABIT")
    print("=" * 55)

    # I ask the user for the habit name
    name = input("  Enter habit name (e.g. 'Drink Water'): ").strip()

    # I check that the name is not empty
    if not name:
        print("  ⚠️  Habit name cannot be empty.")
        press_enter_to_continue()
        return habits

    # I check that this habit name doesn't already exist
    if db.habit_exists(name, DB_PATH):
        print(f"  ⚠️  A habit named '{name}' already exists!")
        press_enter_to_continue()
        return habits

    # I ask the user for a short description
    description = input("  Enter a short description: ").strip()

    # I ask the user to choose daily or weekly
    print("  Periodicity — how often must this habit be done?")
    print("    1. Daily")
    print("    2. Weekly")
    period_choice = input("  Enter 1 or 2: ").strip()

    # I map the user's choice to the correct periodicity string
    if period_choice == "1":
        periodicity = "daily"
    elif period_choice == "2":
        periodicity = "weekly"
    else:
        # The user typed something invalid
        print("  ⚠️  Invalid choice. Please enter 1 or 2.")
        press_enter_to_continue()
        return habits

    # I create a new Habit object with the information the user gave me
    new_habit = Habit(name=name, description=description, periodicity=periodicity)

    # I save the new habit to the SQLite database
    db.save_habit(new_habit, DB_PATH)

    # I add the new habit to my in-memory list as well
    habits.append(new_habit)

    # I confirm success to the user
    print(f"\n  ✅  Habit '{name}' ({periodicity}) has been created successfully!")
    press_enter_to_continue()

    # I return the updated list so the caller knows about the new habit
    return habits


def checkoff_habit(habits: list) -> list:
    """
    I let the user mark a habit as done right now.
    I record the current date and time as the check-off timestamp.

    Args:
        habits (list): The current list of habits.

    Returns:
        list: The updated list (with the check-off recorded).
    """

    clear_screen()
    print("\n" + "=" * 55)
    print("  ✅  CHECK OFF A HABIT (Mark as Done)")
    print("=" * 55)

    # I show the user all their habits with a number next to each one
    if not habits:
        print("  You have no habits yet. Please add one first.")
        press_enter_to_continue()
        return habits

    for i, h in enumerate(habits, start=1):
        print(f"  [{i}] {h.name}  ({h.periodicity})")

    print_separator()

    # I ask the user to pick which habit they completed
    raw = input("  Enter the number of the habit you completed: ").strip()

    # I make sure the user typed a valid number
    try:
        index = int(raw) - 1  # I subtract 1 because lists start at 0
        if index < 0 or index >= len(habits):
            raise ValueError()  # I raise an error if the number is out of range
    except ValueError:
        print("  ⚠️  That is not a valid number.")
        press_enter_to_continue()
        return habits

    # I get the selected habit from my list
    selected_habit = habits[index]

    # I mark it as done right now (using the current timestamp)
    selected_habit.checkoff()

    # I save the updated habit (with the new check-off) to the database
    db.save_habit(selected_habit, DB_PATH)

    # I confirm success to the user and show the new streak
    print(f"\n  ✅  '{selected_habit.name}' has been checked off!")
    print(f"      Current streak: {selected_habit.get_current_streak()} period(s) in a row! 🔥")
    press_enter_to_continue()

    return habits


def delete_habit_ui(habits: list) -> list:
    """
    I let the user permanently delete a habit from the database.
    I ask for confirmation before deleting so the user doesn't
    accidentally lose data.

    Args:
        habits (list): The current list of habits.

    Returns:
        list: The updated list (with the deleted habit removed).
    """

    clear_screen()
    print("\n" + "=" * 55)
    print("  🗑️  DELETE A HABIT")
    print("=" * 55)

    # I show the list of habits so the user can choose one
    if not habits:
        print("  You have no habits to delete.")
        press_enter_to_continue()
        return habits

    for i, h in enumerate(habits, start=1):
        print(f"  [{i}] {h.name}  ({h.periodicity})")

    print_separator()

    # I ask the user which habit to delete
    raw = input("  Enter the number of the habit to delete: ").strip()

    # I validate the input
    try:
        index = int(raw) - 1
        if index < 0 or index >= len(habits):
            raise ValueError()
    except ValueError:
        print("  ⚠️  That is not a valid number.")
        press_enter_to_continue()
        return habits

    # I get the selected habit
    selected_habit = habits[index]

    # I ask the user to confirm before deleting — deleting is permanent!
    confirm = input(
        f"\n  ⚠️  Are you sure you want to delete '{selected_habit.name}'?\n"
        f"  This cannot be undone! Type 'yes' to confirm: "
    ).strip().lower()

    if confirm == "yes":
        # I delete the habit from the database permanently
        db.delete_habit(selected_habit.name, DB_PATH)

        # I also remove it from my in-memory list
        habits.pop(index)

        print(f"\n  🗑️  Habit '{selected_habit.name}' has been deleted.")
    else:
        # The user did NOT confirm — I cancel the deletion
        print("  ↩️  Deletion cancelled. The habit is still there.")

    press_enter_to_continue()
    return habits


# =======================================================================
# MAIN FUNCTION — the heart of the app that ties everything together
# =======================================================================

def main():
    """
    I am the main function. I run the whole app.
    I:
      1. Set up the database
      2. Load the 5 pre-defined habits (only on first run)
      3. Load all habits from the database
      4. Show the main menu in a loop until the user chooses to exit
    """

    # ----- Step 1: I make sure the database tables exist -----
    # (If this is the first time running, this creates the database file)
    db.setup_database(DB_PATH)

    # ----- Step 2: I load the 5 pre-defined example habits -----
    # (This only adds them if they don't already exist)
    print("\n  🌱  Loading pre-defined habits...")
    seed_data.load_predefined_habits(DB_PATH)

    # ----- Step 3: I load ALL habits from the database into memory -----
    # (This is the list I will use throughout the entire session)
    habits = db.load_all_habits(DB_PATH)

    print(f"\n  ✅  Loaded {len(habits)} habit(s) from the database.")
    input("  Press ENTER to open the main menu...")

    # ----- Step 4: I run the main menu loop -----
    # I keep showing the menu until the user chooses to exit (option 6)
    while True:
        # I display the main menu
        display_main_menu()

        # I ask the user to choose an option
        choice = input("  Enter your choice (1-6): ").strip()

        if choice == "1":
            # I show all habits to the user
            display_all_habits(habits)
            press_enter_to_continue()

        elif choice == "2":
            # I guide the user to create a new habit
            habits = add_habit(habits)

        elif choice == "3":
            # I let the user check off (complete) a habit
            habits = checkoff_habit(habits)

        elif choice == "4":
            # I let the user delete a habit
            habits = delete_habit_ui(habits)

        elif choice == "5":
            # I show the analytics sub-menu
            display_analysis_menu(habits)

        elif choice == "6":
            # I say goodbye and exit the app
            clear_screen()
            print("\n  👋  Goodbye! Keep building great habits! See you next time.\n")
            break   # I break out of the while loop — this ends the program

        else:
            # The user typed something unexpected
            print("  ⚠️  Please enter a number between 1 and 6.")
            press_enter_to_continue()


# =======================================================================
# ENTRY POINT
# This is a Python convention: I only run main() if THIS file is being
# run directly (not imported by another file).
# =======================================================================
if __name__ == "__main__":
    main()
