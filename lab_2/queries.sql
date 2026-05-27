-- 1. Список группы изделий определенного года выпуска
-- Год выпуска задается пользователем

SELECT 
    pg.group_name AS "Группа изделий",
    p.product_code AS "Обозначение изделия",
    ry.release_year AS "Год выпуска"
FROM product p
JOIN product_group pg ON p.group_id = pg.group_id
JOIN release_year ry ON p.year_id = ry.year_id
WHERE ry.release_year = 2023;
