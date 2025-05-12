from flask import Flask, render_template, jsonify

from database import init_db, insert_crypto_data, get_all_crypto_data, insert_historical_price, get_historical_prices
from extractor import extract_crypto_data
from signals import generate_signal, calculate_metrics
from transformer import transform_data

app = Flask(__name__)


def fetch_and_store_data():
    """
    Extrae los datos de criptomonedas, los transforma y los almacena en la base de datos.

    Este proceso incluye:
        - Extraer los datos crudos de criptomonedas.
        - Transformar los datos crudos a un formato estructurado.
        - Insertar la información transformada en la tabla principal de precios.
        - Insertar los precios históricos asociados con cada criptomoneda.

    No recibe parámetros y no retorna valores.
    """
    raw_data = extract_crypto_data()
    transformed_data = transform_data(raw_data)
    insert_crypto_data(transformed_data)
    for data in transformed_data:
        insert_historical_price(data['name'], data['actual_price'], data['timestamp'])


@app.route('/api/crypto', methods=['GET'])
def get_crypto_data():
    """
    Controlador de la API para obtener datos de criptomonedas.

    Obtiene la información actual de las criptomonedas, incluyendo señales de compra/venta y métricas estadísticas.
    Los pasos incluyen:
        - Actualización de los datos almacenados en la base de datos.
        - Lectura de los datos de criptomonedas desde la base de datos.
        - Cálculo de señales (compra/venta) y métricas (máximo, mínimo, promedio de precio en la última hora).

    Returns:
        JSON: Una lista de datos de criptomonedas con las siguientes claves:
            - 'name': El nombre de la criptomoneda.
            - 'actual_price': Precio actual.
            - 'highest_1h': Precio más alto en la última hora.
            - 'lower_1h': Precio más bajo en la última hora.
            - 'avg_price': Precio promedio en la última hora.
            - 'signal': Señal de compra ('B'), venta ('S') o None.
    """
    fetch_and_store_data()
    crypto_data = get_all_crypto_data()
    signals_data = []
    for data in crypto_data:
        historical_prices = get_historical_prices(data['name'])
        signal = generate_signal(historical_prices)
        metrics = calculate_metrics(historical_prices)
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
    """
    Renderiza la página principal de la aplicación.
    Returns:
        Response: La plantilla HTML de la página principal.
    """
    return render_template('index.html')


if __name__ == '__main__':
    """
    Punto de entrada del script.
    Inicializa la base de datos y ejecuta la aplicación Flask en un servidor local.
    """
    init_db()
    app.run()
