CREATE TABLE product_group (
    group_id SERIAL PRIMARY KEY,
    group_name VARCHAR(100) NOT NULL
);

CREATE TABLE release_year (
    year_id SERIAL PRIMARY KEY,
    release_year INTEGER NOT NULL
);

CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    product_code VARCHAR(50) NOT NULL,
    group_id INTEGER NOT NULL,
    year_id INTEGER NOT NULL,

    CONSTRAINT fk_product_group
        FOREIGN KEY (group_id)
        REFERENCES product_group(group_id),

    CONSTRAINT fk_product_year
        FOREIGN KEY (year_id)
        REFERENCES release_year(year_id)
);

CREATE TABLE production (
    production_id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    output_volume INTEGER NOT NULL,
    metal_consumption NUMERIC(10,2) NOT NULL,

    CONSTRAINT fk_production_product
        FOREIGN KEY (product_id)
        REFERENCES product(product_id)
);
