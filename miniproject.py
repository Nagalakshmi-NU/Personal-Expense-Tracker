import csv
from datetime import datetime
from collections import defaultdict

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
        print("✅ Expense added successfully!")
    except ValueError:
        print("❌ Invalid input. Please enter a number for amount.")

# ----------- View Summary -----------
def view_summary(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return

    total = sum(exp["amount"] for exp in expenses)
    print(f"\n💰 Total Spending: {total:.2f}")

    # By category
    category_totals = defaultdict(float)
    for exp in expenses:
        category_totals[exp["category"]] += exp["amount"]

    print("\n📊 Spending by Category:")
    for cat, amt in category_totals.items():
        print(f"  {cat}: {amt:.2f}")

# ----------- Main Menu -----------
def main():
    expenses = load_expenses()
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_summary(expenses)
        elif choice == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
