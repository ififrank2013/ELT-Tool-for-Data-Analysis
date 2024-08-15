{{ config(
    materialized='view'
) }}

SELECT
    p.product_id,
    p.product_category_name,
    oi.price
FROM {{ source('ecommerce_data', 'products') }} AS p
LEFT JOIN {{ source('ecommerce_data', 'order_items') }} AS oi
ON p.product_id = oi.product_id