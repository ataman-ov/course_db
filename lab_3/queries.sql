-- База данных: production_db

-- Исключительная ситуация:
-- добавляем изделие, у которого нет записи об объеме выпуска
INSERT INTO product (product_code, group_id, year_id)
VALUES ('ИЗД-004', 1, 2);

-- 1. Выборка: обозначение изделия и объем выпуска
-- Если объема выпуска нет, выводится "объем выпуска неизвестен"

SELECT 
    p.product_code AS "Обозначение изделия",
    COALESCE(
        pr.output_volume::TEXT,
        'объем выпуска неизвестен'
    ) AS "Объем выпуска"
FROM product p
LEFT JOIN production pr ON p.product_id = pr.product_id;


-- 2. Изделия, у которых объем выпуска ниже среднего по группе изделий

SELECT 
    p.product_code AS "Обозначение изделия",
    pg.group_name AS "Группа изделий",
    ry.release_year AS "Год выпуска",
    pr.metal_consumption AS "Расход металла",
    pr.output_volume AS "Объем выпуска",
    avg_table.avg_output AS "Средний объем по группе"
FROM product p
JOIN product_group pg ON p.group_id = pg.group_id
JOIN release_year ry ON p.year_id = ry.year_id
JOIN production pr ON p.product_id = pr.product_id
JOIN (
    SELECT 
        p.group_id,
        AVG(pr.output_volume) AS avg_output
    FROM product p
    JOIN production pr ON p.product_id = pr.product_id
    GROUP BY p.group_id
) avg_table ON p.group_id = avg_table.group_id
WHERE pr.output_volume < avg_table.avg_output;


-- 3. Вывести по группам изделий и годам
-- Группы изделий — строки
-- Годы выпуска — столбцы

SELECT 
    pg.group_name AS "Группа изделий",

    SUM(CASE WHEN ry.release_year = 2022 THEN pr.output_volume ELSE 0 END) AS "2022",
    SUM(CASE WHEN ry.release_year = 2023 THEN pr.output_volume ELSE 0 END) AS "2023",
    SUM(CASE WHEN ry.release_year = 2024 THEN pr.output_volume ELSE 0 END) AS "2024"

FROM product_group pg
LEFT JOIN product p ON pg.group_id = p.group_id
LEFT JOIN release_year ry ON p.year_id = ry.year_id
LEFT JOIN production pr ON p.product_id = pr.product_id
GROUP BY pg.group_name
ORDER BY pg.group_name;
