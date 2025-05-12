from datetime import datetime, timedelta

def transform_price(price_str):
    """Transforma una cadena de precio con formato 'XXX.XXX,X' a float."""
    try:
        # Reemplazar el punto (separador de miles) por una cadena vacía
        sin_separador_miles = price_str.replace('.', '')
        # Reemplazar la coma (separador decimal) por un punto
        precio_float_str = sin_separador_miles.replace(',', '.')
        # Convertir la cadena resultante a float
        precio_float = float(precio_float_str)
        return precio_float
    except ValueError:
        return None

def transform_data(extract_data):
    transform_data = []
    if extract_data is None:
        return

    for data in extract_data:
        transform_data.append({
            'name': data[2],
            'code': data[4],
            'actual_price': transform_price(data[6]),
            'timestamp':datetime.now()
        })
    
    return transform_data