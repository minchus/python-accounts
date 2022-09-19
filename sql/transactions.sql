BEGIN TRANSACTION;

CREATE TABLE transactions (
    date TEXT NOT NULL,
    type TEXT,
    description TEXT NOT NULL,
    value NUMERIC NOT NULL,
    balance NUMERIC,
    account_name TEXT,
    account_number TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ( date, description, value)
);

CREATE INDEX date ON transactions (date);
CREATE INDEX description ON transactions (value);
CREATE INDEX value ON transactions (value);

COMMIT;