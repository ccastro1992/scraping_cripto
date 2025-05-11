from database import get_historical_prices
from datetime import datetime

def generate_signal(historical_prices):
    if not historical_prices or len(historical_prices) < 2:
        return None  # No hay suficientes datos para generar una señal

    last_price = historical_prices[0]['price']
    previous_price = historical_prices[1]['price']

    if last_price > previous_price:
        return 'B'  # Señal de compra (precio subiendo)
    elif last_price < previous_price:
        return 'S'  # Señal de venta (precio bajando)
    else:
        return None  # No hay una tendencia clara

def calculate_metrics(historical_prices):
    if not historical_prices:
        return {'highest_1h': None, 'lower_1h': None, 'avg_price': None}

    prices_last_hour = [hp['price'] for hp in historical_prices if (datetime.now() - datetime.strptime(hp['timestamp'], '%Y-%m-%d %H:%M:%S.%f')).total_seconds() <= 3600]

    if not prices_last_hour:
        return {'highest_1h': None, 'lower_1h': None, 'avg_price': None}

    highest_1h = max(prices_last_hour)
    lower_1h = min(prices_last_hour)
    avg_price = sum(prices_last_hour) / len(prices_last_hour) if prices_last_hour else None

    return {'highest_1h': highest_1h, 'lower_1h': lower_1h, 'avg_price': avg_price}