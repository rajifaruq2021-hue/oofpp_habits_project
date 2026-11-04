"""
main.py

I am the main entry point for the Habit Tracker App.
I show a simple numbered menu that the user can navigate
by typing a number and pressing Enter.

When the user runs: python main.py
This file starts and shows the main menu.

Menu options:
    1. View all habits
    2. Add a new habit
    3. Check off a habit (mark it as done)
    4. Delete a habit
    5. Analyse habits
    6. Exit
"""

# I import the os module so I can clear the screen to keep the menu tidy
import os

# I import datetime so I can show the current date and time to the user
from datetime import datetime

# I import my own modules
import db           # handles saving and loading from the database
import analytics    # provides all the analysis functions
import seed_data    # loads the 5 pre-defined example habits
from habit import Habit   # the Habit class I defined in habit.py


def clear_screen():
    """
    I clear the terminal screen so the menu looks clean each time.
    This works on both Windows and Linux/Mac.
    """
    os.system("cls" if os.name == "nt" else "clear")


def show_header():
    """
    I print a simple header at the top of every menu page.
    """
    print("=" * 50)
    print("      HABIT TRACKER APP")
    print(f"      {datetime.now().strftime('%Y-%m-%d  %H:%M')}")
    print("=" * 50)
    print()


def list_habits(habits):
    """
    I show a numbered list of all habits with their current streaks.

    Args:
        habits (list): the list of Habit objects to display.
    """

    if not habits:
        print("You have no habits yet. Add one first.")
        return

    print(f"{'No.':<5} {'Name':<22} {'Type':<10} {'Streak':<8} {'Best'}")
    print("-" * 55)
    for i, h in enumerate(habits, 1):
        current = h.get_current_streak()
        best    = h.get_longest_streak()
        print(f"{i:<5} {h.name:<22} {h.periodicity:<10} {current:<8} {best}")
    print()


def view_all_habits(habits):
    """
    I show all habits on the screen and wait for the user to press Enter.
    """
    clear_screen()
    show_header()
    print("All habits:")
    print()
    list_habits(habits)
    input("Press Enter to go back to the menu.")


def add_new_habit(habits):
    """
    I ask the user for a name, description, and type,
    then create a new Habit and save it to the database.

    Args:
        habits (list): the current list of habits (I add to this list).
    """
    clear_screen()
    show_header()
    print("Add a New Habit")
    print("-" * 30)

    name = input("Habit name: ").strip()
    if not name:
        print("Name cannot be empty.")
        input("Press Enter to go back.")
        return

    # I check if a habit with this name already exists
    if any(h.name.lower() == name.lower() for h in habits):
        print(f"A habit called '{name}' already exists.")
        input("Press Enter to go back.")
        return

    description = input("Short description: ").strip()

    # I ask for the type and keep asking until the user gives a valid answer
    while True:
        periodicity = input("Type (daily / weekly): ").strip().lower()
        if periodicity in ("daily", "weekly"):
            break
        print("Please type 'daily' or 'weekly'.")

    # I create and save the new habit
    new_habit = Habit(name=name, description=description, periodicity=periodicity)
    habits.append(new_habit)
    db.save_habit(new_habit)

    print(f"Habit '{name}' has been added.")
    input("Press Enter to go back to the menu.")


def checkoff_habit(habits):
    """
    I let the user pick a habit and mark it as done right now.

    Args:
        habits (list): the list of all habits.
    """
    clear_screen()
    show_header()
    print("Check Off a Habit")
    print("-" * 30)
    list_habits(habits)

    if not habits:
        input("Press Enter to go back.")
        return

    try:
        choice = int(input("Enter the habit number to check off: "))
        if choice < 1 or choice > len(habits):
            print("That number is not in the list.")
            input("Press Enter to go back.")
            return
    except ValueError:
        print("Please enter a number.")
        input("Press Enter to go back.")
        return

    # I mark the chosen habit as done and save it
    habit = habits[choice - 1]
    habit.checkoff()
    db.save_habit(habit)

    print(f"Well done! '{habit.name}' has been checked off.")
    input("Press Enter to go back to the menu.")


