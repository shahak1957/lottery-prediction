"""
Prediction module for Israeli Lottery.
Implements multiple prediction strategies based on historical data analysis.
"""
import random
from typing import List, Dict
from collections import Counter
from database import LotteryDatabase


class LotteryPredictor:
    """Generates lottery predictions using various algorithms."""
    
    def __init__(self, db_file: str = "lottery.db"):
        """Initialize predictor with database connection.
        
        Args:
            db_file: Path to the SQLite database file
        """
        self.db = LotteryDatabase(db_file)
        self.MIN_NUMBER = 1
        self.MAX_NUMBER = 37
        self.MIN_STRONG = 1
        self.MAX_STRONG = 7
        self.NUMBERS_TO_PICK = 6
    
    def connect(self):
        """Connect to the database."""
        self.db.connect()
    
    def generate_predictions(self, num_predictions: int = 5) -> List[Dict]:
        """Generate multiple lottery predictions using different strategies.
        
        Args:
            num_predictions: Number of predictions to generate
            
        Returns:
            List of prediction dictionaries with strategy, numbers, and strong number
        """
        strategies = [
            self.predict_hot_numbers,
            self.predict_balanced,
            self.predict_overdue,
            self.predict_pattern_based,
            self.predict_statistical_average,
            self.predict_recent_trends,
            self.predict_random_weighted,
            self.predict_clusters,
            self.predict_gaps,
            self.predict_mixed_strategy
        ]
        
        predictions = []
        for i in range(num_predictions):
            strategy_func = strategies[i % len(strategies)]
            prediction = strategy_func()
            predictions.append(prediction)
        
        return predictions
    
    def predict_hot_numbers(self) -> Dict:
        """Predict using most frequently occurring numbers.
        
        Returns:
            Dictionary with strategy name, numbers, and strong number
        """
        frequency = self.db.get_number_frequency()
        strong_freq = self.db.get_strong_number_frequency()
        
        # Get top frequent numbers
        sorted_nums = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        hot_numbers = [num for num, _ in sorted_nums[:self.NUMBERS_TO_PICK]]
        
        # Get most frequent strong number
        strong_number = max(strong_freq.items(), key=lambda x: x[1])[0]
        
        return {
            'strategy': 'Hot Numbers (Frequency-Based)',
            'numbers': sorted(hot_numbers),
            'strong_number': strong_number,
            'description': 'Numbers that appear most frequently in recent draws'
        }
    
    def predict_balanced(self) -> Dict:
        """Predict using a balanced mix of hot and cold numbers.
        
        Returns:
            Dictionary with strategy name, numbers, and strong number
        """
        frequency = self.db.get_number_frequency()
        strong_freq = self.db.get_strong_number_frequency()
        
        sorted_nums = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        
        # Take 3 hot and 3 cold numbers
        hot_numbers = [num for num, _ in sorted_nums[:3]]
        cold_numbers = [num for num, _ in sorted_nums[-3:]]
        
        numbers = hot_numbers + cold_numbers
        
        # Balanced strong number (middle frequency)
        sorted_strong = sorted(strong_freq.items(), key=lambda x: x[1])
        strong_number = sorted_strong[len(sorted_strong) // 2][0]
        
        return {
            'strategy': 'Balanced Approach',
            'numbers': sorted(numbers),
            'strong_number': strong_number,
            'description': 'Mix of hot (frequent) and cold (rare) numbers'
        }
    
    def predict_overdue(self) -> Dict:
        """Predict using numbers that haven't appeared recently.
        
        Returns:
            Dictionary with strategy name, numbers, and strong number
        """
        last_seen = self.db.get_last_seen()
        
        # Get most overdue numbers
        sorted_nums = sorted(last_seen.items(), key=lambda x: x[1], reverse=True)
        overdue_numbers = [num for num, _ in sorted_nums[:self.NUMBERS_TO_PICK]]
        
        # Random strong number (overdue concept less applicable to 1-7 range)
        strong_number = random.randint(self.MIN_STRONG, self.MAX_STRONG)
        
        return {
            'strategy': 'Overdue Numbers',
            'numbers': sorted(overdue_numbers),
            'strong_number': strong_number,
            'description': 'Numbers that have not appeared recently'
        }
    
    def predict_pattern_based(self) -> Dict:
        """Predict based on even/odd and high/low patterns.
        
        Returns:
            Dictionary with strategy name, numbers, and strong number
        """
        # Aim for balanced even/odd and high/low distribution
        numbers = []
        
        # Pick 3 even and 3 odd numbers
        evens = [n for n in range(2, self.MAX_NUMBER + 1, 2)]
        odds = [n for n in range(1, self.MAX_NUMBER + 1, 2)]
        
        random.shuffle(evens)
        random.shuffle(odds)
        
        numbers.extend(evens[:3])
        numbers.extend(odds[:3])
        
        # Ensure we have exactly 6 unique numbers
        numbers = list(set(numbers))
        while len(numbers) < self.NUMBERS_TO_PICK:
            num = random.randint(self.MIN_NUMBER, self.MAX_NUMBER)
            if num not in numbers:
                numbers.append(num)
        
        strong_number = random.randint(self.MIN_STRONG, self.MAX_STRONG)
        
        return {
            'strategy': 'Pattern-Based',
            'numbers': sorted(numbers[:self.NUMBERS_TO_PICK]),
            'strong_number': strong_number,
            'description': 'Balanced even/odd and high/low distribution'
        }
    
    def predict_statistical_average(self) -> Dict:
        """Predict using numbers with average frequency.
        
        Returns:
            Dictionary with strategy name, numbers, and strong number
        """
        frequency = self.db.get_number_frequency()
        strong_freq = self.db.get_strong_number_frequency()
        
        # Calculate average frequency
        avg_freq = sum(frequency.values()) / len(frequency)
        
        # Find numbers closest to average
        avg_numbers = sorted(
            frequency.items(),
            key=lambda x: abs(x[1] - avg_freq)
        )[:self.NUMBERS_TO_PICK]
        
        numbers = [num for num, _ in avg_numbers]
        
        # Average strong number
        avg_strong_freq = sum(strong_freq.values()) / len(strong_freq)
        strong_number = min(
            strong_freq.items(),
            key=lambda x: abs(x[1] - avg_strong_freq)
        )[0]
        
        return {
            'strategy': 'Statistical Average',
            'numbers': sorted(numbers),
            'strong_number': strong_number,
            'description': 'Numbers with average frequency'
        }
    
    def predict_recent_trends(self) -> Dict:
        """Predict based on numbers appearing in recent draws.
        
        Returns:
            Dictionary with strategy name, numbers, and strong number
        """
        recent = self.db.get_recent_results(20)
        
        # Count occurrences in recent draws
        recent_counter = Counter()
        strong_counter = Counter()
        
        for result in recent:
            for num in result[2:8]:  # The 6 numbers
                recent_counter[num] += 1
            strong_counter[result[8]] += 1  # Strong number
        
        # Get most common in recent draws
        common_numbers = [num for num, _ in recent_counter.most_common(self.NUMBERS_TO_PICK)]
        
        # Fill with random if not enough
        while len(common_numbers) < self.NUMBERS_TO_PICK:
            num = random.randint(self.MIN_NUMBER, self.MAX_NUMBER)
            if num not in common_numbers:
                common_numbers.append(num)
        
        strong_number = strong_counter.most_common(1)[0][0] if strong_counter else random.randint(self.MIN_STRONG, self.MAX_STRONG)
        
        return {
            'strategy': 'Recent Trends',
            'numbers': sorted(common_numbers),
            'strong_number': strong_number,
            'description': 'Based on patterns in the last 20 draws'
        }
    
    def predict_random_weighted(self) -> Dict:
        """Predict using weighted random selection based on frequency.
        
        Returns:
            Dictionary with strategy name, numbers, and strong number
        """
        frequency = self.db.get_number_frequency()
        strong_freq = self.db.get_strong_number_frequency()
        
        # Create weighted list
        numbers = []
        for num, freq in frequency.items():
            # Weight: use frequency as probability weight
            weight = max(1, freq)
            numbers.extend([num] * weight)
        
        # Random selection with weights
        selected = []
        random.shuffle(numbers)
        for num in numbers:
            if num not in selected:
                selected.append(num)
            if len(selected) == self.NUMBERS_TO_PICK:
                break
        
        # Weighted strong number
        strong_list = []
        for num, freq in strong_freq.items():
            weight = max(1, freq)
            strong_list.extend([num] * weight)
        strong_number = random.choice(strong_list)
        
        return {
            'strategy': 'Weighted Random',
            'numbers': sorted(selected),
            'strong_number': strong_number,
            'description': 'Random selection weighted by historical frequency'
        }
    
    def predict_clusters(self) -> Dict:
        """Predict using number clusters/groups.
        
        Returns:
            Dictionary with strategy name, numbers, and strong number
        """
        # Divide into clusters: low (1-12), mid (13-25), high (26-37)
        clusters = [
            list(range(1, 13)),
            list(range(13, 26)),
            list(range(26, 38))
        ]
        
        # Pick 2 from each cluster
        numbers = []
        for cluster in clusters:
            random.shuffle(cluster)
            numbers.extend(cluster[:2])
        
        strong_number = random.randint(self.MIN_STRONG, self.MAX_STRONG)
        
        return {
            'strategy': 'Cluster-Based',
            'numbers': sorted(numbers),
            'strong_number': strong_number,
            'description': 'Distributed selection across low, mid, and high number ranges'
        }
    
    def predict_gaps(self) -> Dict:
        """Predict using analysis of gaps between consecutive draws.
        
        Returns:
            Dictionary with strategy name, numbers, and strong number
        """
        last_seen = self.db.get_last_seen()
        
        # Pick numbers with moderate gaps (not too recent, not too old)
        sorted_gaps = sorted(last_seen.items(), key=lambda x: x[1])
        
        # Take numbers from the middle of the gap distribution
        start = len(sorted_gaps) // 3
        end = start + self.NUMBERS_TO_PICK
        numbers = [num for num, _ in sorted_gaps[start:end]]
        
        strong_number = random.randint(self.MIN_STRONG, self.MAX_STRONG)
        
        return {
            'strategy': 'Gap Analysis',
            'numbers': sorted(numbers),
            'strong_number': strong_number,
            'description': 'Numbers with moderate gaps since last appearance'
        }
    
    def predict_mixed_strategy(self) -> Dict:
        """Predict using a mix of multiple strategies.
        
        Returns:
            Dictionary with strategy name, numbers, and strong number
        """
        frequency = self.db.get_number_frequency()
        last_seen = self.db.get_last_seen()
        
        sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        sorted_gaps = sorted(last_seen.items(), key=lambda x: x[1], reverse=True)
        
        numbers = []
        # 2 hot numbers
        numbers.extend([num for num, _ in sorted_freq[:2]])
        # 2 overdue numbers
        numbers.extend([num for num, _ in sorted_gaps[:2]])
        # 2 random numbers
        while len(numbers) < self.NUMBERS_TO_PICK:
            num = random.randint(self.MIN_NUMBER, self.MAX_NUMBER)
            if num not in numbers:
                numbers.append(num)
        
        strong_number = random.randint(self.MIN_STRONG, self.MAX_STRONG)
        
        return {
            'strategy': 'Mixed Strategy',
            'numbers': sorted(numbers[:self.NUMBERS_TO_PICK]),
            'strong_number': strong_number,
            'description': 'Combination of hot, overdue, and random numbers'
        }
    
    def get_statistics(self) -> Dict:
        """Get comprehensive statistics about lottery numbers.
        
        Returns:
            Dictionary containing various statistics
        """
        frequency = self.db.get_number_frequency()
        strong_freq = self.db.get_strong_number_frequency()
        last_seen = self.db.get_last_seen()
        total_draws = self.db.get_total_draws()
        
        # Find hot and cold numbers
        sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        hot_numbers = sorted_freq[:10]
        cold_numbers = sorted_freq[-10:]
        
        # Find overdue numbers
        sorted_gaps = sorted(last_seen.items(), key=lambda x: x[1], reverse=True)
        overdue_numbers = sorted_gaps[:10]
        
        return {
            'total_draws': total_draws,
            'hot_numbers': hot_numbers,
            'cold_numbers': cold_numbers,
            'overdue_numbers': overdue_numbers,
            'strong_number_freq': sorted(strong_freq.items(), key=lambda x: x[1], reverse=True)
        }
    
    def close(self):
        """Close database connection."""
        self.db.close()


if __name__ == "__main__":
    # Test predictions
    predictor = LotteryPredictor()
    predictor.connect()
    
    print("Generating lottery predictions...\n")
    predictions = predictor.generate_predictions(5)
    
    for i, pred in enumerate(predictions, 1):
        print(f"Prediction {i}: {pred['strategy']}")
        print(f"Numbers: {pred['numbers']}")
        print(f"Strong Number: {pred['strong_number']}")
        print(f"Description: {pred['description']}")
        print()
    
    predictor.close()
