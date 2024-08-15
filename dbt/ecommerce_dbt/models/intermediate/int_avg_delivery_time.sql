{{ config(
    materialized='view'
) }}

WITH delivery_time AS (
    SELECT
        order_id,
        order_purchase_timestamp,
        order_delivered_customer_date,
        TIMESTAMP_DIFF(order_delivered_customer_date, order_purchase_timestamp, SECOND) AS delivery_seconds
    FROM {{ ref('stg_orders') }}
    WHERE order_status = 'delivered'
)

-- Convert the time from second to hours and rounding to 2 decimal places
SELECT
    ROUND(AVG(delivery_seconds) / 3600, 2) AS avg_delivery_hours
FROM delivery_time