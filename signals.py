from datetime import datetime


def generate_signal(historical_prices):
    """
    Genera una señal de compra o venta basada en los precios históricos más recientes.

    La función compara el precio más reciente con el anterior:
        - Si el precio más reciente es mayor, retorna 'B' (señal de compra, por "Buy").
        - Si el precio más reciente es menor, retorna 'S' (señal de venta, por "Sell").
        - Si ambos son iguales, retorna None (sin tendencia clara).

    Args:
        historical_prices (list): Lista de diccionarios con datos de precios históricos
                                  en formato [{'price': float, 'timestamp': str}, ...].

    Returns:
        str or None: Una señal de compra ('B'), venta ('S') o None en caso de no existir una tendencia clara
                     o si los datos son insuficientes.
    """
    if not historical_prices or len(historical_prices) < 2:
        return None  # No hay suficientes datos para generar una señal

    last_price = historical_prices[0]['price']
    previous_price = historical_prices[1]['price']

    if last_price is None or previous_price is None:
        return None

    if last_price > previous_price:
        return 'B'  # Señal de compra (precio subiendo)
    elif last_price < previous_price:
        return 'S'  # Señal de venta (precio bajando)
    else:
        return None  # No hay una tendencia clara


def calculate_metrics(historical_prices):
    """
    Calcula métricas estadísticas (máximo, mínimo y promedio) de los precios históricos en la última hora.

    La función filtra los precios históricos para incluir solo aquellos que pertenecen a la última
    hora, y calcula las siguientes métricas:
        - El precio más alto (highest_1h).
        - El precio más bajo (lower_1h).
        - El precio promedio (avg_price).

    Args:
        historical_prices (list): Lista de diccionarios con datos de precios históricos
                                  en formato [{'price': float, 'timestamp': str}, ...].

    Returns:
        dict: Diccionario con las métricas calculadas:
                - 'highest_1h' (float o None): Precio más alto de la última hora.
                - 'lower_1h' (float o None): Precio más bajo de la última hora.
                - 'avg_price' (float o None): Precio promedio de la última hora.
    """
    if not historical_prices:
        return {'highest_1h': None, 'lower_1h': None, 'avg_price': None}

    # Filtrar precios de la última hora
    prices_last_hour = [
        hp['price'] for hp in historical_prices
        if (datetime.now() - datetime.strptime(hp['timestamp'], '%Y-%m-%d %H:%M:%S.%f')).total_seconds() <= 3600
    ]

    if not prices_last_hour:
        return {'highest_1h': None, 'lower_1h': None, 'avg_price': None}

    # Calcular métricas de la última hora
    highest_1h = max(prices_last_hour)
    lower_1h = min(prices_last_hour)
    avg_price = round(sum(prices_last_hour) / len(prices_last_hour), 4) if prices_last_hour else None

    return {
        'highest_1h': highest_1h,
        'lower_1h': lower_1h,
        'avg_price': avg_price
    }
