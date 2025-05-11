DROP TABLE IF EXISTS crypto_prices;
CREATE TABLE crypto_prices (
    name TEXT PRIMARY KEY,
    code TEXT,
    actual_price REAL,
    last_updated DATETIME
);

DROP TABLE IF EXISTS historical_prices;
CREATE TABLE historical_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    code TEXT,
    price REAL,
    timestamp DATETIME
);