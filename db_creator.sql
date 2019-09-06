-- bdd du projet 5

-- NOTE: si dans base 1 CHAR(10) et VARCHAR(255)
-- mysql convertit automatiquement CHAR(10) en VARCHAR(10).

-- Database
-- -------
-- -------
DROP DATABASE IF EXISTS Python

CREATE DATABASE Python;

USE Python;

-- Tables
-- -------
-- -------

DROP TABLE IF EXISTS User, Substitute, Brand, Label, Search;

CREATE TABLE User (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    pseudo char(100) NOT NULL,
    password char(30) NOT NULL,
    PRIMARY KEY (id)
)ENGINE = INNODB;

CREATE TABLE Search (
    user_id SMALLINT UNSIGNED NOT NULL,
    substitute_id SMALLINT UNSIGNED NOT NULL,
    day_date DATETIME,
    category CHAR(100) NOT NULL,
    product_name CHAR(100) NOT NULL,
    PRIMARY KEY (user_id, substitute_id)
)ENGINE = INNODB;

DROP TABLE IF EXISTS Product;
CREATE TABLE Product (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    category VARCHAR(60) NOT NULL,
    name VARCHAR(150) NOT NULL,
    labels VARCHAR(300),
    additives VARCHAR(150) ,
    packagings VARCHAR(300) ,
    nutrition_grade VARCHAR(5),
    nova_group VARCHAR(5),
    traces VARCHAR(120),
    manufacturing_places_tags VARCHAR(500),
    minerals_tags VARCHAR(50),
    palm_oil VARCHAR(5),
    composition VARCHAR(1800),
    link VARCHAR(200),
    quantity VARCHAR(10),
    brands VARCHAR(80),
    nutriments VARCHAR(3500),
    PRIMARY KEY (id)
)ENGINE = INNODB;
