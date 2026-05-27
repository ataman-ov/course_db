INSERT INTO product_group (group_name) VALUES
('Детали'),
('Узлы'),
('Механизмы');

INSERT INTO release_year (release_year) VALUES
(2022),
(2023),
(2024);

INSERT INTO product (product_code, group_id, year_id) VALUES
('ИЗД-001', 1, 1),
('ИЗД-002', 2, 2),
('ИЗД-003', 3, 3);

INSERT INTO production (product_id, output_volume, metal_consumption) VALUES
(1, 1500, 320.50),
(2, 800, 275.00),
(3, 450, 510.80);
