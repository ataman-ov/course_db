SELECT 
    p.product_code AS "Обозначение изделия",
    pg.group_name AS "Группа изделий",
    ry.release_year AS "Год выпуска",
    pr.output_volume AS "Объем выпуска",
    pr.metal_consumption AS "Расход металла"
FROM product p
JOIN product_group pg ON p.group_id = pg.group_id
JOIN release_year ry ON p.year_id = ry.year_id
JOIN production pr ON p.product_id = pr.product_id
WHERE pr.output_volume > 500
  AND ry.release_year > 2022;
