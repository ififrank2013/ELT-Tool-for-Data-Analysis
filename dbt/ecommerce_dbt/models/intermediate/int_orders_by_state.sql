{{ config(
    materialized='view'
) }}

WITH orders_by_state AS (
    SELECT
        customer_state,
        COUNT(order_id) AS total_orders
    FROM {{ ref('stg_orders') }}
    GROUP BY customer_state
)

SELECT
    customer_state,
    total_orders
FROM orders_by_state