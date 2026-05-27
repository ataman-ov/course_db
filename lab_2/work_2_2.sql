SELECT 
    COUNT(*) AS "Количество изделий"
FROM product p
JOIN release_year ry ON p.year_id = ry.year_id
JOIN production pr ON p.product_id = pr.product_id
WHERE pr.output_volume > 500
  AND ry.release_year > 2022;
