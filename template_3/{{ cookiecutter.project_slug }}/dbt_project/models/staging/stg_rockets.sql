{% raw %}{{ config(materialized='view', schema="staging") }}{% endraw %}

WITH source_data AS (
    SELECT * FROM raw_rockets
)

SELECT * FROM source_data