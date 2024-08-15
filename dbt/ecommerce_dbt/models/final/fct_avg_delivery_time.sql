{{ config(
    materialized='table'
) }}

SELECT
    avg_delivery_hours
FROM {{ ref('int_avg_delivery_time') }}