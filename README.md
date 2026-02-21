AI-Powered Expense Tracker
An intelligent, console-based financial management system that leverages Natural Language Processing (NLP) and Machine Learning to categorize spending habits. Unlike traditional trackers, this application "learns" from user behavior and understands human-like sentences.

Key Features :-
•	Natural Language Entry: Don't fill out forms. Just type: "Spent $45 on petrol at Shell station" or "Paid 12.50 for a delicious latte".
•	Self-Learning Classifier: Built on a custom Naive Bayes algorithm. If you correct the AI, it updates its probability weights in real-time to better understand your specific habits.
•	Smart Insights: Dynamic spending breakdown with visual bars and percentage distributions.
•	 Persistent Memory: Automatically serializes both your financial data and the AI's "brain" state into a JSON-based local database.
•	Robust Error Handling: Debugged NLP parser that intelligently separates currency symbols, amounts, and descriptions.

Technical Architecture :-
The project follows a modular design pattern for clean, maintainable, and scalable code:
1.	ai_core.py: The engine. Contains the SmartClassifier (Probability Math) and NLPParser (Regex-based extraction).
2.	tracker.py: The controller. Manages state, handles CRUD operations, and performs data serialization.
3.	main.py: The interface. A clean, interactive CLI loop for user interaction.
   
Installation & Usage :-
1.	Clone the repository:
2.	git clone [https://github.com/yourusername/ai-expense-tracker.git](https://github.com/yourusername/ai-expense-tracker.git)
3.	cd ai-expense-tracker
4.	Run the application: (No external dependencies required!)
5.	python main.py
   
How the AI Works :-
This project implements a Multinomial Naive Bayes classifier from scratch.
•	Tokenization: Descriptions are stripped of "noise" (stop-words like the, for, with) to focus on meaningful keywords.
•	Laplace Smoothing: Ensures that the AI doesn't break when encountering a word it hasn't seen before.
•	Probability Weights:
$$P(Category | Word) \propto P(Category) \cdot \prod P(Word | Category)$$
The model calculates the likelihood of an expense belonging to a category based on your historical data.

Contributing :-
Contributions are what make the open-source community such an amazing place to learn, inspire, and create.
1.	Fork the Project
2.	Create your Feature Branch (git checkout -b feature/AmazingFeature)
3.	Commit your Changes (git commit -m 'Add some AmazingFeature')
4.	Push to the Branch (git push origin feature/AmazingFeature)
5.	Open a Pull Request

