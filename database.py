import sqlite3
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
DATABASE = 'scraping_cripto.db'
db_path = os.path.join(script_dir, DATABASE)

def get_db():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    return conn

def init_db():
    schema_path = os.path.join(script_dir, 'schema.sql')
    with get_db() as db:
        with open(schema_path, 'r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    conn = get_db()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    conn = get_db()
    cur = conn.execute(query, args)
    conn.commit()
    cur.close()
    conn.close()

def insert_crypto_data(crypto_data):
    with get_db() as db:
        for data in crypto_data:
            db.execute(
                'INSERT OR REPLACE INTO crypto_prices (name, actual_price, last_updated) VALUES (?, ?, ?)',
                (data['name'], data['actual_price'], data['timestamp'])
            )
        db.commit()

def get_all_crypto_data():
    return query_db('SELECT name, actual_price FROM crypto_prices')

def get_historical_prices(name, limit=100):
    return query_db('SELECT price, timestamp FROM historical_prices WHERE name = ? ORDER BY timestamp DESC LIMIT ?', (name, limit))

def insert_historical_price(name, price, timestamp):
    execute_db('INSERT INTO historical_prices (name, price, timestamp) VALUES (?, ?, ?)', (name, price, timestamp))

if __name__ == '__main__':
    init_db()
    print("Base de datos inicializada.")