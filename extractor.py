from flask import Flask, jsonify, render_template
import requests
from bs4 import BeautifulSoup, NavigableString
import time
import logging
import cloudscraper
import time
from datetime import datetime, timedelta

URL = "https://es.investing.com/crypto/currencies"
logging.basicConfig(level=logging.DEBUG)

def extract_crypto_data():
    try:
        # Intentar con requests y BeautifulSoup primero
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        response = scraper.get(URL)

        # response = requests.get(URL, headers=headers, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        div_crypto = soup.find('div', {'class': 'crypto-coins-table_crypto-coins-table-container__bgBaf'})
        first_div = div_crypto.find('div')
        second_div = first_div.find('div')
        table = second_div.find('table')
        if not table:
            logging.warning("No se encontró la tabla de criptomonedas")

        rows = table.find('tbody').find_all('tr', limit=1)  # Limitar a 5 criptomonedas
        crypto_data = []
        #labels = ['CodigEstado', 'Nro', 'Logo', 'Nombre', 'Precio', 'Var.(24h)', 'Var.(7d)', 'Cap. mercado', 'Vol.(24h)', 'Vol. total', 'Codigo 2'] 
        for row in rows:
            try:
                vals = []
                cols = row.find_all('td')
                for col in cols:
                    if col:
                        for x in col.contents:
                            if isinstance(x, NavigableString):
                                texto = x.strip()
                                if texto:
                                    vals.append(texto)
                            elif len(x.contents) > 1:
                                for y in x.contents:
                                    texto = y.get_text(strip=True)
                                    if texto:
                                        vals.append(texto)
                            elif x.name in ['span', 'div']:
                                texto = x.get_text(strip=True)
                                if texto:
                                    vals.append(texto)
                            
                crypto_data.append(vals)
            except AttributeError as e:
                logging.warning("Error al procesar una fila: %s", e)
                continue

        if not crypto_data:
            logging.warning("No se obtuvieron datos con requests")

        return crypto_data
    except requests.RequestException as e:
        logging.error("Error en la solicitud HTTP: %s", e)
    except Exception as e:
        logging.error("Error general en el scraping: %s", e)

if __name__ == '__main__':
    data = extract_crypto_data()