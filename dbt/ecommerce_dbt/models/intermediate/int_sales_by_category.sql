{{ config(
    materialized='view'
) }}

WITH product_sales AS (
    SELECT
        product_category_name,
        SUM(price) AS total_sales
    FROM {{ ref('stg_products') }}
    GROUP BY product_category_name
)

SELECT
    product_category_name,
    total_sales
FROM product_sales
