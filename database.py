import sqlite3
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
DATABASE = 'scraping_cripto.db'
db_path = os.path.join(script_dir, DATABASE)

def get_db():
    """Abre una conexión a la base de datos SQLite y configura la fábrica de filas para acceder a las columnas mediante nombres."""
    import mysql.connector

    conn = mysql.connector.connect(
        host="localhost",  # Servidor MySQL
        user="operador",  # Usuario de MySQL
        password="",  # Contraseña
        database="scraping_cripto",  # Nombre de la base de datos
        auth_plugin = 'mysql_native_password'
    )
    return conn


def init_db():
    """
    Inicializa la base de datos ejecutando el script de esquema SQL.

    El script de esquema se encuentra en el archivo 'schema.sql'.
    Crea o reemplaza tablas y su estructura siguiendo las definiciones contenidas en dicho archivo.
    """
    schema_path = os.path.join(script_dir, 'schema.sql')
    conn = get_db()
    cursor = conn.cursor()

    try:
        with open(schema_path, 'r') as f:
            # Leemos todo el contenido del archivo
            sql_commands = f.read()
            # Dividimos por ; para ejecutar cada comando por separado
            commands = sql_commands.split(';')

            for command in commands:
                # Ignoramos líneas vacías o solo con espacios
                if command.strip():
                    cursor.execute(command)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


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
    cursor = conn.cursor(dictionary=True)  # Para obtener resultados como diccionarios

    try:
        cursor.execute(query, args)
        rv = cursor.fetchall()
        return (rv[0] if rv else None) if one else rv
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


def execute_db(query, args=()):
    """
    Ejecuta una consulta de escritura o modificación en la base de datos.

    Args:
        query (str): Consulta SQL que se ejecutará.
        args (tuple, opcional): Lista de parámetros para la consulta. Por defecto es una tupla vacía.

    Esta función realiza operaciones como inserciones, actualizaciones o eliminaciones.
    """
    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute(query, args)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
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
        conn = get_db()
        cursor = conn.cursor()

        try:
            for data in crypto_data:
                cursor.execute('''
                               INSERT INTO crypto_prices (name, actual_price, last_updated)
                               VALUES (%s, %s, %s) ON DUPLICATE KEY
                               UPDATE
                                   actual_price =
                               VALUES (actual_price), last_updated =
                               VALUES (last_updated)
                               ''', (data['name'], data['actual_price'], data['timestamp']))

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()


def get_all_crypto_data():
    """
    Recupera todos los registros de la tabla `crypto_prices`.

    Returns:
        list[dict]: Lista de diccionarios con los datos de todas las criptomonedas.
            Cada diccionario contiene 'name' y 'actual_price'.
        list[]: Lista vacía si hay un error o no hay datos.
    """
    try:
        results = query_db("""
            SELECT 
                name,
                CAST(actual_price AS DECIMAL(20,8)) as actual_price 
            FROM crypto_prices
            WHERE actual_price IS NOT NULL
            ORDER BY name
        """)
        return results if results else []
    except Exception as e:
        print(f"Error al obtener datos de criptomonedas: {e}")
        return []


def get_historical_prices(name, limit=100):
    """
    Recupera los precios históricos de una criptomoneda específica.

    Args:
        name (str): Nombre de la criptomoneda.
        limit (int, opcional): Número máximo de registros a recuperar. Por defecto es 100.

    Returns:
        list[dict]: Lista de diccionarios con los precios históricos.
            Cada diccionario contiene 'price' y 'timestamp'.
        list[]: Lista vacía si hay un error o no hay datos.
    """
    try:
        return query_db('''
            SELECT 
                CAST(price AS DECIMAL(20,8)) as price,
                timestamp 
            FROM historical_prices 
            WHERE name = %s 
                AND price IS NOT NULL 
            ORDER BY timestamp DESC 
            LIMIT %s
        ''', (name, limit)) or []
    except Exception as e:
        print(f"Error al obtener precios históricos para {name}: {e}")
        return []

def insert_historical_price(name, price, timestamp):
    """
    Inserta un precio histórico para una criptomoneda en la tabla `historical_prices`.

    Args:
        name (str): Nombre de la criptomoneda.
        price (float): Precio en el momento especificado.
        timestamp (str): Marca de tiempo en formato ISO (YYYY-MM-DD HH:MM:SS).

    Raises:
        Exception: Si hay un error al insertar los datos.
    """
    try:
        execute_db('''
            INSERT INTO historical_prices 
                (name, price, timestamp) 
            VALUES 
                (%s, CAST(%s AS DECIMAL(20,8)), %s)
        ''', (name, price, timestamp))
    except Exception as e:
        print(f"Error al insertar precio histórico para {name}: {e}")
        raise

if __name__ == '__main__':
    """
    Punto de entrada del script para inicializar la base de datos.

    Llama a init_db() para crear las tablas y estructura definidas en 'schema.sql', si aún no existen.
    """
    init_db()
    print("Base de datos inicializada.")