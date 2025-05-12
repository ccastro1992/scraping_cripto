import sqlite3
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
DATABASE = 'scraping_cripto.db'
db_path = os.path.join(script_dir, DATABASE)

def get_db():
    """Abre una conexión a la base de datos SQLite y configura la fábrica de filas para acceder a las columnas mediante nombres."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Inicializa la base de datos ejecutando el script de esquema SQL.

    El script de esquema se encuentra en el archivo 'schema.sql'.
    Crea o reemplaza tablas y su estructura siguiendo las definiciones contenidas en dicho archivo.
    """
    schema_path = os.path.join(script_dir, 'schema.sql')
    with get_db() as db:
        with open(schema_path, 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    """
    Ejecuta una consulta de solo lectura en la base de datos.

    Args:
        query (str): Consulta SQL que se ejecutará.
        args (tuple, opcional): Lista de parámetros para la consulta. Por defecto es una tupla vacía.
        one (bool, opcional): Si es True, devuelve solo la primera fila del resultado. Por defecto es False.

    Returns:
        list | dict | None: Resultados de la consulta. Si 'one' es True, devuelve un diccionario o None.
    """
    conn = get_db()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    """
    Ejecuta una consulta de escritura o modificación en la base de datos.

    Args:
        query (str): Consulta SQL que se ejecutará.
        args (tuple, opcional): Lista de parámetros para la consulta. Por defecto es una tupla vacía.

    Esta función realiza operaciones como inserciones, actualizaciones o eliminaciones.
    """
    conn = get_db()
    cur = conn.execute(query, args)
    conn.commit()
    cur.close()
    conn.close()

def insert_crypto_data(crypto_data):
    """
    Inserta o actualiza registros en la tabla `crypto_prices` usando datos de criptomonedas.

    Args:
        crypto_data (list[dict]): Lista de diccionarios, cada uno con la información de una criptomoneda.
            Ejemplo:
                [{
                    'name': 'Bitcoin',
                    'actual_price': 50000,
                    'timestamp': '2023-10-26 12:00:00'
                }]

    Esta función reemplaza registros existentes si la criptomoneda ya estaba en la base de datos.
    """
    if crypto_data is not None:
        with get_db() as db:
            for data in crypto_data:
                db.execute(
                    'INSERT OR REPLACE INTO crypto_prices (name, actual_price, last_updated) VALUES (?, ?, ?)',
                    (data['name'], data['actual_price'], data['timestamp'])
                )
            db.commit()

def get_all_crypto_data():
    """
    Recupera todos los registros de la tabla `crypto_prices`.

    Returns:
        list[dict]: Lista de diccionarios con los datos de todas las criptomonedas.
    """
    return query_db("SELECT name, actual_price FROM crypto_prices")

def get_historical_prices(name, limit=100):
    """
    Recupera los precios históricos de una criptomoneda específica.

    Args:
        name (str): Nombre de la criptomoneda.
        limit (int, opcional): Número máximo de registros a recuperar. Por defecto es 100.

    Returns:
        list[dict]: Lista de diccionarios con los precios históricos.
    """
    return query_db('SELECT price, timestamp FROM historical_prices WHERE name = ? ORDER BY timestamp DESC LIMIT ?', (name, limit))

def insert_historical_price(name, price, timestamp):
    """
    Inserta un precio histórico para una criptomoneda en la tabla `historical_prices`.

    Args:
        name (str): Nombre de la criptomoneda.
        price (float): Precio en el momento especificado.
        timestamp (str): Marca de tiempo en formato ISO (YYYY-MM-DD HH:MM:SS).
    """
    execute_db('INSERT INTO historical_prices (name, price, timestamp) VALUES (?, ?, ?)', (name, price, timestamp))

if __name__ == '__main__':
    """
    Punto de entrada del script para inicializar la base de datos.

    Llama a init_db() para crear las tablas y estructura definidas en 'schema.sql', si aún no existen.
    """
    init_db()
    print("Base de datos inicializada.")