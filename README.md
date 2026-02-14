# 🎱 Israeli Lottery Predictor

מערכת מתקדמת לחיזוי קודים בהגרלת הלוטו הישראלי

An advanced lottery prediction application that analyzes historical Israeli Lottery results to generate data-driven predictions for future draws.

## ✨ Features

* 📊 **Data Analysis**: Analyzes historical lottery data
* 🎯 **Multiple Prediction Strategies**: 10 different algorithms including:
  * Frequency-based (Hot numbers)
  * Balanced approach (Hot & Cold numbers)
  * Overdue numbers
  * Pattern-based analysis
  * Statistical average
  * Recent trends
  * Weighted random
  * Cluster-based
  * Gap analysis
  * Mixed strategy
* 📈 **Comprehensive Statistics**: Track hot, cold, and overdue numbers
* 🌐 **Web Interface**: Beautiful, modern web UI
* 💻 **CLI Tool**: Command-line interface for quick access
* ➕ **Add New Results**: Easily update the database after each raffle
* 🗄️ **SQLite Database**: Fast, reliable data storage
* 🔄 **Auto-Updater**: Automatic result checking (requires implementation)
* 🌍 **Hebrew Support**: Full RTL and Hebrew language support

## 📋 Installation

### Prerequisites

* Python 3.7 or higher
* pip (Python package installer)

### Setup

1. **Clone or download this repository**

2. **Install Python dependencies**:

```bash
pip install -r requirements.txt
```

3. **Initialize the database with historical data**:

```bash
python database.py
```

This will import all data from `Lotto.csv` into the SQLite database.

## 🚀 Usage

### Web Interface

1. **Start the web server**:

```bash
python app.py
```

2. **Open your browser** and navigate to:

```
http://localhost:5000
```

3. **Features available in the web interface**:
   * **Home**: View recent results and statistics overview
   * **Predictions**: Generate lottery predictions using multiple strategies
   * **Statistics**: View detailed analysis of historical data
   * **History**: Browse all past lottery results with pagination
   * **Add Result**: Add new lottery results after each draw

### Command Line Interface (CLI)

Run the CLI tool:

```bash
python cli.py
```

**CLI Menu Options**:

1. Initialize/Import Database from CSV
2. Generate Predictions
3. View Statistics
4. Add New Result
5. View Recent Results
6. Exit

### Python API

You can also use the modules directly in your Python code:

```python
from database import LotteryDatabase
from predictor import LotteryPredictor

# Initialize database
db = LotteryDatabase()
db.connect()

# Add a new result
db.add_result(
    draw_number=3873,
    draw_date="02/02/2026",
    numbers=[5, 12, 18, 24, 31, 36],
    strong_number=4
)

# Generate predictions
predictor = LotteryPredictor()
predictor.connect()
predictions = predictor.generate_predictions(num_predictions=5)

for pred in predictions:
    print(f"Strategy: {pred['strategy']}")
    print(f"Numbers: {pred['numbers']}")
    print(f"Strong Number: {pred['strong_number']}")

predictor.close()
db.close()
```

## 🎲 Israeli Lottery System

The Israeli Lottery (לוטו) works as follows:

* Select **6 numbers** from 1-37
* Select **1 strong number** (המספר החזק/נוסף) from 1-7

## 📊 Prediction Strategies

### 1. Hot Numbers (Frequency-Based)
Focuses on numbers that appear most frequently in recent draws. These "hot" numbers are statistically more common in the short term.

### 2. Balanced Approach
Combines both hot (frequent) and cold (rare) numbers for a balanced selection that covers different statistical patterns.

### 3. Overdue Numbers
Targets numbers that haven't appeared recently, based on the theory that overdue numbers are "due" to appear.

### 4. Pattern-Based
Analyzes patterns in recent draws such as even/odd distribution and high/low number balance to generate predictions.

### 5. Statistical Average
Selects numbers that appear with average frequency, avoiding extremes of too hot or too cold.

### 6. Recent Trends
Analyzes the last 20 draws to identify emerging patterns and trends.

### 7. Weighted Random
Random selection weighted by historical frequency for more realistic predictions.

### 8. Cluster-Based
Distributes selections across low (1-12), mid (13-25), and high (26-37) number ranges.

### 9. Gap Analysis
Selects numbers with moderate gaps since last appearance.

### 10. Mixed Strategy
Combines multiple approaches: hot numbers, overdue numbers, and random selection.

## 🗄️ Database Schema

The application uses SQLite with the following schema:

```sql
CREATE TABLE lottery_results (
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
```

## 🔄 Automatic Updates

The app includes an auto-updater module for checking new lottery results:

### Option 1: Run Standalone Auto-Updater

**Windows:**
```bash
python auto_updater.py
```
Or double-click `run_updater.bat`

**Linux/Mac:**
```bash
python3 auto_updater.py
```
Or: `chmod +x run_updater.sh && ./run_updater.sh`

### Option 2: Run Once (Manual Check)

```bash
python auto_updater.py --once
```

This checks once and exits - useful for cron jobs or Task Scheduler.

## 🌐 API Endpoints

The web application provides REST API endpoints:

* `GET /api/predict?num=5` - Get predictions (default: 5)
* `GET /api/statistics` - Get statistics in JSON format

Example:

```bash
curl http://localhost:5000/api/predict?num=3
```

## 📁 File Structure

```
lottery-prediction/
├── Lotto.csv              # Historical lottery data
├── lottery.db             # SQLite database (created on first run)
├── database.py            # Database management module
├── predictor.py           # Prediction algorithms module
├── app.py                 # Flask web application
├── cli.py                 # Command-line interface
├── auto_updater.py        # Auto-update module
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── run_updater.bat        # Windows updater script
├── run_updater.sh         # Linux/Mac updater script
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── predict.html
│   ├── statistics.html
│   ├── history.html
│   └── add_result.html
└── static/                # Static files
    └── style.css
```

## 🛠️ Requirements

* Python 3.7+
* Flask 3.0.0
* Werkzeug 3.0.1
* requests 2.31.0
* beautifulsoup4 4.12.2

## ⚠️ Disclaimer

**Important**: This application is for entertainment and educational purposes only. Lottery results are random and cannot be predicted with certainty. Past performance does not guarantee future results. Please gamble responsibly.

## 📄 License

This project is open source and available for personal and educational use.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 💬 Support

For issues, questions, or contributions, please refer to the project repository.

---

**Good luck! 🍀**
