import re
import math
from collections import defaultdict, Counter

class SmartClassifier:
    """
    A lightweight Naive Bayes Classifier implemented from scratch.
    It predicts the category of an expense based on the description.
    """
    def __init__(self):
        self.feature_counts = defaultdict(Counter)
        self.category_counts = Counter()
        self.vocab = set()
        self._seed_knowledge()

    def _seed_knowledge(self):
        """Initializes the AI with common sense logic."""
        seeds = [
            ("coffee starbucks latte espresso", "Food & Drink"),
            ("burger pizza lunch dinner restaurant mcdonalds", "Food & Drink"),
            ("uber taxi bus train gas fuel petrol", "Transportation"),
            ("netflix spotify subscription apple music hulu", "Entertainment"),
            ("movie cinema bowling game", "Entertainment"),
            ("grocery milk eggs bread walmart costco", "Groceries"),
            ("electric water bill utility internet wifi", "Utilities"),
            ("rent mortgage house", "Housing"),
            ("salary paycheck deposit income", "Income"),
            ("shirt pants clothes shoes mall shopping", "Shopping")
        ]
        for text, category in seeds:
            self.train(text, category)

    def _tokenize(self, text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        return [w for w in text.split() if len(w) > 2]

    def train(self, text, category):
        words = self._tokenize(text)
        for word in words:
            self.feature_counts[category][word] += 1
            self.vocab.add(word)
        self.category_counts[category] += 1

    def predict(self, text):
        words = self._tokenize(text)
        if not words:
            return "Uncategorized"

        best_category = None
        max_prob = -float('inf')
        total_docs = sum(self.category_counts.values())
        
        for category in self.category_counts:
            log_prob = math.log(self.category_counts[category] / total_docs)
            total_words_in_category = sum(self.feature_counts[category].values())
            vocab_size = len(self.vocab)
            
            for word in words:
                word_count = self.feature_counts[category][word]
                log_prob += math.log((word_count + 1) / (total_words_in_category + vocab_size))
            
            if log_prob > max_prob:
                max_prob = log_prob
                best_category = category

        return best_category

    def to_dict(self):
        return {
            'feature_counts': {k: dict(v) for k, v in self.feature_counts.items()},
            'category_counts': dict(self.category_counts)
        }

    def load_from_dict(self, data):
        if not data: return
        self.feature_counts = defaultdict(Counter)
        for cat, words in data.get('feature_counts', {}).items():
            self.feature_counts[cat] = Counter(words)
            self.vocab.update(words.keys())
        self.category_counts = Counter(data.get('category_counts', {}))


class NLPParser:
    """Extracts amount and description from natural language sentences."""
    @staticmethod
    def parse(sentence):
        amount_pattern = r'(?:[\£\$\€]{1}[,\d]+(?:\.\d{2})?)|(?:[,\d]+(?:\.\d{2})?(?=\s*(?:dollars|usd|eur|inr|rs)))'
        match = re.search(amount_pattern, sentence, re.IGNORECASE)
        
        amount = 0.0
        description = sentence

        if match:
            amount_str = match.group(0)
            clean_amount = re.sub(r'[^\d.]', '', amount_str)
            try:
                amount = float(clean_amount)
                description = sentence.replace(amount_str, "").strip()
                description = re.sub(r'^(spent|paid|for|on)\s+', '', description, flags=re.IGNORECASE)
                description = re.sub(r'\s+(dollars|usd|rs|inr)$', '', description, flags=re.IGNORECASE).strip()
            except ValueError:
                pass
        
        return amount, description