def delete_habit_menu(habits):
    """
    I let the user pick a habit and delete it after confirming.

    Args:
        habits (list): the list of all habits.
    """
    clear_screen()
    show_header()
    print("Delete a Habit")
    print("-" * 30)
    list_habits(habits)

    if not habits:
        input("Press Enter to go back.")
        return

    try:
        choice = int(input("Enter the habit number to delete: "))
        if choice < 1 or choice > len(habits):
            print("That number is not in the list.")
            input("Press Enter to go back.")
            return
    except ValueError:
        print("Please enter a number.")
        input("Press Enter to go back.")
        return

    habit = habits[choice - 1]

    # I ask the user to confirm before deleting
    confirm = input(f"Are you sure you want to delete '{habit.name}'? (yes / no): ").strip().lower()
    if confirm == "yes":
        db.delete_habit(habit.name)
        habits.remove(habit)
        print(f"'{habit.name}' has been deleted.")
    else:
        print("Deletion cancelled.")

    input("Press Enter to go back to the menu.")


def analyse_habits_menu(habits):
    """
    I show a small sub-menu with five analysis options the user can choose from.

    Args:
        habits (list): the list of all habits.
    """

    while True:
        clear_screen()
        show_header()
        print("Analyse Habits")
        print("-" * 30)
        print("1. Show all habits")
        print("2. Show only daily habits")
        print("3. Show only weekly habits")
        print("4. Show the longest streak across all habits")
        print("5. Show the longest streak for one habit")
        print("6. Back to main menu")
        print()

        choice = input("Pick an option (1-6): ").strip()

        if choice == "1":
            # I show all habits with their streaks
            clear_screen()
            show_header()
            print("All habits:")
            print()
            list_habits(analytics.get_all_habits(habits))
            input("Press Enter to continue.")

        elif choice == "2":
            # I show only daily habits
            clear_screen()
            show_header()
            print("Daily habits:")
            print()
            list_habits(analytics.get_habits_by_periodicity(habits, "daily"))
            input("Press Enter to continue.")

        elif choice == "3":
            # I show only weekly habits
            clear_screen()
            show_header()
            print("Weekly habits:")
            print()
            list_habits(analytics.get_habits_by_periodicity(habits, "weekly"))
            input("Press Enter to continue.")

        elif choice == "4":
            # I show the best streak across all habits
            clear_screen()
            show_header()
            best = analytics.get_longest_streak_all(habits)
            print(f"The longest streak across all habits is: {best} period(s)")
            print()
            input("Press Enter to continue.")

        elif choice == "5":
            # I ask for a habit name and show its best streak
            clear_screen()
            show_header()
            list_habits(habits)
            name = input("Enter the habit name: ").strip()
            result = analytics.get_longest_streak_for_habit(habits, name)
            if result == -1:
                print(f"No habit called '{name}' was found.")
            else:
                print(f"The longest streak for '{name}' is: {result} period(s)")
            input("Press Enter to continue.")

        elif choice == "6":
            # I go back to the main menu
            break

        else:
            print("Please pick a number between 1 and 6.")
            input("Press Enter to try again.")


def main():
    """
    I am the main function that starts the app.
    I set up the database, load habits, and show the menu in a loop.
    """

    # I set up the database tables if they do not exist yet
    db.setup_database()

    # I load all saved habits from the database
    habits = db.load_all_habits()

    # I load the example habits only if the database is empty
    if not habits:
        print("Loading example habits for the first time.")
        seed_data.load_predefined_habits()
        habits = db.load_all_habits()

    # I keep showing the menu until the user picks Exit
    while True:
        clear_screen()
        show_header()
        print("What would you like to do?")
        print()
        print("1. View all habits")
        print("2. Add a new habit")
        print("3. Check off a habit")
        print("4. Delete a habit")
        print("5. Analyse habits")
        print("6. Exit")
        print()

        choice = input("Pick an option (1-6): ").strip()

        if choice == "1":
            view_all_habits(habits)
        elif choice == "2":
            add_new_habit(habits)
        elif choice == "3":
            checkoff_habit(habits)
        elif choice == "4":
            delete_habit_menu(habits)
        elif choice == "5":
            analyse_habits_menu(habits)
        elif choice == "6":
            print("Goodbye! Keep up your good habits.")
            break
        else:
            print("Please pick a number between 1 and 6.")
            input("Press Enter to try again.")


# I call main() only when this file is run directly
if __name__ == "__main__":
    main()
