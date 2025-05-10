from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import time
import logging
import cloudscraper

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.DEBUG)

# URL de la página de criptomonedas de Investing.com
URL = "https://es.investing.com/crypto/currencies"


# Función para obtener datos de criptomonedas
def fetch_crypto_data():
    try:
        # Intentar con requests y BeautifulSoup primero
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd"
        response = requests.get(url)
        return response.json()

        # response = requests.get(URL, headers=headers, timeout=5)
        response.raise_for_status()
        logging.debug("Solicitud exitosa con requests a %s", URL)

        soup = BeautifulSoup(response.text, 'html.parser')
        div_crypto = soup.find('div', {'class': 'crypto-coins-table_crypto-coins-table-container__bgBaf'})
        first_div = div_crypto.find('div')
        second_div = first_div.find('div')
        table = second_div.find('table')
        if not table:
            logging.warning("No se encontró la tabla de criptomonedas")

        rows = table.find('tbody').find_all('tr', limit=5)  # Limitar a 5 criptomonedas
        crypto_data = []

        for row in rows:
            try:
                vals = []
                cols = row.find_all('td')
                for col in cols:
                    if col:
                        val = col.text.strip()
                        vals.append(val)
                
                crypto_data.append(vals)
            except AttributeError as e:
                logging.warning("Error al procesar una fila: %s", e)
                continue

        if not crypto_data:
            logging.warning("No se obtuvieron datos con requests")

        logging.debug("Datos scrapeados: %s", crypto_data)
        return crypto_data
    except requests.RequestException as e:
        logging.error("Error en la solicitud HTTP: %s", e)
    except Exception as e:
        logging.error("Error general en el scraping: %s", e)


# Ruta para obtener datos en tiempo real
@app.route('/api/crypto', methods=['GET'])
def get_crypto_data():
    try:
        data = fetch_crypto_data()
        response = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'data': data
        }
        # logging.debug("Respuesta enviada: %s", response)
        return jsonify(response)
    except Exception as e:
        logging.error("Error en el endpoint /api/crypto: %s", e)
        return jsonify({'error': 'Error en el servidor'}), 500

# Ruta para servir la página principal
@app.route('/')
def index():
    try:
        with open('templates/index.html', 'r') as file:
            return file.read()
    except FileNotFoundError:
        logging.error("Archivo index.html no encontrado")
        return "Error: Página no encontrada", 404

if __name__ == '__main__':
    app.run()