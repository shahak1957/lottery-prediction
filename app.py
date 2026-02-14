"""
Flask web application for Israeli Lottery Predictor.
Provides a web interface for predictions, statistics, and result management.
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from database import LotteryDatabase
from predictor import LotteryPredictor
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'lottery_prediction_secret_key_2026'


@app.route('/')
def index():
    """Home page showing recent results and quick stats."""
    db = LotteryDatabase()
    db.connect()
    
    recent_results = db.get_recent_results(10)
    total_draws = db.get_total_draws()
    latest_draw = db.get_latest_draw_number()
    
    db.close()
    
    return render_template('index.html', 
                         recent_results=recent_results,
                         total_draws=total_draws,
                         latest_draw=latest_draw)


@app.route('/predict')
def predict():
    """Predictions page showing multiple prediction strategies."""
    num_predictions = request.args.get('num', default=5, type=int)
    num_predictions = min(max(num_predictions, 1), 10)  # Limit between 1-10
    
    predictor = LotteryPredictor()
    predictor.connect()
    
    predictions = predictor.generate_predictions(num_predictions)
    
    predictor.close()
    
    return render_template('predict.html', predictions=predictions)


@app.route('/statistics')
def statistics():
    """Statistics page showing comprehensive data analysis."""
    predictor = LotteryPredictor()
    predictor.connect()
    
    stats = predictor.get_statistics()
    
    predictor.close()
    
    return render_template('statistics.html', stats=stats)


@app.route('/history')
def history():
    """History page showing all past lottery results."""
    page = request.args.get('page', default=1, type=int)
    per_page = 50
    
    db = LotteryDatabase()
    db.connect()
    
    all_results = db.get_all_results()
    total_results = len(all_results)
    
    # Calculate pagination
    total_pages = (total_results + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    page_results = all_results[start_idx:end_idx]
    
    db.close()
    
    return render_template('history.html', 
                         results=page_results,
                         page=page,
                         total_pages=total_pages,
                         total_results=total_results)


@app.route('/add_result', methods=['GET', 'POST'])
def add_result():
    """Page for adding new lottery results."""
    if request.method == 'POST':
        try:
            draw_number = int(request.form['draw_number'])
            draw_date = request.form['draw_date']
            
            numbers = [
                int(request.form['number1']),
                int(request.form['number2']),
                int(request.form['number3']),
                int(request.form['number4']),
                int(request.form['number5']),
                int(request.form['number6'])
            ]
            
            strong_number = int(request.form['strong_number'])
            
            # Validate numbers
            if not all(1 <= n <= 37 for n in numbers):
                flash('All numbers must be between 1 and 37', 'error')
                return redirect(url_for('add_result'))
            
            if not 1 <= strong_number <= 7:
                flash('Strong number must be between 1 and 7', 'error')
                return redirect(url_for('add_result'))
            
            if len(numbers) != len(set(numbers)):
                flash('All numbers must be unique', 'error')
                return redirect(url_for('add_result'))
            
            # Add to database
            db = LotteryDatabase()
            db.connect()
            
            # Convert date format (YYYY-MM-DD to DD/MM/YYYY)
            date_parts = draw_date.split('-')
            formatted_date = f"{date_parts[2]}/{date_parts[1]}/{date_parts[0]}"
            
            success = db.add_result(draw_number, formatted_date, numbers, strong_number)
            
            db.close()
            
            if success:
                flash(f'Successfully added draw #{draw_number}', 'success')
                return redirect(url_for('index'))
            else:
                flash(f'Draw #{draw_number} already exists in the database', 'error')
                return redirect(url_for('add_result'))
                
        except (ValueError, KeyError) as e:
            flash(f'Invalid input: {str(e)}', 'error')
            return redirect(url_for('add_result'))
    
    # GET request - show form
    db = LotteryDatabase()
    db.connect()
    latest_draw = db.get_latest_draw_number()
    db.close()
    
    suggested_draw = (latest_draw + 1) if latest_draw else 1
    today = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('add_result.html', 
                         suggested_draw=suggested_draw,
                         today=today)


@app.route('/api/predict')
def api_predict():
    """API endpoint for predictions."""
    num = request.args.get('num', default=5, type=int)
    num = min(max(num, 1), 10)
    
    predictor = LotteryPredictor()
    predictor.connect()
    
    predictions = predictor.generate_predictions(num)
    
    predictor.close()
    
    return jsonify(predictions)


@app.route('/api/statistics')
def api_statistics():
    """API endpoint for statistics."""
    predictor = LotteryPredictor()
    predictor.connect()
    
    stats = predictor.get_statistics()
    
    predictor.close()
    
    # Convert to JSON-serializable format
    result = {
        'total_draws': stats['total_draws'],
        'hot_numbers': [{'number': num, 'frequency': freq} for num, freq in stats['hot_numbers']],
        'cold_numbers': [{'number': num, 'frequency': freq} for num, freq in stats['cold_numbers']],
        'overdue_numbers': [{'number': num, 'draws_ago': gap} for num, gap in stats['overdue_numbers']],
        'strong_number_freq': [{'number': num, 'frequency': freq} for num, freq in stats['strong_number_freq']]
    }
    
    return jsonify(result)


if __name__ == '__main__':
    # Initialize database if needed
    db = LotteryDatabase()
    db.connect()
    
    # Try to import data if database is empty
    if db.get_total_draws() == 0:
        print("Database is empty. Importing data from CSV...")
        count = db.import_from_csv()
        if count > 0:
            print(f"Imported {count} lottery results")
        else:
            print("No CSV file found. Database will be empty.")
    
    db.close()
    
    print("Starting Flask web server...")
    print("Open your browser and navigate to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
