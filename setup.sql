CREATE DATABASE IF NOT EXISTS nm;
CREATE USER IF NOT EXISTS 'maxtrussell'@'localhost';
GRANT ALL PRIVILEGES ON nm.* TO 'maxtrussell'@'localhost';
USE nm;

CREATE TABLE IF NOT EXISTS food (
    name VARCHAR(255) NOT NULL,
    fat FLOAT NOT NULL,
    carbs FLOAT NOT NULL,
    protein FLOAT NOT NULL,
    alcohol FLOAT,
    sugar FLOAT,
    fiber FLOAT,
    servings JSON,
    username VARCHAR(255),
    PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS food_log (
    time TIMESTAMP NOT NULL,
    name VARCHAR(255) NOT NULL,
    serving VARCHAR(255) NOT NULL,
    quantity FLOAT NOT NULL,
    PRIMARY KEY (time)
);

CREATE TABLE IF NOT EXISTS weight_log (
    time TIMESTAMP NOT NULL,
    weight FLOAT NOT NULL,
    notes VARCHAR(255),
    PRIMARY KEY (time)
);

