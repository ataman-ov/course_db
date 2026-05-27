SET client_encoding = 'UTF8';

DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS product_groups;

CREATE TABLE product_groups (
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_code VARCHAR(50) NOT NULL UNIQUE,
    group_id INTEGER NOT NULL,
    release_year INTEGER NOT NULL,
    output_volume INTEGER NOT NULL,
    metal_consumption NUMERIC(10, 2) NOT NULL,
    note TEXT,
    CONSTRAINT fk_products_group
        FOREIGN KEY (group_id)
        REFERENCES product_groups(group_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT chk_products_release_year
        CHECK (release_year BETWEEN 1900 AND 2100),
    CONSTRAINT chk_products_output_volume
        CHECK (output_volume >= 0),
    CONSTRAINT chk_products_metal_consumption
        CHECK (metal_consumption >= 0)
);

CREATE INDEX idx_products_code ON products(product_code);
CREATE INDEX idx_products_year ON products(release_year);
CREATE INDEX idx_products_group_id ON products(group_id);
