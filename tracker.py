import json
import os
from datetime import datetime
from collections import defaultdict
from ai_core import SmartClassifier, NLPParser

class ExpenseTrackerApp:
    FILE_NAME = "expense_data.json"

    def __init__(self):
        self.expenses = []
        self.classifier = SmartClassifier()
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.FILE_NAME):
            return
        try:
            with open(self.FILE_NAME, 'r') as f:
                data = json.load(f)
                self.expenses = data.get('expenses', [])
                self.classifier.load_from_dict(data.get('ai_model', {}))
        except (json.JSONDecodeError, IOError):
            print("(!) Error loading data file. Starting fresh.")

    def save_data(self):
        data = {
            'expenses': self.expenses,
            'ai_model': self.classifier.to_dict()
        }
        try:
            with open(self.FILE_NAME, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError:
            print("(!) Error saving data.")

    def add_expense_smart(self):
        print("\n--- Smart AI Entry ---")
        print("Type naturally! (e.g., 'Spent $12 on lunch at Burger King')")
        user_input = input(">> ")

        amount, desc = NLPParser.parse(user_input)

        if amount == 0:
            print("(!) Could not detect an amount. Please try manual entry.")
            return

        predicted_category = self.classifier.predict(desc)
        
        print(f"\nExtracted Amount: ${amount:.2f}")
        print(f"Extracted Desc:   {desc}")
        print(f"AI Suggestion:    [{predicted_category}]")
        
        confirm = input("Is this correct? (y/n/change category): ").strip().lower()

        final_category = predicted_category
        if confirm == 'n' or confirm == 'change':
            final_category = input("Enter correct category: ").strip().title()
            print("(+) Learning from your correction...")
            self.classifier.train(desc, final_category)
        elif confirm == 'y':
            self.classifier.train(desc, predicted_category)
        else:
            print("Cancelled.")
            return

        self._commit_expense(amount, desc, final_category)

    def add_expense_manual(self):
        print("\n--- Manual Entry ---")
        try:
            amount = float(input("Amount: "))
        except ValueError:
            print("Invalid amount.")
            return

        desc = input("Description: ").strip()
        suggestion = self.classifier.predict(desc)
        print(f"AI Suggests Category: {suggestion}")
        
        cat_input = input(f"Category (Press Enter for '{suggestion}'): ").strip()
        category = cat_input.title() if cat_input else suggestion

        self.classifier.train(desc, category)
        self._commit_expense(amount, desc, category)

    def _commit_expense(self, amount, desc, category):
        entry = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'amount': amount,
            'description': desc,
            'category': category
        }
        self.expenses.append(entry)
        self.save_data()
        print("($) Expense saved successfully!")

    def view_expenses(self):
        print("\n--- Expense History ---")
        if not self.expenses:
            print("No expenses recorded yet.")
            return

        sorted_exp = sorted(self.expenses, key=lambda x: x['date'], reverse=True)
        print(f"{'Date':<20} | {'Category':<15} | {'Amount':<10} | {'Description'}")
        print("-" * 70)
        for ex in sorted_exp:
            print(f"{ex['date']:<20} | {ex['category']:<15} | ${ex['amount']:<9.2f} | {ex['description']}")

    def show_insights(self):
        print("\n--- AI Financial Insights ---")
        if not self.expenses:
            print("Not enough data for insights.")
            return

        total_spent = sum(x['amount'] for x in self.expenses)
        cat_breakdown = defaultdict(float)
        for x in self.expenses:
            cat_breakdown[x['category']] += x['amount']

        print(f"Total Spending: ${total_spent:.2f}\n")
        print("Spending by Category:")
        
        sorted_cats = sorted(cat_breakdown.items(), key=lambda x: x[1], reverse=True)
        for cat, amt in sorted_cats:
            bar_len = int((amt / total_spent) * 20)
            bar = "█" * bar_len
            percent = (amt / total_spent) * 100
            print(f"{cat:<15} | ${amt:<9.2f} | {bar} {percent:.1f}%")

        if len(self.expenses) > 1:
            avg_expense = total_spent / len(self.expenses)
            print(f"\nAverage per transaction: ${avg_expense:.2f}")