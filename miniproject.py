import csv
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"

# ----------- File Handling -----------
def load_expenses():
    expenses = []
    try:
        with open(FILE_NAME, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                expenses.append({
                    "amount": float(row["amount"]),
                    "category": row["category"],
                    "date": row["date"]
                })
    except FileNotFoundError:
        pass  # If no file exists yet
    return expenses

def save_expenses(expenses):
    with open(FILE_NAME, mode="w", newline="") as file:
        fieldnames = ["amount", "category", "date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)

# ----------- Add Expense -----------
def add_expense(expenses):
    try:
        amount = float(input("Enter amount: "))
        category = input("Enter category (Food, Transport, etc.): ")
        date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ")

        if date_input.strip() == "":
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            date = date_input

        expense = {"amount": amount, "category": category, "date": date}
        expenses.append(expense)
        save_expenses(expenses)
        print("Expense added successfully!")
    except ValueError:
        print("Invalid input. Please enter a number for amount.")

# ----------- View Summary -----------
def view_summary(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return

    total = sum(exp["amount"] for exp in expenses)
    print(f"\nTotal Spending: {total:.2f}")

    # By category
    category_totals = defaultdict(float)
    for exp in expenses:
        category_totals[exp["category"]] += exp["amount"]

    print("\nSpending by Category:")
    for cat, amt in category_totals.items():
        print(f"  {cat}: {amt:.2f}")

# ----------- Spending Over Time -----------
def spending_over_time(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return

    choice = input("View spending by (D)aily, (W)eekly, (M)onthly? ").lower()

    time_totals = defaultdict(float)
    for exp in expenses:
        date_obj = datetime.strptime(exp["date"], "%Y-%m-%d")
        if choice == "d":
            key = date_obj.strftime("%Y-%m-%d")
        elif choice == "w":
            year, week, _ = date_obj.isocalendar()
            key = f"{year}-W{week}"
        elif choice == "m":
            key = date_obj.strftime("%Y-%m")
        else:
            print("Invalid choice.")
            return
        time_totals[key] += exp["amount"]

    print("\nSpending Over Time:")
    for k, v in sorted(time_totals.items()):
        print(f"{k}: {v:.2f}")

# ----------- Edit/Delete Expense -----------
def manage_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return

    for i, exp in enumerate(expenses, 1):
        print(f"{i}. {exp['date']} - {exp['category']} - {exp['amount']}")

    choice = input("Enter expense number to (E)dit, (D)elete, or (Q)uit: ").lower()
    if choice == "q":
        return

    try:
        idx = int(input("Enter expense number: ")) - 1
        if idx < 0 or idx >= len(expenses):
            print("Invalid number.")
            return

        if choice == "e":
            new_amount = input("New amount (leave blank to keep): ")
            new_category = input("New category (leave blank to keep): ")
            new_date = input("New date YYYY-MM-DD (leave blank to keep): ")

            if new_amount: expenses[idx]["amount"] = float(new_amount)
            if new_category: expenses[idx]["category"] = new_category
            if new_date: expenses[idx]["date"] = new_date

            save_expenses(expenses)
            print("Expense updated successfully!")

        elif choice == "d":
            expenses.pop(idx)
            save_expenses(expenses)
            print("Expense deleted successfully!")

    except ValueError:
        print("Invalid input.")

# ----------- Graphical Summary -----------
def plot_summary(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return

    category_totals = defaultdict(float)
    for exp in expenses:
        category_totals[exp["category"]] += exp["amount"]

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Expense Distribution by Category")
    plt.show()

# ----------- Main Menu -----------
def main():
    expenses = load_expenses()
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Spending Over Time")
        print("4. Edit/Delete Expense")
        print("5. Graphical Summary")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_summary(expenses)
        elif choice == "3":
            spending_over_time(expenses)
        elif choice == "4":
            manage_expenses(expenses)
        elif choice == "5":
            plot_summary(expenses)
        elif choice == "6":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()