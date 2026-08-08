"""
EXPENSE TRACKER (Python)
-------------------------
A command-line expense tracker that lets you add, view, and analyze
expenses by category, with data persisted to a JSON file.

Run:  python expense_tracker.py
"""

import json
import os
from datetime import date

DATA_FILE = "expenses.json"


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(expenses):
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    category = input("Category (e.g. Food, Travel, Books): ").strip().title()
    note = input("Note (optional): ").strip()

    entry = {
        "date": str(date.today()),
        "amount": amount,
        "category": category,
        "note": note,
    }
    expenses.append(entry)
    save_expenses(expenses)
    print(f"Added: {amount} under '{category}'.")


def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"\n{'Date':<12}{'Category':<15}{'Amount':<10}Note")
    print("-" * 55)
    for e in expenses:
        print(f"{e['date']:<12}{e['category']:<15}{e['amount']:<10}{e['note']}")


def view_by_category(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return

    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]

    print("\n--- Totals by Category ---")
    for category, total in sorted(totals.items(), key=lambda x: -x[1]):
        print(f"{category:<15} {total:.2f}")

    grand_total = sum(totals.values())
    print("-" * 25)
    print(f"{'TOTAL':<15} {grand_total:.2f}")


def delete_expense(expenses):
    view_expenses(expenses)
    if not expenses:
        return
    try:
        index = int(input("\nEnter the row number to delete (1-based): ")) - 1
        if 0 <= index < len(expenses):
            removed = expenses.pop(index)
            save_expenses(expenses)
            print(f"Deleted: {removed}")
        else:
            print("Invalid index.")
    except ValueError:
        print("Please enter a valid number.")


def main():
    expenses = load_expenses()

    menu = """
===== EXPENSE TRACKER =====
1. Add Expense
2. View All Expenses
3. View Totals by Category
4. Delete an Expense
5. Exit
"""
    while True:
        print(menu)
        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            view_by_category(expenses)
        elif choice == "4":
            delete_expense(expenses)
        elif choice == "5":
            print("Goodbye! Your data is saved in expenses.json.")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
