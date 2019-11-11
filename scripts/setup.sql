CREATE DATABASE IF NOT EXISTS nm;
CREATE USER IF NOT EXISTS 'maxtrussell'@'localhost';
GRANT ALL PRIVILEGES ON nm.* TO 'maxtrussell'@'localhost';
USE nm;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL AUTO_INCREMENT,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    calories_goal INTEGER,
    fat_goal INTEGER,
    carbs_goal INTEGER,
    protein_goal INTEGER,
    fiber_goal INTEGER,
    sugar_goal INTEGER,
    usda_api_key VARCHAR(64),
    view_verified_foods BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS food (
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    calories FLOAT NOT NULL,
    fat FLOAT NOT NULL,
    carbs FLOAT NOT NULL,
    protein FLOAT NOT NULL,
    alcohol FLOAT,
    sugar FLOAT,
    fiber FLOAT,
    servings JSON,
    username VARCHAR(64),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS food_log (
    id INTEGER NOT NULL AUTO_INCREMENT,
    time TIMESTAMP NOT NULL,
    food_id INTEGER NOT NULL,
    serving VARCHAR(255) NOT NULL,
    quantity FLOAT NOT NULL,
    username VARCHAR(64),
    PRIMARY KEY (id),
    FOREIGN KEY (food_id)
        REFERENCES food(id)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS weight (
    id INTEGER NOT NULL AUTO_INCREMENT,
    date DATE NOT NULL,
    weight FLOAT NOT NULL,
    notes VARCHAR(255),
    username VARCHAR(64) NOT NULL,
    PRIMARY KEY (id)
);
