"""
Database module for managing Israeli Lottery results.
Handles all database operations including initialization, adding results, and queries.
"""
import sqlite3
import csv
from datetime import datetime
from typing import List, Tuple, Optional


class LotteryDatabase:
    """Manages the lottery database operations."""
    
    def __init__(self, db_file: str = "lottery.db"):
        """Initialize database connection.
        
        Args:
            db_file: Path to the SQLite database file
        """
        self.db_file = db_file
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to the database and create tables if needed."""
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create the lottery_results table if it doesn't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS lottery_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                draw_number INTEGER UNIQUE NOT NULL,
                draw_date DATE NOT NULL,
                number1 INTEGER NOT NULL,
                number2 INTEGER NOT NULL,
                number3 INTEGER NOT NULL,
                number4 INTEGER NOT NULL,
                number5 INTEGER NOT NULL,
                number6 INTEGER NOT NULL,
                strong_number INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def import_from_csv(self, csv_file: str = "Lotto.csv") -> int:
        """Import lottery results from a CSV file.
        
        Args:
            csv_file: Path to the CSV file containing lottery data
            
        Returns:
            Number of records imported
        """
        count = 0
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        # Extract numbers from the row
                        numbers = [
                            int(row['number1']),
                            int(row['number2']),
                            int(row['number3']),
                            int(row['number4']),
                            int(row['number5']),
                            int(row['number6'])
                        ]
                        
                        self.add_result(
                            draw_number=int(row['draw_number']),
                            draw_date=row['draw_date'],
                            numbers=numbers,
                            strong_number=int(row['strong_number'])
                        )
                        count += 1
                    except (ValueError, KeyError, sqlite3.IntegrityError) as e:
                        # Skip invalid rows or duplicates
                        continue
        except FileNotFoundError:
            print(f"CSV file '{csv_file}' not found. Creating empty database.")
        
        return count
    
    def add_result(self, draw_number: int, draw_date: str, 
                   numbers: List[int], strong_number: int) -> bool:
        """Add a new lottery result to the database.
        
        Args:
            draw_number: The draw/raffle number
            draw_date: Date of the draw (DD/MM/YYYY format)
            numbers: List of 6 winning numbers
            strong_number: The strong/bonus number
            
        Returns:
            True if successful, False otherwise
        """
        if len(numbers) != 6:
            raise ValueError("Must provide exactly 6 numbers")
        
        try:
            # Convert date format if needed (DD/MM/YYYY to YYYY-MM-DD)
            if '/' in draw_date:
                parts = draw_date.split('/')
                draw_date = f"{parts[2]}-{parts[1]}-{parts[0]}"
            
            self.cursor.execute("""
                INSERT INTO lottery_results 
                (draw_number, draw_date, number1, number2, number3, 
                 number4, number5, number6, strong_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (draw_number, draw_date, *numbers, strong_number))
            
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Draw number already exists
            return False
    
    def get_all_results(self) -> List[Tuple]:
        """Get all lottery results ordered by draw number descending.
        
        Returns:
            List of tuples containing all lottery results
        """
        self.cursor.execute("""
            SELECT draw_number, draw_date, number1, number2, number3,
                   number4, number5, number6, strong_number
            FROM lottery_results
            ORDER BY draw_number DESC
        """)
        return self.cursor.fetchall()
    
    def get_recent_results(self, limit: int = 10) -> List[Tuple]:
        """Get the most recent lottery results.
        
        Args:
            limit: Number of recent results to retrieve
            
        Returns:
            List of tuples containing recent lottery results
        """
        self.cursor.execute("""
            SELECT draw_number, draw_date, number1, number2, number3,
                   number4, number5, number6, strong_number
            FROM lottery_results
            ORDER BY draw_number DESC
            LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()
    
    def get_latest_draw_number(self) -> Optional[int]:
        """Get the latest draw number in the database.
        
        Returns:
            Latest draw number or None if database is empty
        """
        self.cursor.execute("SELECT MAX(draw_number) FROM lottery_results")
        result = self.cursor.fetchone()
        return result[0] if result[0] is not None else None
    
    def get_number_frequency(self) -> dict:
        """Calculate frequency of each number in all draws.
        
        Returns:
            Dictionary mapping number to frequency count
        """
        frequency = {i: 0 for i in range(1, 38)}
        
        results = self.get_all_results()
        for result in results:
            # result[2:8] contains the 6 numbers
            for num in result[2:8]:
                frequency[num] = frequency.get(num, 0) + 1
        
        return frequency
    
    def get_strong_number_frequency(self) -> dict:
        """Calculate frequency of strong numbers.
        
        Returns:
            Dictionary mapping strong number to frequency count
        """
        frequency = {i: 0 for i in range(1, 8)}
        
        self.cursor.execute("SELECT strong_number FROM lottery_results")
        results = self.cursor.fetchall()
        
        for result in results:
            strong_num = result[0]
            frequency[strong_num] = frequency.get(strong_num, 0) + 1
        
        return frequency
    
    def get_last_seen(self) -> dict:
        """Calculate how many draws ago each number was last seen.
        
        Returns:
            Dictionary mapping number to draws since last appearance
        """
        last_seen = {i: 0 for i in range(1, 38)}
        
        results = self.get_all_results()  # Already sorted by draw_number DESC
        
        for draw_index, result in enumerate(results):
            for num in result[2:8]:  # The 6 numbers
                if last_seen[num] == 0:
                    last_seen[num] = draw_index
        
        # For numbers never seen, set to total number of draws
        total_draws = len(results)
        for num in last_seen:
            if last_seen[num] == 0:
                last_seen[num] = total_draws
        
        return last_seen
    
    def get_total_draws(self) -> int:
        """Get total number of draws in database.
        
        Returns:
            Total number of lottery draws
        """
        self.cursor.execute("SELECT COUNT(*) FROM lottery_results")
        return self.cursor.fetchone()[0]
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Initialize and import data
    db = LotteryDatabase()
    db.connect()
    
    print("Importing lottery data from CSV...")
    count = db.import_from_csv()
    print(f"Imported {count} lottery results")
    
    # Display some statistics
    total = db.get_total_draws()
    print(f"Total draws in database: {total}")
    
    if total > 0:
        print("\nMost recent results:")
        recent = db.get_recent_results(5)
        for result in recent:
            print(f"Draw #{result[0]} ({result[1]}): "
                  f"{result[2]}, {result[3]}, {result[4]}, "
                  f"{result[5]}, {result[6]}, {result[7]} + {result[8]}")
    
    db.close()
