from flask import Flask, render_template, jsonify
from extractor import extract_crypto_data, scrape_with_selenium
from database import init_db, insert_crypto_data, get_all_crypto_data, insert_historical_price, get_historical_prices
from transformer import transform_data
from signals import generate_signal, calculate_metrics
from datetime import datetime

app = Flask(__name__)

def fetch_and_store_data():
    raw_data = extract_crypto_data()
    transformed_data = transform_data(raw_data)
    insert_crypto_data(transformed_data)
    for data in transformed_data:
        insert_historical_price(data['name'], data['actual_price'], data['timestamp'])

@app.route('/api/crypto', methods=['GET'])
def get_crypto_data():
    fetch_and_store_data()
    crypto_data = get_all_crypto_data()
    signals_data = []
    for data in crypto_data:
        historical_prices = get_historical_prices(data['name'])
        signal = generate_signal(historical_prices)
        metrics = calculate_metrics(get_historical_prices(data['name'])) # Historial de la última hora
        signals_data.append({
            'name': data['name'],
            'actual_price': data['actual_price'],
            'highest_1h': metrics['highest_1h'],
            'lower_1h': metrics['lower_1h'],
            'avg_price': metrics['avg_price'],
            'signal': signal
        })
    return jsonify(signals_data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run()