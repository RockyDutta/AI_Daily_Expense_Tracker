from tracker import ExpenseTrackerApp

def main():
    app = ExpenseTrackerApp()
    
    while True:
        print("\n===========================")
        print(" AI EXPENSE TRACKER ")
        print("===========================")
        print("1. Smart Add (Natural Language)")
        print("2. Manual Add")
        print("3. View History")
        print("4. View Insights")
        print("5. Exit")
        
        choice = input("\nSelect option: ").strip()

        if choice == '1':
            app.add_expense_smart()
        elif choice == '2':
            app.add_expense_manual()
        elif choice == '3':
            app.view_expenses()
        elif choice == '4':
            app.show_insights()
        elif choice == '5':
            print("Goodbye! Your data has been saved.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()