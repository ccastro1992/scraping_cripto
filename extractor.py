import logging
import shutil

import cloudscraper
import requests
from bs4 import BeautifulSoup, NavigableString
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://es.investing.com/crypto"
logging.basicConfig(level=logging.DEBUG)


def scrape_with_selenium():
    """
    Realiza un web scraping de datos de criptomonedas utilizando Selenium.

    La función utiliza un navegador Chrome en modo 'headless' para navegar al sitio objetivo,
    captura la tabla dinámica de criptomonedas y extrae sus datos en un formato tabular.

    Returns:
        list: Lista de listas, donde cada sublista representa una fila con datos de una criptomoneda.
    """
    PATH_TO_CHROMEDRIVER = "/usr/bin/chromedriver"
    chromedriver_path = shutil.which("chromedriver")
    if chromedriver_path:
        PATH_TO_CHROMEDRIVER = chromedriver_path

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Navegación en modo sin cabeza
    chrome_options.add_argument("--disable-gpu")  # Desactiva GPU
    chrome_options.add_argument("--disable-extensions")  # Desactiva extensiones innecesarias
    chrome_options.add_argument("--no-sandbox")  # Requerido en algunos entornos Linux
    chrome_options.add_argument("--disable-dev-shm-usage")  # Reduce el uso de memoria compartida
    chrome_options.add_argument("--window-size=1920x1080")

    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # Inicializar el controlador
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=chrome_options, service=service)

    try:
        # Navegar al sitio web
        driver.get(URL)

        # Esperar a que el elemento dinámico esté cargado
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'datatable-v2_table__93S4Y'))
        )

        # Capturar la tabla completa
        table = driver.find_element(By.CLASS_NAME, 'datatable-v2_table__93S4Y')
        tbody = table.find_element(By.TAG_NAME, 'tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')[:5]

        crypto_data = []
        for row in rows:
            vals = []
            cols = row.find_elements(By.TAG_NAME, 'td')

            for col in cols:
                vals.append(col.text)
            vals.insert(0, '')  # Elemento agregado siguiendo el formato esperado
            vals.insert(3, '')
            vals.insert(5, '')

            crypto_data.append(vals)

        return crypto_data
    finally:
        driver.quit()


def scrape_with_beautifulsoup():
    """
    Realiza un web scraping de datos de criptomonedas utilizando BeautifulSoup.

    La función hace una solicitud HTTP al sitio objetivo a través de la librería `cloudscraper`
    y extrae los datos relevantes de criptomonedas desde una tabla HTML.

    Returns:
        list: Lista de listas, donde cada sublista contiene los datos de una criptomoneda.
        None: En caso de errores HTTP o si no se encuentran datos.
    """
    try:
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
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        div_crypto = soup.find('div', {'class': 'crypto-coins-table_crypto-coins-table-container__bgBaf'})
        first_div = div_crypto.find('div')
        second_div = first_div.find('div')
        table = second_div.find('table')
        if not table:
            logging.warning("No se encontró la tabla de criptomonedas")

        rows = table.find('tbody').find_all('tr', limit=5)
        crypto_data = []
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


def extract_crypto_data():
    """
    Extrae datos de criptomonedas.

    Llama a una de las funciones de scraping disponibles (`scrape_with_selenium` o `scrape_with_beautifulsoup`)
    para extraer datos de criptomonedas desde el sitio web.

    Returns:
        list: Lista de datos de criptomonedas extraídos.
    """
    return scrape_with_selenium()


if __name__ == '__main__':
    """
    Punto de entrada del script.

    Extrae los datos de criptomonedas y los imprime en la salida estándar.
    """
    data = extract_crypto_data()
