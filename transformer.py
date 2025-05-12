from datetime import datetime


def transform_price(price_str):
    """
    Transforma una cadena de texto de precio en formato 'XXX.XXX,X' a un valor decimal (float).

    Este método elimina el separador de miles (puntos) y convierte
    el separador decimal (coma) a un punto para facilitar la transformación a `float`.

    Args:
        price_str (str): Cadena de texto que representa el precio en formato 'XXX.XXX,X'.

    Returns:
        float: Precio convertido en formato decimal.
        None: Si ocurre un error en la conversión (por ejemplo, formato inválido).
    """
    try:
        # Reemplazar separadores para adecuar el formato
        sin_separador_miles = price_str.replace('.', '')
        precio_float_str = sin_separador_miles.replace(',', '.')
        precio_float = float(precio_float_str)  # Convertir a float
        return precio_float
    except ValueError:
        return None  # Retornar None si falla la conversión


def transform_data(extract_data):
    """
    Transforma una lista de datos crudos a un formato estructurado y manejable.

    Cada elemento de la lista transformada incluye:
    - Nombre de la criptomoneda.
    - Código de la criptomoneda.
    - Precio actual transformado (como float).
    - Marca temporal (`timestamp`) con la fecha y hora actual en que se realiza la transformación.

    Args:
        extract_data (list or None): Lista de datos crudos extraídos del sitio web, donde cada
                                     elemento es otra lista que contiene la información en formato
                                     desestructurado.

    Returns:
        list or None: Lista de diccionarios con la estructura transformada, o `None` si
                      `extract_data` es `None`.
    """
    transform_data = []
    if extract_data is None:
        return

    for data in extract_data:
        transform_data.append({
            'name': data[2],  # Usa el índice correspondiente para el nombre
            'code': data[4],  # Usa el índice correspondiente para el código
            'actual_price': transform_price(data[6]),  # Convierte el precio con `transform_price`
            'timestamp': datetime.now()  # Registra la hora actual
        })

    return transform_data
