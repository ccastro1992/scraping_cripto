import time

import requests
from bs4 import BeautifulSoup


url = "https://consultaweb.ant.gob.ec/PortalWEB/paginas/clientes/clp_criterio_consulta.jsp"
session = requests.Session()

for placa in ['PDU1854', 'PDQ1194', 'PBX6104', 'PCM4901', 'PBE1132', 'EBL0744', 'TDH0668', 'GSH2659', 'IBC4929', 'PBZ3943', 'ABF2068']:
    # Compila los datos que se enviarán
    params = {
        'ps_tipo_identificacion': 'PLA',
        'ps_identificacion': placa
    }

    action_url = 'clp_grid_citaciones.jsp'
    post_url = action_url if action_url.startswith('http') else url.rsplit('/', 1)[0] + '/' + action_url
    response = session.get(post_url, params=params)

    if response.status_code != 200:
        print("Error al enviar el formulario")
        exit()

    result_soup = BeautifulSoup(response.text, 'html.parser')

    # Extraer los datos requeridos
    results_table = result_soup.find_all("table")
    if len(results_table) > 1:
        data = []
        results_table = results_table[1]
        if results_table:
            rows = results_table.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                cols = [col.get_text(strip=True) for col in cols]
                data.append(cols)

        # Imprimir los datos extraídos
        for item in data:
            print(item)

    print('----------------------------------------------------------------------------------------------------------------------')
    time.sleep(1)
