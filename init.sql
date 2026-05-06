-- Script d'initialisation de la base de données
-- Exécuté automatiquement au premier démarrage du conteneur PostgreSQL

CREATE TABLE IF NOT EXISTS categories (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255),
    category_id VARCHAR(255),
    parent_id   INTEGER,
    url         VARCHAR(2048),
    level       INTEGER,
    image_url   VARCHAR(2048)
);

CREATE TABLE IF NOT EXISTS product (
    id               SERIAL PRIMARY KEY,
    product_id       INTEGER,
    product_code     INTEGER,
    product_category VARCHAR(255),
    name             VARCHAR(255) NOT NULL,
    price_euros      FLOAT,
    price_cents      FLOAT,
    price_concat     FLOAT,
    url              VARCHAR(2048),
    description      TEXT
);