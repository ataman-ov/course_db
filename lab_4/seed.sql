SET client_encoding = 'UTF8';

INSERT INTO product_groups (group_name) VALUES
    ('Машиностроение'),
    ('Металлоконструкции'),
    ('Приборостроение'),
    ('Комплектующие')
ON CONFLICT (group_name) DO NOTHING;

INSERT INTO products (
    product_code,
    group_id,
    release_year,
    output_volume,
    metal_consumption,
    note
)
SELECT 'IZD-1001', group_id, 2022, 1200, 15.75, 'Базовая серия'
FROM product_groups
WHERE group_name = 'Машиностроение'
ON CONFLICT (product_code) DO NOTHING;

INSERT INTO products (
    product_code,
    group_id,
    release_year,
    output_volume,
    metal_consumption,
    note
)
SELECT 'MK-2040', group_id, 2023, 850, 42.30, 'Усиленная конструкция'
FROM product_groups
WHERE group_name = 'Металлоконструкции'
ON CONFLICT (product_code) DO NOTHING;

INSERT INTO products (
    product_code,
    group_id,
    release_year,
    output_volume,
    metal_consumption,
    note
)
SELECT 'PR-330', group_id, 2024, 2100, 3.40, 'Малая серия'
FROM product_groups
WHERE group_name = 'Приборостроение'
ON CONFLICT (product_code) DO NOTHING;

INSERT INTO products (
    product_code,
    group_id,
    release_year,
    output_volume,
    metal_consumption,
    note
)
SELECT 'KMP-77', group_id, 2024, 5000, 1.25, 'Расход металла на единицу'
FROM product_groups
WHERE group_name = 'Комплектующие'
ON CONFLICT (product_code) DO NOTHING;
