CREATE TABLE IF NOT EXISTS crypto_prices (
    name VARCHAR(255) PRIMARY KEY,
    code VARCHAR(10),
    actual_price DECIMAL(20,8),
    last_updated DATETIME
);

CREATE TABLE IF NOT EXISTS historical_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    code VARCHAR(10),
    price DECIMAL(20,8),
    timestamp DATETIME
);
