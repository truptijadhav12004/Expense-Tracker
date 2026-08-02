
import csv

def add_expense():
    date = input("Enter Date (DD-MM-YYYY): ")
    category = input("Enter Category: ")
    description = input("Enter Description: ")
    amount = input("Enter Amount: ")

    with open("expenses.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, description, amount])

    print("Expense Added Successfully!")

def view_expenses():
    with open("expenses.csv", "r") as file:
        reader = csv.reader(file)

        print("\n------ Expense List ------")

        for row in reader:
            print(f"Date: {row[0]}")
            print(f"Category: {row[1]}")
            print(f"Description: {row[2]}")
            print(f"Amount: ₹{row[3]}")

def search_expense():
    category = input("Enter Category to Search: ")

    with open("expenses.csv", "r") as file:
        reader = csv.reader(file)

        print("\n------ Search Result ------")

        for row in reader:
            if len(row) > 1 and row[1].lower() == category.lower():
                print(row)
print("===================================")
print("      EXPENSE TRACKER SYSTEM")
print("===================================")

while True:
    print("\n1. Add Expense")
    print("2. View Expenses")
    print("3. Search Expense")
    print("4. Delete Expense")
    print("5. Exit")

    choice = input("\nEnter your choice (1-5): ")

    if choice == "1":
        add_expense()

    elif choice == "2":
         view_expenses()

    elif choice == "3":
        search_expense()

    elif choice == "4":
        print("Delete Expense Selected")

    elif choice == "5":
        print("Thank you for using Expense Tracker!")
        break

    else:
        print("Invalid Choice! Please try again.")