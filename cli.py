"""
Command-Line Interface for Israeli Lottery Predictor.
Provides a text-based menu for managing lottery data and predictions.
"""
from database import LotteryDatabase
from predictor import LotteryPredictor
import sys


def print_header():
    """Print the CLI header."""
    print("\n" + "=" * 60)
    print("🎱 Israeli Lottery Predictor - CLI")
    print("=" * 60)


def print_menu():
    """Display the main menu."""
    print("\nMain Menu:")
    print("1. Initialize/Import Database from CSV")
    print("2. Generate Predictions")
    print("3. View Statistics")
    print("4. Add New Result")
    print("5. View Recent Results")
    print("6. Exit")
    print()


def initialize_database():
    """Initialize database and import CSV data."""
    db = LotteryDatabase()
    db.connect()
    
    print("\nInitializing database...")
    count = db.import_from_csv()
    
    if count > 0:
        print(f"✓ Successfully imported {count} lottery results")
    else:
        print("✗ No data imported. Make sure Lotto.csv exists.")
    
    total = db.get_total_draws()
    print(f"Total draws in database: {total}")
    
    db.close()
    input("\nPress Enter to continue...")


def generate_predictions():
    """Generate and display lottery predictions."""
    predictor = LotteryPredictor()
    predictor.connect()
    
    print("\nHow many predictions would you like? (1-10): ", end='')
    try:
        num = int(input())
        num = min(max(num, 1), 10)
    except ValueError:
        num = 5
    
    print(f"\nGenerating {num} predictions...\n")
    predictions = predictor.generate_predictions(num)
    
    for i, pred in enumerate(predictions, 1):
        print(f"\n{'=' * 60}")
        print(f"Prediction {i}: {pred['strategy']}")
        print(f"{'=' * 60}")
        print(f"Description: {pred['description']}")
        print(f"\nNumbers: {', '.join(map(str, pred['numbers']))}")
        print(f"Strong Number: {pred['strong_number']}")
    
    predictor.close()
    input("\nPress Enter to continue...")


def view_statistics():
    """Display lottery statistics."""
    predictor = LotteryPredictor()
    predictor.connect()
    
    print("\nCalculating statistics...\n")
    stats = predictor.get_statistics()
    
    print(f"Total Draws: {stats['total_draws']}\n")
    
    print("🔥 HOT NUMBERS (Most Frequent):")
    print("-" * 40)
    for num, freq in stats['hot_numbers'][:10]:
        print(f"  Number {num:2d}: {freq:3d} times")
    
    print("\n❄️  COLD NUMBERS (Least Frequent):")
    print("-" * 40)
    for num, freq in stats['cold_numbers'][:10]:
        print(f"  Number {num:2d}: {freq:3d} times")
    
    print("\n⏰ OVERDUE NUMBERS:")
    print("-" * 40)
    for num, gap in stats['overdue_numbers'][:10]:
        print(f"  Number {num:2d}: {gap:3d} draws ago")
    
    print("\n💪 STRONG NUMBERS:")
    print("-" * 40)
    for num, freq in stats['strong_number_freq']:
        print(f"  Number {num}: {freq:3d} times")
    
    predictor.close()
    input("\nPress Enter to continue...")


def add_new_result():
    """Add a new lottery result."""
    db = LotteryDatabase()
    db.connect()
    
    latest = db.get_latest_draw_number()
    suggested = (latest + 1) if latest else 1
    
    print("\nAdd New Lottery Result")
    print("=" * 60)
    
    try:
        print(f"\nDraw Number (suggested: {suggested}): ", end='')
        draw_number = int(input())
        
        print("Draw Date (DD/MM/YYYY): ", end='')
        draw_date = input().strip()
        
        print("\nEnter the 6 winning numbers (1-37):")
        numbers = []
        for i in range(6):
            print(f"  Number {i+1}: ", end='')
            num = int(input())
            if not 1 <= num <= 37:
                print("Error: Number must be between 1 and 37")
                db.close()
                input("\nPress Enter to continue...")
                return
            numbers.append(num)
        
        if len(numbers) != len(set(numbers)):
            print("Error: All numbers must be unique")
            db.close()
            input("\nPress Enter to continue...")
            return
        
        print("\nStrong Number (1-7): ", end='')
        strong_number = int(input())
        
        if not 1 <= strong_number <= 7:
            print("Error: Strong number must be between 1 and 7")
            db.close()
            input("\nPress Enter to continue...")
            return
        
        # Add to database
        success = db.add_result(draw_number, draw_date, numbers, strong_number)
        
        if success:
            print(f"\n✓ Successfully added draw #{draw_number}")
        else:
            print(f"\n✗ Draw #{draw_number} already exists")
    
    except (ValueError, KeyError) as e:
        print(f"\n✗ Error: {str(e)}")
    
    db.close()
    input("\nPress Enter to continue...")


def view_recent_results():
    """Display recent lottery results."""
    db = LotteryDatabase()
    db.connect()
    
    print("\nHow many recent results? (1-50, default: 10): ", end='')
    try:
        limit = int(input())
        limit = min(max(limit, 1), 50)
    except ValueError:
        limit = 10
    
    results = db.get_recent_results(limit)
    
    print(f"\nShowing {len(results)} most recent results:")
    print("=" * 80)
    
    for result in results:
        numbers = [result[2], result[3], result[4], result[5], result[6], result[7]]
        numbers_str = ', '.join(f"{n:2d}" for n in numbers)
        print(f"Draw #{result[0]:4d} ({result[1]:10s}): [{numbers_str}] + {result[8]}")
    
    db.close()
    input("\nPress Enter to continue...")


def main():
    """Main CLI loop."""
    while True:
        print_header()
        print_menu()
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice == '1':
            initialize_database()
        elif choice == '2':
            generate_predictions()
        elif choice == '3':
            view_statistics()
        elif choice == '4':
            add_new_result()
        elif choice == '5':
            view_recent_results()
        elif choice == '6':
            print("\nThank you for using Israeli Lottery Predictor!")
            print("Good luck! 🍀\n")
            sys.exit(0)
        else:
            print("\n✗ Invalid option. Please try again.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting... Good luck! 🍀\n")
        sys.exit(0)
